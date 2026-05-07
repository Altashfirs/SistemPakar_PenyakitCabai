from engine.cf_engine import (
    build_detail_rows,
    build_ranking_rows,
    build_rule_rows,
    calc_cf_individual,
    cf_label,
    combine_cf,
    evaluate_rule,
    fire_rules,
    forward_chaining,
)


def test_calc_cf_individual_multiplies_and_rounds() -> None:
    assert calc_cf_individual(0.9, 0.8) == 0.72
    assert calc_cf_individual(0.33333, 0.33333) == 0.1111


def test_combine_cf_ignores_non_positive_values() -> None:
    assert combine_cf([0, -0.5]) == 0.0
    assert combine_cf([0.2, 0.3]) == 0.44


def test_cf_label_maps_ranges_correctly() -> None:
    assert cf_label(0.0) == "Tidak Ada"
    assert cf_label(0.25) == "Sangat Lemah"
    assert cf_label(0.45) == "Lemah"
    assert cf_label(0.7) == "Sedang"
    assert cf_label(0.85) == "Kuat"
    assert cf_label(0.95) == "Sangat Kuat"


def test_forward_chaining_returns_sorted_results_with_details() -> None:
    user_inputs = {"G01": 1.0, "G02": 0.8, "G03": 0.9, "G25": 0.7}

    results = forward_chaining(user_inputs)
    top_result = next(iter(results.values()))

    assert top_result["code"] == "P1"
    assert top_result["name"] == "Antraknosa (Busuk Buah)"
    assert top_result["cf_combined"] == 0.997
    assert top_result["percentage"] == 99.7
    assert top_result["label"] == "Sangat Kuat"
    assert top_result["is_candidate"] is True
    assert top_result["active_symptoms"] == 4
    assert set(top_result["detail"].keys()) == {"G01", "G02", "G03", "G25"}
    assert {rule["rule_id"] for rule in top_result["fired_rules"]} == {"R-P1-CORE", "R-P1-SIGNAL"}


def test_build_ranking_and_detail_rows_shape() -> None:
    results = forward_chaining({"G12": 1.0, "G13": 0.9, "G15": 1.0})

    ranking_rows = build_ranking_rows(results)
    detail_rows = build_detail_rows(results)
    rule_rows = build_rule_rows(results)

    assert ranking_rows[0]["Kode"] == "P4"
    assert ranking_rows[0]["Penyakit"] == "Virus Kuning (Gemini Virus)"
    assert ranking_rows[0]["Interpretasi"] == "Sangat Kuat"
    assert ranking_rows[0]["Kandidat FC"] == "Ya"

    assert any(row["Kode Gejala"] == "G13" for row in detail_rows)
    assert all("CF(H,E)" in row for row in detail_rows)
    assert any(row["Rule ID"] == "R-P4-CORE" for row in rule_rows)
    assert any(row["Rule ID"] == "R-P4-SIGNAL" for row in rule_rows)


def test_evaluate_rule_and_fire_rules_work_explicitly() -> None:
    user_inputs = {"G18": 1.0, "G19": 0.6}
    evaluation = evaluate_rule(
        user_inputs,
        {
            "rule_id": "R-TEST",
            "disease_code": "PX",
            "name": "Test Rule",
            "antecedents": ["G18", "G19", "G20"],
            "minimum_matches": 2,
        },
    )

    assert evaluation["is_fired"] is True
    assert evaluation["matched_count"] == 2
    assert evaluation["matched_symptoms"] == ["G18", "G19"]

    fired_rules = fire_rules(user_inputs)
    fired_ids = {rule["rule_id"] for rule in fired_rules}
    assert "R-P6-CORE" in fired_ids
    assert "R-P6-SIGNAL" in fired_ids
