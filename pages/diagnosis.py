"""Diagnosis page renderer."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from data.knowledge_base import SYMPTOM_GROUPS, SYMPTOMS
from data.recommendations import RECOMMENDATIONS
from engine.cf_engine import build_detail_rows, build_ranking_rows, forward_chaining
from engine.excel_generator import generate_excel_report


def _init_state() -> None:
    st.session_state.setdefault("last_results", None)
    st.session_state.setdefault("last_inputs", None)
    st.session_state.setdefault("diagnosis_history", [])


def _reset_form() -> None:
    for symptom_code in SYMPTOMS:
        key = f"slider_{symptom_code}"
        if key in st.session_state:
            st.session_state[key] = 0.0
    st.session_state["last_results"] = None
    st.session_state["last_inputs"] = None


def render_diagnosis() -> None:
    _init_state()

    st.title("Diagnosis")
    st.caption("Isi tingkat keyakinan gejala dari 0.0 sampai 1.0, lalu jalankan diagnosis.")

    top_actions = st.columns([3, 1])
    with top_actions[1]:
        if st.button("Reset Form", width="stretch"):
            _reset_form()
            st.rerun()

    user_inputs = {}
    for group_name, symptom_codes in SYMPTOM_GROUPS.items():
        with st.expander(group_name, expanded=True):
            cols = st.columns(2)
            for index, code in enumerate(symptom_codes):
                with cols[index % 2]:
                    user_inputs[code] = st.slider(
                        label=f"{code} - {SYMPTOMS[code]}",
                        min_value=0.0,
                        max_value=1.0,
                        value=st.session_state.get(f"slider_{code}", 0.0),
                        step=0.1,
                        key=f"slider_{code}",
                        help="0.0 = tidak ada gejala, 1.0 = sangat yakin",
                    )

    selected_symptoms = sum(1 for value in user_inputs.values() if value > 0)
    st.write(f"Gejala aktif: **{selected_symptoms}** dari **{len(SYMPTOMS)}**")

    centered = st.columns([1, 2, 1])
    with centered[1]:
        diagnose_clicked = st.button("Diagnosa Sekarang", type="primary", width="stretch")

    if diagnose_clicked:
        if selected_symptoms == 0:
            st.warning("Pilih minimal satu gejala sebelum menjalankan diagnosis.")
        else:
            results = forward_chaining(user_inputs)
            st.session_state["last_results"] = results
            st.session_state["last_inputs"] = user_inputs.copy()
            st.session_state["diagnosis_history"].insert(
                0,
                {
                    "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Penyakit Utama": next(iter(results.values()))["name"],
                    "Persentase": next(iter(results.values()))["percentage"],
                },
            )

    if st.session_state["last_results"] and st.session_state["last_inputs"]:
        _render_results(st.session_state["last_results"], st.session_state["last_inputs"])

    if st.session_state["diagnosis_history"]:
        st.subheader("Riwayat Diagnosis Sesi")
        st.dataframe(pd.DataFrame(st.session_state["diagnosis_history"]), width="stretch")


def _render_results(results: dict[str, dict], user_inputs: dict[str, float]) -> None:
    st.divider()
    st.header("Hasil Diagnosis")

    top_result = next(iter(results.values()))
    metrics = st.columns(4)
    metrics[0].metric("Penyakit Utama", top_result["name"])
    metrics[1].metric("Kode", top_result["code"])
    metrics[2].metric("Certainty Factor", f"{top_result['cf_combined']:.4f}")
    metrics[3].metric("Tingkat Kepercayaan", f"{top_result['percentage']:.2f}%")

    st.success(f"Interpretasi hasil utama: **{top_result['label']}**")

    fig = go.Figure(
        go.Bar(
            x=[value["percentage"] for value in results.values()],
            y=[value["name"] for value in results.values()],
            orientation="h",
            marker_color=[
                "#C62828" if value["cf_combined"] >= 0.7 else "#E65100" if value["cf_combined"] >= 0.4 else "#455A64"
                for value in results.values()
            ],
            text=[f"{value['percentage']}%" for value in results.values()],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Ranking Semua Penyakit",
        xaxis_title="Tingkat Kepercayaan (%)",
        yaxis_title="Penyakit",
        height=420,
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Ranking Penyakit")
    ranking_rows = build_ranking_rows(results)
    st.dataframe(pd.DataFrame(ranking_rows), width="stretch")

    st.subheader("Rekomendasi Penanganan")
    for recommendation in RECOMMENDATIONS.get(top_result["code"], []):
        st.write(f"- {recommendation}")

    st.subheader("Detail Perhitungan CF")
    detail_rows = build_detail_rows(results)
    if detail_rows:
        st.dataframe(pd.DataFrame(detail_rows), width="stretch")
    else:
        st.info("Tidak ada detail perhitungan karena tidak ada gejala yang cocok.")

    excel_bytes = generate_excel_report(results, user_inputs)
    st.download_button(
        label="Download Laporan Excel",
        data=excel_bytes,
        file_name="Laporan_Diagnosis_Cabai.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch",
    )
