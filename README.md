# SiPakar Cabai Web

`SiPakar Cabai Web` adalah aplikasi web sistem pakar untuk diagnosis penyakit tanaman cabai berbasis `Streamlit`. Sistem ini menggunakan pendekatan **Forward Chaining + Certainty Factor (CF)** secara eksplisit:

- **Forward Chaining** dipakai untuk mengevaluasi rule `IF-THEN` dan menentukan kandidat penyakit.
- **Certainty Factor** dipakai untuk menghitung tingkat keyakinan diagnosis hanya pada kandidat yang lolos tahap forward chaining.

Proyek ini ditujukan untuk kebutuhan pembelajaran, demonstrasi, dan pengembangan sistem pakar pada domain pertanian, khususnya diagnosis awal 7 penyakit utama tanaman cabai.

## Fitur

- Input 25 gejala dengan slider nilai keyakinan pengguna `0.0 - 1.0`
- Diagnosis 7 penyakit utama tanaman cabai
- Rule base forward chaining yang eksplisit dan transparan
- Ranking penyakit berdasarkan nilai Certainty Factor
- Tabel rule forward chaining yang terpicu
- Detail perhitungan `CF(H,E)` per gejala
- Rekomendasi penanganan penyakit utama
- Export laporan diagnosis ke Excel (`.xlsx`)
- Riwayat diagnosis dalam session
- Halaman edukasi penyakit dan penjelasan metode

## Metode Inferensi

### 1. Forward Chaining

Inferensi dimulai dari fakta berupa gejala yang dipilih pengguna. Sistem kemudian mengevaluasi rule `IF-THEN` pada `data/rules.py`.

Contoh konsep rule:

```text
IF gejala inti penyakit terpenuhi
THEN penyakit menjadi kandidat diagnosis
```

Implementasi rule dibagi menjadi dua jenis:

- **Rule inti**: membutuhkan minimal dua gejala khas untuk mengaktifkan kandidat penyakit.
- **Rule sinyal kuat**: digunakan untuk gejala yang sangat khas dan cukup kuat memicu kandidat sendiri.

Output tahap ini adalah daftar **penyakit kandidat** beserta rule yang berhasil `fire`.

### 2. Certainty Factor

Setelah kandidat penyakit didapat, sistem menghitung nilai keyakinan setiap penyakit dengan formula:

```text
CF(H,E) = CF_Pakar x CF_User
```

Untuk menggabungkan beberapa evidence positif:

```text
CF final = 1 - PRODUCT(1 - CFi)
```

Interpretasi nilai CF:

- `0.00 - 0.19`: Tidak Ada
- `0.20 - 0.39`: Sangat Lemah
- `0.40 - 0.59`: Lemah
- `0.60 - 0.79`: Sedang
- `0.80 - 0.89`: Kuat
- `0.90 - 1.00`: Sangat Kuat

## Penyakit yang Dicakup

- `P1` Antraknosa (Busuk Buah)
- `P2` Layu Fusarium
- `P3` Bercak Daun Cercospora
- `P4` Virus Kuning (Gemini Virus)
- `P5` Busuk Phytophthora
- `P6` Embun Tepung
- `P7` Bercak Alternaria

## Struktur Proyek

```text
Cabai/
├── app.py
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── assets/
│   └── style.css
├── data/
│   ├── __init__.py
│   ├── diseases.py
│   ├── knowledge_base.py
│   ├── recommendations.py
│   └── rules.py
├── engine/
│   ├── __init__.py
│   ├── cf_engine.py
│   └── excel_generator.py
├── views/
│   ├── __init__.py
│   ├── diagnosis.py
│   ├── home.py
│   └── info_penyakit.py
└── tests/
    ├── datasets/
    ├── e2e/
    └── unit/
```

## Komponen Utama

### `app.py`

Entry point aplikasi Streamlit. Mengatur:

- konfigurasi halaman
- styling global dari `assets/style.css`
- navigasi sidebar
- halaman `Home`, `Diagnosis`, `Info Penyakit`, dan `Tentang Metode`

### `data/knowledge_base.py`

