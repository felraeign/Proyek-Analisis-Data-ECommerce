# Proyek Analisis Data: E-Commerce Public Dataset

Proyek analisis data ini menggunakan dataset publik E-Commerce (Brasil) untuk menyajikan *dashboard* analitik interaktif tingkat eksekutif. Fokus utama dari proyek ini adalah menjawab tiga pilar analisis bisnis strategis:
1. **Performa Kategori Produk:** Evaluasi kategori produk terlaris dan terendah sebagai dasar alokasi anggaran pemasaran.
2. **Preferensi Pembayaran:** Analisis volume transaksi dan rata-rata nilai pesanan untuk optimalisasi payment gateway.
3. **Kinerja Logistik:** Evaluasi dampak keterlambatan pengiriman terhadap kepuasan pelanggan sebagai dasar evaluasi mitra logistik.

## Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

```

## Setup Environment - Shell/Terminal

```bash
pip install -r requirements.txt

```

## Run Streamlit App

```bash
streamlit run dashboard/dashboard.py

```

## Struktur Direktori Proyek

Pastikan susunan folder dan file Anda di GitHub sama persis dengan struktur berikut:

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
