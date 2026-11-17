import os
from types import SimpleNamespace

import pytest

# retrieval imports the Pinecone client at module load, which reads config.
os.environ.setdefault("PINECONE_API_KEY", "test-key")

from sky_leap.services.rag.retrieval import reciprocal_rank_fusion


def _docs(*ids: str) -> list[SimpleNamespace]:
    return [SimpleNamespace(id=doc_id) for doc_id in ids]


def test_document_in_both_lists_ranks_first():
    dense = _docs("a", "b", "c")
    keyword = _docs("c", "d")

    fused = reciprocal_rank_fusion([dense, keyword], k=60)

    assert fused[0][0].id == "c"
    assert fused[0][1] == pytest.approx(1 / 63 + 1 / 61)


def test_duplicates_are_merged():
    fused = reciprocal_rank_fusion([_docs("a", "b"), _docs("b", "a")], k=60)

    assert [doc.id for doc, _ in fused] == ["a", "b"]
    assert len(fused) == 2


def test_empty_lists():
    assert reciprocal_rank_fusion([], k=60) == []
    assert reciprocal_rank_fusion([[], []], k=60) == []


def test_one_empty_list_keeps_other_order():
    fused = reciprocal_rank_fusion([_docs("a", "b", "c"), []], k=60)

    assert [doc.id for doc, _ in fused] == ["a", "b", "c"]


def test_ties_keep_first_seen_order():
    # "a" is rank 1 in the first list, "x" is rank 1 in the second: equal scores.
    fused = reciprocal_rank_fusion([_docs("a"), _docs("x")], k=60)

    assert [doc.id for doc, _ in fused] == ["a", "x"]
