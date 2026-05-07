"""Home page renderer."""

import streamlit as st


def render_home() -> None:
    st.title("SiPakar Cabai")
    st.caption("Sistem Pakar Diagnosa Penyakit Tanaman Cabai berbasis Forward Chaining dan Certainty Factor")

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Penyakit", "7")
    col2.metric("Jumlah Gejala", "25")
    col3.metric("Output", "Excel .xlsx")

    st.markdown(
        """
        Aplikasi ini membantu pengguna melakukan diagnosis awal penyakit tanaman cabai berdasarkan gejala yang diamati.

        **Fitur utama**
        - Input tingkat keyakinan untuk 25 gejala
        - Perhitungan CF otomatis untuk 7 penyakit utama
        - Ranking penyakit dan interpretasi tingkat keyakinan
        - Rekomendasi penanganan
        - Export hasil diagnosis ke Excel
        """
    )

    st.info(
        "Gunakan menu `Diagnosis` untuk mulai mengisi gejala. Hasil bersifat pendukung keputusan dan sebaiknya divalidasi dengan penyuluh atau pakar pertanian."
    )