Berisi basis pengetahuan utama:

- daftar penyakit
- daftar gejala
- pengelompokan gejala untuk UI
- bobot `CF pakar` per gejala dan penyakit

### `data/rules.py`

Berisi rule `IF-THEN` eksplisit untuk forward chaining. Setiap rule memiliki:

- `rule_id`
- `disease_code`
- nama rule
- daftar `antecedents`
- `minimum_matches`

### `engine/cf_engine.py`

Berisi logika inferensi inti:

- `calc_cf_individual()`
- `combine_cf()`
- `evaluate_rule()`
- `fire_rules()`
- `forward_chaining()`
- helper untuk membentuk tabel ranking, detail CF, dan rule fired

### `engine/excel_generator.py`

Membuat laporan diagnosis dalam format Excel dengan sheet:

- `Ringkasan`
- `Ranking`
- `Input Gejala`
- `Detail CF`
- `Rule FC`

### `views/diagnosis.py`

Halaman utama diagnosis yang menangani:

- input gejala pengguna
- reset form
- eksekusi diagnosis
- tampilan ranking
- tampilan rule forward chaining yang terpenuhi
- tampilan detail perhitungan CF
- download laporan Excel

## Menjalankan Proyek

### 1. Install dependensi

```bash
pip install -r requirements.txt
```

### 2. Jalankan aplikasi

```bash
streamlit run app.py
```

### 3. Buka di browser

```text
http://localhost:8501
```

## Testing

Project ini memiliki unit test, E2E test, dan dataset-based validation.

### Install dependensi test

```bash
pip install -r requirements-dev.txt
```

### Jalankan semua test

```bash
pytest -q
```

Status saat ini:

```text
38 passed
```

### Menjalankan E2E test saja

```bash
pytest tests/e2e -q
```

### Menjalankan unit test saja

```bash
pytest tests/unit -q
```

## Dataset Test

Terdapat beberapa dataset test untuk memvalidasi perilaku sistem.

### `tests/datasets/diagnosis_cases.json`

Dataset kasus diagnosis utama untuk memastikan setiap penyakit dapat muncul sebagai hasil teratas pada skenario representatif.

### `tests/datasets/academic_reference_cases.json`

Dataset validasi akademik berbasis pola gejala referensi dari PRD dan jurnal. Cocok untuk pembuktian bahwa rule dan hasil diagnosis sejalan dengan basis pengetahuan yang dirancang.

### `tests/datasets/diagnosis_edge_cases.json`

Dataset untuk kasus ambigu dan edge case, misalnya:

- input kosong
- overlap gejala antar penyakit
- evidence lemah
- kasus dengan lebih dari satu kandidat forward chaining

## Output Sistem

Setelah diagnosis dijalankan, aplikasi menghasilkan:

- penyakit utama
- kode penyakit
- nilai Certainty Factor
- persentase tingkat keyakinan
- ranking semua penyakit
- rule forward chaining yang terpicu
- detail `CF(H,E)`
- rekomendasi penanganan
- file laporan Excel

## Deployment

### Streamlit Community Cloud

Langkah deployment:

1. Push project ke GitHub
2. Buka `https://share.streamlit.io`
3. Login dengan akun GitHub
4. Pilih repository ini
5. Set `main file path` ke `app.py`
6. Klik `Deploy`

## Catatan Akademik

Secara implementasi, project ini **bukan hanya CF scoring**, tetapi benar-benar memisahkan dua tahap inferensi:

1. **Forward Chaining** untuk menentukan kandidat penyakit dari rule yang terpenuhi
2. **Certainty Factor** untuk menghitung tingkat keyakinan kandidat tersebut

Dengan struktur ini, penjelasan metode untuk laporan, presentasi, atau demonstrasi ke dosen menjadi lebih kuat dan lebih mudah dipertanggungjawabkan.

## Disclaimer

Sistem ini adalah alat bantu diagnosis awal berbasis pengetahuan. Hasil komputasi tidak menggantikan pemeriksaan langsung oleh pakar pertanian, penyuluh, atau otoritas terkait.
