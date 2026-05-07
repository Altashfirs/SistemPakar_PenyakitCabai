"""Home page renderer."""

import streamlit as st


def render_home() -> None:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.title("🌶️ SiPakar Cabai")
    st.markdown("### Sistem Pakar Diagnosa Penyakit Tanaman Cabai")
    st.caption("Berbasis *Forward Chaining* dan *Certainty Factor*")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="custom-card" style="text-align: center;">', unsafe_allow_html=True)
        st.metric("Jumlah Penyakit", "7", "Terdokumentasi")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="custom-card" style="text-align: center;">', unsafe_allow_html=True)
        st.metric("Jumlah Gejala", "25", "Identifiable")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="custom-card" style="text-align: center;">', unsafe_allow_html=True)
        st.metric("Output Sistem", "Excel .xlsx", "Detail")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown(
        """
        Aplikasi ini didesain secara spesifik untuk membantu petani dan praktisi pertanian dalam melakukan **diagnosis awal penyakit tanaman cabai** secara mandiri berdasarkan gejala fisik yang diamati pada tanaman.

        #### ✨ Fitur Utama
        * 🔍 **Input Presisi**: Masukkan tingkat keyakinan Anda untuk 25 gejala yang tersedia.
        * ⚙️ **Analisis Otomatis**: Perhitungan Certainty Factor cerdas terhadap 7 penyakit utama.
        * 📊 **Ranking Akurat**: Dapatkan prioritas penyakit berdasarkan tingkat kemungkinan tertinggi.
        * 💡 **Solusi Praktis**: Rekomendasi penanganan komprehensif.
        * 📁 **Laporan Detil**: Export hasil analisis lengkap ke dalam format Excel.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.info(
        "💡 **Mulai Diagnosis:** Gunakan menu navigasi di sebelah kiri untuk masuk ke halaman `Diagnosis`. "
        "Perlu diingat bahwa hasil diagnosis sistem ini bersifat sebagai **pendukung keputusan** dan disarankan untuk divalidasi dengan penyuluh pertanian setempat."
    )
