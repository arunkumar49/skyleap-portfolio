import json
from datetime import datetime
from pathlib import Path

from sky_leap.core.config import get_settings
from sky_leap.services.rag.retrieval import retrieve

config = get_settings()

GOLDEN_SET_PATH = Path(__file__).parent / "golden_set.json"
RESULTS_DIR = Path(__file__).parent / "results"
K_VALUES = [1, 3, 5]


class EvalRetrieval:

    def __init__(self, top_k: int = 10):
        self.top_k = top_k

    def load_golden_set(self) -> list[dict]:
        with open(GOLDEN_SET_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    def first_hit_rank(self, retrieved_doc_ids: list[str | None], expected_docs: list[str]) -> int | None:
        """1-based rank of the first chunk that comes from an expected document, or None."""
        for rank, doc_id in enumerate(retrieved_doc_ids, start=1):
            if doc_id in expected_docs:
                return rank
        return None

    def hit_at_k(self, rank: int | None, k: int) -> bool:
        return rank is not None and rank <= k

    def reciprocal_rank(self, rank: int | None) -> float:
        if rank is None:
            return 0.0
        return 1.0 / rank

    def evaluate_question(self, item: dict) -> dict:
        retrieved_chunks = retrieve(item["question"], self.top_k)
        retrieved_doc_ids = [chunk.doc_id for chunk in retrieved_chunks]

        result = {
            "id": item["id"],
            "type": item["type"],
            "question": item["question"],
            "expected_doc": item["expected_doc"],
            "retrieved_doc_ids": retrieved_doc_ids,
        }

        # Unanswerable questions have no expected document, so they are not scored.
        if not item["expected_doc"]:
            result["first_hit_rank"] = None
            for k in K_VALUES:
                result[f"hit@{k}"] = None
            result["reciprocal_rank"] = None
            return result

        rank = self.first_hit_rank(retrieved_doc_ids, item["expected_doc"])
        result["first_hit_rank"] = rank
        for k in K_VALUES:
            result[f"hit@{k}"] = self.hit_at_k(rank, k)
        result["reciprocal_rank"] = self.reciprocal_rank(rank)
        return result

    def _average(self, results: list[dict]) -> dict:
        count = len(results)
        metrics: dict = {"count": count}
        for k in K_VALUES:
            metrics[f"hit@{k}"] = sum(r[f"hit@{k}"] for r in results) / count
        metrics["mrr"] = sum(r["reciprocal_rank"] for r in results) / count
        return metrics

    def compute_metrics(self, results: list[dict]) -> dict:
        scored = [r for r in results if r["expected_doc"]]

        by_type: dict[str, list[dict]] = {}
        for r in scored:
            by_type.setdefault(r["type"], []).append(r)

        return {
            "overall": self._average(scored) if scored else {"count": 0},
            "by_type": {question_type: self._average(items) for question_type, items in by_type.items()},
        }

    def print_table(self, metrics: dict, results: list[dict]) -> None:
        header = f"{'type':<14}{'count':>6}" + "".join(f"{f'hit@{k}':>8}" for k in K_VALUES) + f"{'MRR':>8}"
        print()
        print(header)
        print("-" * len(header))

        rows = list(metrics["by_type"].items()) + [("overall", metrics["overall"])]
        for name, m in rows:
            if name == "overall":
                print("-" * len(header))
            if m["count"] == 0:
                print(f"{name:<14}{0:>6}")
                continue
            line = f"{name:<14}{m['count']:>6}"
            line += "".join(f"{m[f'hit@{k}']:>8.3f}" for k in K_VALUES)
            line += f"{m['mrr']:>8.3f}"
            print(line)

        skipped = len([r for r in results if not r["expected_doc"]])
        print(f"\n{skipped} unanswerable questions were not scored.")

        misses = [r for r in results if r["expected_doc"] and not r[f"hit@{K_VALUES[-1]}"]]
        print(f"\nMisses (no expected doc in top {K_VALUES[-1]}): {len(misses)}")
        for r in misses:
            print(f"  {r['id']} [{r['type']}] {r['question']}")
            print(f"      expected: {', '.join(r['expected_doc'])}")
            print(f"      got:      {', '.join(str(d) for d in r['retrieved_doc_ids'][:3])}")

    def save_results(self, metrics: dict, results: list[dict], run_at: datetime) -> Path:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = RESULTS_DIR / f"retrieval_{run_at.strftime('%Y-%m-%d_%H%M%S')}.json"

        output = {
            "run_at": run_at.isoformat(timespec="seconds"),
            "config": {
                "top_k": self.top_k,
                "rrf_k": config.rrf_k,
                "retrieval_candidates": config.retrieval_candidates,
                "pinecone_namespace": config.pinecone_namespace,
            },
            "metrics": metrics,
            "results": results,
        }

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=2, ensure_ascii=False)

        return output_path

    def run(self) -> None:
        run_at = datetime.now()
        golden_set = self.load_golden_set()

        results = []
        for item in golden_set:
            results.append(self.evaluate_question(item))
            print(f"{item['id']} ... done")

        metrics = self.compute_metrics(results)
        self.print_table(metrics, results)

        output_path = self.save_results(metrics, results, run_at)
        print(f"\nSaved results to {output_path}")


if __name__ == "__main__":
    EvalRetrieval().run()
