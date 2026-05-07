# SiPakar Cabai Web

Aplikasi web sistem pakar untuk diagnosis penyakit tanaman cabai menggunakan metode Forward Chaining dan Certainty Factor.

## Menjalankan Proyek

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Menjalankan E2E Test

```bash
pip install -r requirements-dev.txt
pytest tests/e2e -q
```

## Dataset Test Diagnosis

Dataset kasus uji diagnosis ada di `tests/datasets/diagnosis_cases.json`.
Setiap case menyimpan gejala input, penyakit yang diharapkan, label interpretasi, dan batas minimum CF untuk validasi otomatis.

Dataset tambahan:
- `tests/datasets/academic_reference_cases.json` untuk validasi pola gejala referensi dari PRD/jurnal
- `tests/datasets/diagnosis_edge_cases.json` untuk kasus ambigu, overlap, dan confidence rendah

Untuk menjalankan seluruh test termasuk dataset:

```bash
pytest -q
```

## Fitur Utama

- Input 25 gejala dengan nilai keyakinan pengguna
- Diagnosis 7 penyakit utama tanaman cabai
- Ranking semua penyakit berdasarkan Certainty Factor
- Detail perhitungan CF yang transparan
- Rekomendasi penanganan
- Export laporan diagnosis ke Excel
