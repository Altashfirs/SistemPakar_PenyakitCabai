"""Core certainty factor engine."""

from __future__ import annotations

from data.knowledge_base import DISEASES, KNOWLEDGE_BASE, SYMPTOMS
from data.rules import RULES


def calc_cf_individual(cf_pakar: float, cf_user: float) -> float:
    """CF(H,E) = CF pakar x CF user."""
    return round(cf_pakar * cf_user, 4)


def combine_cf(cf_list: list[float]) -> float:
    """Combine positive CF values using MYCIN style accumulation."""
    positive_cfs = [cf for cf in cf_list if cf > 0]
    if not positive_cfs:
        return 0.0

    result = 1.0
    for cf_value in positive_cfs:
        result *= 1 - cf_value
    return round(1 - result, 4)


def cf_label(cf_value: float) -> str:
    """Map CF to interpretation label."""
    if cf_value < 0.2:
        return "Tidak Ada"
    if cf_value < 0.4:
        return "Sangat Lemah"
    if cf_value < 0.6:
        return "Lemah"
    if cf_value < 0.8:
        return "Sedang"
    if cf_value < 0.9:
        return "Kuat"
    return "Sangat Kuat"


def evaluate_rule(user_inputs: dict[str, float], rule: dict) -> dict:
    """Evaluate a single IF-THEN rule against active user symptoms."""
    matched_symptoms = [
        symptom_code
        for symptom_code in rule["antecedents"]
        if user_inputs.get(symptom_code, 0.0) > 0
    ]
    is_fired = len(matched_symptoms) >= rule["minimum_matches"]
    return {
        "rule_id": rule["rule_id"],
        "disease_code": rule["disease_code"],
        "rule_name": rule["name"],
        "antecedents": rule["antecedents"],
        "minimum_matches": rule["minimum_matches"],
        "matched_symptoms": matched_symptoms,
        "matched_count": len(matched_symptoms),
        "is_fired": is_fired,
    }


def fire_rules(user_inputs: dict[str, float]) -> list[dict]:
    """Run forward chaining by firing all matching rules."""
    return [evaluation for evaluation in (evaluate_rule(user_inputs, rule) for rule in RULES) if evaluation["is_fired"]]


def forward_chaining(user_inputs: dict[str, float]) -> dict[str, dict]:
    """Run explicit forward chaining first, then Certainty Factor scoring."""
    results: dict[str, dict] = {}
    fired_rules = fire_rules(user_inputs)
    candidate_rules: dict[str, list[dict]] = {}

    for rule in fired_rules:
        candidate_rules.setdefault(rule["disease_code"], []).append(rule)

    for disease_code, disease_name in DISEASES.items():
        cf_individual_list: list[float] = []
        cf_detail: dict[str, dict] = {}
        disease_rules = candidate_rules.get(disease_code, [])
        is_candidate = bool(disease_rules)

        if is_candidate:
            for symptom_code, cf_user in user_inputs.items():
                if cf_user <= 0:
                    continue

                cf_pakar = KNOWLEDGE_BASE.get(symptom_code, {}).get(disease_code, 0.0)
                if cf_pakar <= 0:
                    continue

                cf_he = calc_cf_individual(cf_pakar, cf_user)
                cf_individual_list.append(cf_he)
                cf_detail[symptom_code] = {
                    "symptom_name": SYMPTOMS[symptom_code],
                    "cf_pakar": cf_pakar,
                    "cf_user": cf_user,
                    "cf_he": cf_he,
                }

        cf_combined = combine_cf(cf_individual_list)
        results[disease_code] = {
            "code": disease_code,
            "name": disease_name,
            "is_candidate": is_candidate,
            "fired_rules": disease_rules,
            "cf_combined": cf_combined,
            "percentage": round(cf_combined * 100, 2),
            "label": cf_label(cf_combined),
            "detail": cf_detail,
            "active_symptoms": len(cf_detail),
        }

    return dict(sorted(results.items(), key=lambda item: item[1]["cf_combined"], reverse=True))


def build_ranking_rows(results: dict[str, dict]) -> list[dict]:
    """Return ranking rows for tables and export."""
    rows = []
    for index, result in enumerate(results.values(), start=1):
        rows.append(
            {
                "Ranking": index,
                "Kode": result["code"],
                "Penyakit": result["name"],
                "CF": result["cf_combined"],
                "Persentase": result["percentage"],
                "Interpretasi": result["label"],
                "Kandidat FC": "Ya" if result["is_candidate"] else "Tidak",
                "Rule Fired": len(result["fired_rules"]),
                "Gejala Aktif": result["active_symptoms"],
            }
        )
    return rows


def build_detail_rows(results: dict[str, dict]) -> list[dict]:
    """Flatten CF detail rows for display and export."""
    rows = []
    for result in results.values():
        for symptom_code, detail in result["detail"].items():
            rows.append(
                {
                    "Kode Penyakit": result["code"],
                    "Penyakit": result["name"],
                    "Kode Gejala": symptom_code,
                    "Gejala": detail["symptom_name"],
                    "CF Pakar": detail["cf_pakar"],
                    "CF User": detail["cf_user"],
                    "CF(H,E)": detail["cf_he"],
                }
            )
    return rows


def build_rule_rows(results: dict[str, dict]) -> list[dict]:
    """Flatten fired forward chaining rules for display and export."""
    rows = []
    for result in results.values():
        for rule in result["fired_rules"]:
            rows.append(
                {
                    "Kode Penyakit": result["code"],
                    "Penyakit": result["name"],
                    "Rule ID": rule["rule_id"],
                    "Rule": rule["rule_name"],
                    "Minimum Match": rule["minimum_matches"],
                    "Matched Count": rule["matched_count"],
                    "Matched Symptoms": ", ".join(rule["matched_symptoms"]),
                }
            )
    return rows
