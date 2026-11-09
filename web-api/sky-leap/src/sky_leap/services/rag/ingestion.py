from pathlib import Path
from unstructured.documents.elements import Element
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.md import partition_md
from unstructured.partition.auto import partition


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
 
# Unstructured sizes are in CHARACTERS. ~1500 chars is roughly 300-400 tokens.
DEFAULT_CHUNKING = dict(
    max_characters=2000,          # hard max; larger elements get text-split
    new_after_n_chars=1500,       # soft max; preferred chunk size
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

def chunk_document(file_path: str) -> list[Element]:
    file = Path(file_path)
    ext = file.suffix.lower()
    
    if not file.is_file():
        raise FileNotFoundError(f"The required file was not found at: {file.absolute()}")
    
    elements = partition(filename=file_path)
    
    chunks = chunk_by_title(elements, **{**DEFAULT_CHUNKING, **CHUNKING_OVERRIDES.get(ext, {})})
    
    for chunk in chunks:
        print(chunk.text)
        print("-" * 40)
        
    return chunks


