import json
from pathlib import Path

import pytest

from engine.cf_engine import forward_chaining


DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "diagnosis_cases.json"


with DATASET_PATH.open(encoding="utf-8") as dataset_file:
    DIAGNOSIS_CASES = json.load(dataset_file)


@pytest.mark.parametrize("case", DIAGNOSIS_CASES, ids=[case["case_id"] for case in DIAGNOSIS_CASES])
def test_diagnosis_cases_dataset(case: dict) -> None:
    results = forward_chaining(case["user_inputs"])
    top_result = next(iter(results.values()))

    assert top_result["code"] == case["expected_top_code"]
    assert top_result["name"] == case["expected_top_name"]
    assert top_result["label"] == case["expected_label"]
    assert top_result["cf_combined"] >= case["min_expected_cf"]
    assert top_result["active_symptoms"] > 0
