"""Disease information page."""

import streamlit as st

from data.diseases import DISEASE_DETAILS
from data.recommendations import RECOMMENDATIONS


def render_info_penyakit() -> None:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.title("📚 Info Penyakit")
    st.caption("Edukasi dan ringkasan penyakit utama pada basis pengetahuan SiPakar Cabai")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    for code, detail in DISEASE_DETAILS.items():
        with st.expander(f"🌿 {code} - {detail['name']}", expanded=False):
            st.markdown(f"**🔬 Penyebab:** {detail['cause']}")
            st.markdown(f"**📝 Deskripsi:** {detail['summary']}")
            st.markdown(f"**📖 Referensi:** {detail['reference']}")
            st.markdown("**💡 Rekomendasi Penanganan:**")
            for recommendation in RECOMMENDATIONS.get(code, []):
                st.markdown(f"- {recommendation}")
