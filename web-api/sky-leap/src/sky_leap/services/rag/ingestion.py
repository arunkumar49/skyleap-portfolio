from pathlib import Path
from sky_leap.infrastructure.vector_store.pc_vector_store import upsert_vector
from sky_leap.services.rag.embedding import get_titan_embedding
from unstructured.documents.elements import Element
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.md import partition_md
from unstructured.partition.auto import partition
from sky_leap.core.config import get_settings

config = get_settings()

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
 
# Unstructured sizes are in CHARACTERS. ~1500 chars is roughly 300-400 tokens.
DEFAULT_CHUNKING = dict(
    max_characters=1500,          # hard max; larger elements get text-split
    new_after_n_chars=1000,       # soft max; preferred chunk size
    combine_text_under_n_chars=500,  # merge tiny sections (e.g. a lone heading)
    overlap=200,                  # only applied when an oversized element is split
    multipage_sections=True,
    include_orig_elements=True,   # needed to compute section breadcrumbs
)


# Per-extension overrides
CHUNKING_OVERRIDES = {
    # Respecting page boundaries in a deck = one slide never bleeds into the next
    ".pptx": dict(multipage_sections=False),
    ".ppt": dict(multipage_sections=False),
}
 
# Per-extension partition settings
PARTITION_OVERRIDES = {
    ".pdf": dict(strategy="hi_res", infer_table_structure=True),  # layout model + tables
    ".png": dict(strategy="hi_res", infer_table_structure=True),
    ".jpg": dict(strategy="hi_res", infer_table_structure=True),
    ".jpeg": dict(strategy="hi_res", infer_table_structure=True),
    ".tiff": dict(strategy="hi_res", infer_table_structure=True),
    ".eml": dict(process_attachments=True),
    ".msg": dict(process_attachments=True),
}
 
SPREADSHEET_EXTS = {".xlsx", ".xls", ".csv", ".tsv"}
ROWS_PER_CHUNK = 25
 
# Boilerplate element types to drop before chunking
DROP_CATEGORIES = {"Header", "Footer", "PageBreak", "PageNumber"}
 
# Final token guard (in case any chunk is still too large for the embedding model)
MAX_TOKENS = 800

METADATA_FIELDS = (
    "doc_id", "chunk_index", "name",
    "doc_title", "heading", "subheading", "section_path", "headings",
    "filename", "filetype", "languages", "page_number",
)


def chunk_document(file_path: str) -> list[Element]:
    file = Path(file_path)
    ext = file.suffix.lower()
    
    if not file.is_file():
        raise FileNotFoundError(f"The required file was not found at: {file.absolute()}")
    
    elements = partition(filename=file_path)
    
    chunks = chunk_by_title(elements, **{**DEFAULT_CHUNKING, **CHUNKING_OVERRIDES.get(ext, {})})
    
    _add_heading_metadata(chunks=chunks, file=file.name)
        
    return chunks


def embed_file(file: str, namespace: str):
    # 3. Embed each Element and keep its metadata for your vector DB
    embedded_records = []
    vectors = []
    
    chunks = chunk_document(file)
    
    for chunk in chunks:
        # Skip empty chunks
        if not chunk.text or not chunk.text.strip():
            continue
    
        text_to_embed = chunk.text
        vector = get_titan_embedding(text_to_embed)
        vectors.append(vector)
        # print(vector)

        embedded_records.append({
            "id": f"{chunk.metadata.doc_id}#{chunk.metadata.chunk_index}",
            "values": vector,
            "metadata": _to_pinecone_metadata(chunk, chunk.text),
        })
    upsert_vector(vectors=embedded_records, namespace=namespace)
    
    # print(f"Embedded {embedded_records} chunks.")


def _to_pinecone_metadata(chunk, text: str) -> dict:
    raw = chunk.metadata.to_dict()
    meta = {k: raw[k] for k in METADATA_FIELDS if raw.get(k) is not None}
    meta["text"] = text
    return meta


def _add_heading_metadata(chunks: list[Element], file: str | Path) -> None:
    """Attach doc title, heading, subheading and section path to each chunk.

    Keeps a heading stack (depth -> text) across chunks, so a chunk that starts
    mid-section still knows which section it belongs to.
    """
    stack: dict[int, str] = {}

    for index, chunk in enumerate(chunks):
        context: dict[int, str] | None = None   # headings in effect where the content starts
        headings: list[str] = []                # every heading inside this chunk

        chunk.metadata.chunk_index = index
        chunk.metadata.doc_id = file
        
        for el in chunk.metadata.orig_elements or []:
            if el.category == "Title":
                depth = el.metadata.category_depth or 0
                stack = {d: t for d, t in stack.items() if d < depth}  # drop same/deeper levels
                stack[depth] = el.text
                headings.append(el.text)
            elif context is None:
                context = dict(stack)

        if context is None:          # chunk had only headings
            context = dict(stack)

        if 0 in context:
            chunk.metadata.doc_title = context[0]    # H1
        if 1 in context:
            chunk.metadata.heading = context[1]      # H2
        if 2 in context:
            chunk.metadata.subheading = context[2]   # H3
        if context:
            chunk.metadata.section_path = " > ".join(context[d] for d in sorted(context))
        if headings:
            chunk.metadata.headings = headings

