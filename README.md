# Jakarta Public Transportation Dashboard 2026

Proyek ini adalah portofolio Data Analyst untuk menganalisis data pergerakan, pendapatan, dan efisiensi operasional dari transportasi publik di DKI Jakarta (**TransJakarta, MRT Jakarta, dan LRT Jakarta**) menggunakan data simulasi tahun 2026.

## Fitur Utama
1. **Generator Data Otomatis**: Menghasilkan data simulasi yang realistis, menirukan pola jam sibuk (*peak hours*), akhir pekan, kapasitas penumpang, serta status keterlambatan operasional.
2. **Data Cleaning & ETL**: Script ETL sederhana untuk membersihkan dataset mentah dan mengekstrak fitur waktu (hari, jam sibuk, bulan) menggunakan Pandas.
3. **Interactive Dashboard**: Visualisasi interaktif menggunakan Streamlit dan Plotly untuk memantau KPI utama, pola harian, jam sibuk, status operasional, serta rute terpopuler.

## Tech Stack
* **Python** (Pandas, NumPy)
* **Streamlit** (Web Dashboard Framework)
* **Plotly** (Interactive Data Visualization)

## Cara Menjalankan Project

### 1. Prasyarat
Pastikan Anda sudah menginstal Python (>= 3.9) dan menginstal dependencies berikut:
```bash
pip install pandas numpy streamlit plotly
```

### 2. Langkah-langkah
1. **Generate Data Mentah**
   Jalankan script untuk membuat dataset transportasi buatan di folder `data/`:
   ```bash
   python generate_data.py
   ```
2. **Proses & Bersihkan Data**
   Lakukan ETL / pemrosesan data untuk menambahkan kolom kategori jam sibuk, hari dalam bahasa Indonesia, dan lainnya:
   ```bash
   python process_data.py
   ```
3. **Jalankan Dashboard Streamlit**
   Luncurkan dashboard visualisasi interaktif di browser lokal Anda:
   ```bash
   streamlit run app.py
   ```

## Struktur File
* `generate_data.py`: Script untuk generate data simulasi.
* `process_data.py`: Script untuk membersihkan dan menyiapkan data.
* `app.py`: Script aplikasi dashboard Streamlit.
* `data/`: Folder berisi dataset CSV.

