"""Main Streamlit app for SiPakar Cabai."""

import streamlit as st

from views.diagnosis import render_diagnosis
from views.home import render_home
from views.info_penyakit import render_info_penyakit


st.set_page_config(
    page_title="SiPakar Cabai",
    page_icon="🌶️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


def render_about() -> None:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.title("🤖 Tentang Metode")
    st.markdown(
        """
        ### 🔍 Forward Chaining
        Metode penalaran yang bekerja dari **fakta atau gejala** yang dipilih pengguna dan merangkai aturan untuk mencapai kesimpulan/hipotesis penyakit yang paling sesuai.

        ### 📊 Certainty Factor
        Metode yang digunakan untuk merepresentasikan dan mengakumulasi **tingkat keyakinan** (baik dari pakar maupun pengguna) terhadap suatu gejala.
        
        **Formula utama yang digunakan:**
        - `CF(H,E) = CF_Pakar x CF_User`
        - `CF final = 1 - PRODUCT(1 - CFi)` (untuk semua *evidence* positif).
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.warning(
        "⚠️ **Disclaimer:** Aplikasi ini adalah alat bantu diagnosis awal berbasis pengetahuan. Hasil komputasi tidak menggantikan pemeriksaan fisik langsung oleh pakar pertanian atau otoritas terkait."
    )


def main() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="margin-bottom: 0;">🌶️ SiPakar</h1>
                <p style="color: gray; font-size: 0.9em; margin-top: 0;">Pakar Cabai Cerdas</p>
            </div>
            <hr>
            """,
            unsafe_allow_html=True
        )
        st.subheader("📌 Navigasi")
        menu = st.radio(
            "Pilih halaman",
            ["🏠 Home", "🩺 Diagnosis", "📚 Info Penyakit", "🤖 Tentang Metode"],
            label_visibility="collapsed",
        )
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.caption("Versi 1.0.0")
        st.caption("© 2026 SiPakar Cabai")

    if menu == "🏠 Home":
        render_home()
    elif menu == "🩺 Diagnosis":
        render_diagnosis()
    elif menu == "📚 Info Penyakit":
        render_info_penyakit()
    else:
        render_about()


if __name__ == "__main__":
    main()
