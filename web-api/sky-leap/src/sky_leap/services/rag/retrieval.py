from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from sky_leap.core.config import get_settings
from sky_leap.infrastructure.vector_store.pc_vector_store import (
    search_dense,
    search_text,
)
from sky_leap.services.rag.embedding import get_titan_embedding

config = get_settings()


@dataclass(frozen=True)
class RetrievedChunk:
    id: str
    chunk_text: str
    section_path: str | None
    doc_id: str | None
    score: float


def reciprocal_rank_fusion(result_lists: Sequence[Sequence[Any]], k: int = 60) -> list[tuple[Any, float]]:
    """Merge ranked lists into one, scoring each document as sum(1 / (k + rank)).

    Each list holds documents with an ``id`` attribute, best first. A document found
    by several lists gets the sum of its scores. Returns (document, score) pairs,
    best first; ties keep the order in which documents were first seen.
    """
    scores: dict[str, float] = {}
    documents: dict[str, Any] = {}

    for results in result_lists:
        for rank, doc in enumerate(results, start=1):
            scores[doc.id] = scores.get(doc.id, 0.0) + 1.0 / (k + rank)
            documents.setdefault(doc.id, doc)

    ranked_ids = sorted(scores, key=lambda doc_id: scores[doc_id], reverse=True)
    return [(documents[doc_id], scores[doc_id]) for doc_id in ranked_ids]


def retrieve(query: str, top_n: int = 3) -> list[RetrievedChunk]:
    """Hybrid search: dense (Titan) + full-text (BM25), merged with reciprocal rank fusion."""
    namespace = config.pinecone_namespace
    candidates = config.retrieval_candidates

    vector = get_titan_embedding(query)
    dense = search_dense(vector, namespace=namespace, top_k=candidates)
    keyword = search_text(query, namespace=namespace, top_k=candidates)

    fused = reciprocal_rank_fusion([dense.matches, keyword.matches], k=config.rrf_k)

    return [
        RetrievedChunk(
            id=doc.id,
            chunk_text=doc.get("chunk_text") or "",
            section_path=doc.get("section_path"),
            doc_id=doc.get("doc_id"),
            score=score,
        )
        for doc, score in fused[:top_n]
    ]
