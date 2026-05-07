"""Core certainty factor engine."""

from __future__ import annotations

from data.knowledge_base import DISEASES, KNOWLEDGE_BASE, SYMPTOMS


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


def forward_chaining(user_inputs: dict[str, float]) -> dict[str, dict]:
    """Run diagnosis across all diseases from active symptoms."""
    results: dict[str, dict] = {}

    for disease_code, disease_name in DISEASES.items():
        cf_individual_list: list[float] = []
        cf_detail: dict[str, dict] = {}

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
