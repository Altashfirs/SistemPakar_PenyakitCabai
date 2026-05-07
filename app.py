"""Main Streamlit app for SiPakar Cabai."""

import streamlit as st

from pages.diagnosis import render_diagnosis
from pages.home import render_home
from pages.info_penyakit import render_info_penyakit


st.set_page_config(
    page_title="SiPakar Cabai",
    page_icon="🌶️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_about() -> None:
    st.title("Tentang Metode")
    st.markdown(
        """
        **Forward Chaining** bekerja dari gejala yang dipilih pengguna menuju hipotesis penyakit yang paling sesuai.

        **Certainty Factor** dipakai untuk merepresentasikan tingkat keyakinan pakar dan pengguna pada setiap gejala.

        Formula utama yang digunakan:

        `CF(H,E) = CF_Pakar x CF_User`

        `CF final = 1 - PRODUCT(1 - CFi)` untuk semua evidence positif.
        """
    )

    st.warning(
        "Aplikasi ini adalah alat bantu diagnosis awal berbasis pengetahuan. Hasil tidak menggantikan pemeriksaan langsung oleh pakar pertanian."
    )


def main() -> None:
    with st.sidebar:
        st.title("Navigasi")
        menu = st.radio(
            "Pilih halaman",
            ["Home", "Diagnosis", "Info Penyakit", "Tentang Metode"],
            label_visibility="collapsed",
        )

    if menu == "Home":
        render_home()
    elif menu == "Diagnosis":
        render_diagnosis()
    elif menu == "Info Penyakit":
        render_info_penyakit()
    else:
        render_about()


if __name__ == "__main__":
    main()
