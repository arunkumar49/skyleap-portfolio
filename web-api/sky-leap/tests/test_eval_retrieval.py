import os

import pytest

# eval_retrieval imports the Pinecone client at module load, which reads config.
os.environ.setdefault("PINECONE_API_KEY", "test-key")

from sky_leap.eval.eval_retrieval import EvalRetrieval


@pytest.fixture
def evaluator() -> EvalRetrieval:
    return EvalRetrieval()


def _result(question_type: str, expected_doc: list[str], rank: int | None) -> dict:
    """A scored result as evaluate_question would build it."""
    if not expected_doc:
        return {"type": question_type, "expected_doc": [], "hit@1": None, "hit@3": None,
                "hit@5": None, "reciprocal_rank": None}
    return {
        "type": question_type,
        "expected_doc": expected_doc,
        "hit@1": rank is not None and rank <= 1,
        "hit@3": rank is not None and rank <= 3,
        "hit@5": rank is not None and rank <= 5,
        "reciprocal_rank": 1 / rank if rank else 0.0,
    }


def test_first_hit_rank_at_top(evaluator):
    assert evaluator.first_hit_rank(["a.md", "b.md"], ["a.md"]) == 1


def test_first_hit_rank_further_down(evaluator):
    assert evaluator.first_hit_rank(["a.md", "b.md", "c.md"], ["c.md"]) == 3


def test_first_hit_rank_no_hit(evaluator):
    assert evaluator.first_hit_rank(["a.md", "b.md"], ["z.md"]) is None


def test_first_hit_rank_any_expected_doc_counts(evaluator):
    assert evaluator.first_hit_rank(["a.md", "c.md", "b.md"], ["b.md", "c.md"]) == 2


def test_first_hit_rank_uses_chunk_rank_with_duplicate_docs(evaluator):
    # Three chunks from a.md come first, so the first b.md chunk is at chunk rank 4.
    assert evaluator.first_hit_rank(["a.md", "a.md", "a.md", "b.md"], ["b.md"]) == 4


def test_first_hit_rank_ignores_missing_doc_id(evaluator):
    assert evaluator.first_hit_rank([None, "a.md"], ["a.md"]) == 2


def test_hit_at_k_and_reciprocal_rank(evaluator):
    assert evaluator.hit_at_k(3, 3) is True
    assert evaluator.hit_at_k(4, 3) is False
    assert evaluator.hit_at_k(None, 5) is False
    assert evaluator.reciprocal_rank(4) == pytest.approx(0.25)
    assert evaluator.reciprocal_rank(None) == 0.0


def test_compute_metrics_averages_and_skips_unanswerable(evaluator):
    results = [
        _result("factual", ["a.md"], 1),
        _result("factual", ["a.md"], 4),
        _result("keyword", ["b.md"], None),
        _result("unanswerable", [], None),
    ]

    metrics = evaluator.compute_metrics(results)

    overall = metrics["overall"]
    assert overall["count"] == 3
    assert overall["hit@1"] == pytest.approx(1 / 3)
    assert overall["hit@3"] == pytest.approx(1 / 3)
    assert overall["hit@5"] == pytest.approx(2 / 3)
    assert overall["mrr"] == pytest.approx((1 + 0.25 + 0) / 3)

    assert set(metrics["by_type"]) == {"factual", "keyword"}
    assert metrics["by_type"]["factual"]["count"] == 2
    assert metrics["by_type"]["factual"]["mrr"] == pytest.approx(0.625)
    assert metrics["by_type"]["keyword"]["hit@5"] == 0.0


def test_compute_metrics_with_only_unanswerable(evaluator):
    metrics = evaluator.compute_metrics([_result("unanswerable", [], None)])

    assert metrics["overall"] == {"count": 0}
    assert metrics["by_type"] == {}
