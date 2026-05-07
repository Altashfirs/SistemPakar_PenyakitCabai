"""Disease information page."""

import streamlit as st

from data.diseases import DISEASE_DETAILS
from data.recommendations import RECOMMENDATIONS


def render_info_penyakit() -> None:
    st.title("Info Penyakit")
    st.caption("Ringkasan penyakit utama yang dicakup dalam basis pengetahuan SiPakar Cabai")

    for code, detail in DISEASE_DETAILS.items():
        with st.expander(f"{code} - {detail['name']}", expanded=False):
            st.write(f"**Penyebab:** {detail['cause']}")
            st.write(f"**Deskripsi:** {detail['summary']}")
            st.write(f"**Referensi:** {detail['reference']}")
            st.write("**Rekomendasi:**")
            for recommendation in RECOMMENDATIONS.get(code, []):
                st.write(f"- {recommendation}")
