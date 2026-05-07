import json
from pathlib import Path

import pytest

from engine.cf_engine import forward_chaining


DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "diagnosis_edge_cases.json"


with DATASET_PATH.open(encoding="utf-8") as dataset_file:
    EDGE_CASES = json.load(dataset_file)


@pytest.mark.parametrize("case", EDGE_CASES, ids=[case["case_id"] for case in EDGE_CASES])
def test_edge_cases(case: dict) -> None:
    results = forward_chaining(case["user_inputs"])
    ordered_results = list(results.values())
    candidate_results = [result for result in ordered_results if result["is_candidate"]]
    top_result = candidate_results[0] if candidate_results else ordered_results[0]

    assert top_result["code"] == case["expected_top_code"]
    assert top_result["label"] == case["expected_label"]
    assert len(candidate_results) == case["expected_candidate_count"]

    if "expected_second_code" in case:
        assert candidate_results[1]["code"] == case["expected_second_code"]

    if "min_expected_cf" in case:
        assert top_result["cf_combined"] >= case["min_expected_cf"]

    if "max_expected_cf" in case:
        assert top_result["cf_combined"] <= case["max_expected_cf"]
