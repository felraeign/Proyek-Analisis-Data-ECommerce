# E-Commerce Executive Analytics Dashboard 

Proyek analisis data ini menggunakan dataset publik E-Commerce (Brasil) untuk menyajikan *dashboard* analitik interaktif tingkat eksekutif. Fokus utama dari proyek ini adalah menjawab tiga pilar analisis bisnis strategis:
1. **Performa Kategori Produk (Q4 2017):** Evaluasi kategori produk terlaris (*Cash Cows*) dan produk dengan performa terendah (*Underperformers*).
2. **Preferensi Pembayaran (2018):** Analisis volume transaksi dan *Average Order Value* (AOV) berdasarkan metode pembayaran.
3. **Kinerja Logistik (São Paulo, 2018):** Evaluasi dampak keterlambatan *Service Level Agreement* (SLA) pengiriman terhadap *Customer Satisfaction Score* (CSAT).


## Struktur Direktori Proyek

Pastikan susunan folder dan file Anda di GitHub sama persis dengan struktur berikut agar path dataset terbaca dengan benar oleh program:

```text
Proyek_Analisis_Data/
│
├── dashboard/
│   └── dashboard.py
├── data/
│   ├── customers_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   └── products_dataset.csv
├── notebook.ipynb
├── requirements.txt
├── url.txt
└── README.md


```

---

## Cara Menjalankan Proyek

### 1. Instalasi Dependensi

Buka terminal atau Command Prompt pada direktori proyek Anda, lalu jalankan perintah berikut untuk menginstal seluruh *library* Python yang dibutuhkan (Pandas, Streamlit, dan Plotly):

```bash
pip install -r requirements.txt

```

*(Atau jika menggunakan Windows Python Launcher: `py -m pip install -r requirements.txt`)*

### 2. Menjalankan Dashboard Streamlit

Setelah proses instalasi selesai, jalankan *server* Streamlit dengan mengarahkan eksekusi ke dalam folder `dashboard`:

```bash
py -m streamlit run dashboard/dashboard.py

```

*(Atau menggunakan perintah Windows: `py -m streamlit run dashboard/dashboard.py`)*

*Dashboard* interaktif akan terbuka secara otomatis di *browser* utama Anda (biasanya pada alamat `http://localhost:8501`).
