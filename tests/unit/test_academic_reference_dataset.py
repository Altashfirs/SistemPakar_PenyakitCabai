import json
from pathlib import Path

import pytest

from engine.cf_engine import forward_chaining


DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "academic_reference_cases.json"


with DATASET_PATH.open(encoding="utf-8") as dataset_file:
    ACADEMIC_REFERENCE_CASES = json.load(dataset_file)


@pytest.mark.parametrize("case", ACADEMIC_REFERENCE_CASES, ids=[case["case_id"] for case in ACADEMIC_REFERENCE_CASES])
def test_academic_reference_cases(case: dict) -> None:
    results = forward_chaining(case["user_inputs"])
    candidate_results = [result for result in results.values() if result["is_candidate"]]
    top_result = candidate_results[0]

    assert top_result["code"] == case["expected_top_code"]
    assert top_result["name"] == case["expected_top_name"]
    assert top_result["label"] == case["expected_label"]
    assert top_result["cf_combined"] >= case["min_expected_cf"]
    assert len(candidate_results) == case["expected_candidate_count"]
    if "expected_second_code" in case:
        assert candidate_results[1]["code"] == case["expected_second_code"]
    assert len(case["source_refs"]) >= 1
