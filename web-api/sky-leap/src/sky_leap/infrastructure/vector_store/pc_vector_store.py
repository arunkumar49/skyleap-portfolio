from collections.abc import Mapping, Sequence
from typing import Any

from pinecone import (
    DenseVectorQuery,
    Index,
    Pinecone,
    SearchDocumentsResponse,
    TextQuery,
)
from pinecone.exceptions import PineconeException

from sky_leap.core.config import get_settings
from functools import lru_cache

config = get_settings()

pc = Pinecone(api_key=config.pinecone_api_key)

# Field names declared in the index schema. They must match the index created in Pinecone.
DENSE_FIELD = "embedding"
TEXT_FIELDS = ["chunk_text", "section_path"]
RETURN_FIELDS = ["chunk_text", "section_path", "doc_id"]

@lru_cache
def _get_index() -> Index:
    # The index has a document schema, so it is created once in the Pinecone console,
    # not here. Auto-creating it would build an index without the full-text fields.
    if not pc.has_index(config.pinecone_index):
        raise RuntimeError(
            f"Pinecone index {config.pinecone_index!r} does not exist. Create it with fields "
            f"'chunk_text' and 'section_path' (string, full-text search) and "
            f"'{DENSE_FIELD}' (dense vector, {config.embed_dimensions} dim, cosine)."
        )

    return pc.index(name=config.pinecone_index)


def upsert_documents(documents: Sequence[Mapping[str, Any]], namespace: str) -> None:
    try:
        index = _get_index()
        result = index.documents.batch_upsert(
            namespace=namespace,
            documents=documents,
            show_progress=False,
        )
    except PineconeException as e:
        raise Exception(f"Failed to upsert the documents into pinecone database {e}")

    if result.has_errors:
        failed_ids = [doc.get("_id") for doc in result.failed_items]
        raise Exception(f"Failed to upsert {len(failed_ids)} documents into pinecone database: {failed_ids}")


def search_dense(vector: Sequence[float], namespace: str, top_k: int) -> SearchDocumentsResponse:
    try:
        index = _get_index()
        return index.documents.search(
            namespace=namespace,
            score_by=[DenseVectorQuery(field=DENSE_FIELD, values=list(vector))],
            top_k=top_k,
            include_fields=RETURN_FIELDS,
        )
    except PineconeException as e:
        raise Exception(f"Failed to run dense search in pinecone database {e}")


def search_text(query: str, namespace: str, top_k: int) -> SearchDocumentsResponse:
    try:
        index = _get_index()
        return index.documents.search(
            namespace=namespace,
            score_by=[TextQuery(query=query, fields=TEXT_FIELDS)],
            top_k=top_k,
            include_fields=RETURN_FIELDS,
        )
    except PineconeException as e:
        raise Exception(f"Failed to run full-text search in pinecone database {e}")
