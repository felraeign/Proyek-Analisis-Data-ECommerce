import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Executive Performance Dashboard", layout="wide")

# --- 2. DATA LOADING (CACHED) ---
@st.cache_data
def load_data():
    orders = pd.read_csv("data/orders_dataset.csv")
    items = pd.read_csv("data/order_items_dataset.csv")
    payments = pd.read_csv("data/order_payments_dataset.csv")
    reviews = pd.read_csv("data/order_reviews_dataset.csv")
    products = pd.read_csv("data/products_dataset.csv")
    translation = pd.read_csv("data/product_category_name_translation.csv")
    customers = pd.read_csv("data/customers_dataset.csv")

    # Datetime conversion 
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce')
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'], errors='coerce')
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'], errors='coerce')

    # Menggabungkan data pesanan dengan pelanggan untuk mendapatkan informasi lokasi (State)
    orders = pd.merge(orders, customers[['customer_id', 'customer_state']], on='customer_id', how='left')

    return orders, items, payments, reviews, products, translation, customers

orders, items, payments, reviews, products, translation, customers = load_data()

# --- 3. SIDEBAR: FITUR INTERAKTIF (FILTER TANGGAL & LOKASI) ---
st.sidebar.markdown("<h2 style='text-align: center; color: #1f77b4;'>Business Analytics</h2>", unsafe_allow_html=True)
st.sidebar.divider()

st.sidebar.subheader("Filter Interaktif")

min_date = orders['order_purchase_timestamp'].min().date()
max_date = orders['order_purchase_timestamp'].max().date()

# A. Filter Tanggal 
default_start = datetime.date(2017, 10, 1)
default_end = datetime.date(2017, 12, 31)

start_date, end_date = st.sidebar.date_input(
    label="Rentang Waktu Transaksi",
    value=(default_start, default_end),
    min_value=min_date,
    max_value=max_date
)

# B. Filter Lokasi (Multiselect Negara Bagian)
all_states = sorted(orders['customer_state'].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    label="Pilih Lokasi (Negara Bagian)",
    options=all_states,
    default=[] 
)

# Menerapkan Filter pada Dataframe Utama
if not selected_states:
    filtered_orders = orders[(orders['order_purchase_timestamp'].dt.date >= start_date) & 
                             (orders['order_purchase_timestamp'].dt.date <= end_date)]
    state_text = "Semua Lokasi"
else:
    filtered_orders = orders[(orders['order_purchase_timestamp'].dt.date >= start_date) & 
                             (orders['order_purchase_timestamp'].dt.date <= end_date) &
                             (orders['customer_state'].isin(selected_states))]
    state_text = ", ".join(selected_states)

# Kalkulasi KPI Global berdasarkan Filter
filtered_payments = pd.merge(payments, filtered_orders[['order_id']], on='order_id', how='inner')
total_revenue = filtered_payments['payment_value'].sum()
total_orders = filtered_orders['order_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

# Format Angka KPI untuk Eksekutif (Million / K)
if total_revenue >= 1000000:
    rev_str = f"R$ {total_revenue/1000000:,.2f}M"
elif total_revenue >= 1000:
    rev_str = f"R$ {total_revenue/1000:,.2f}K"
else:
    rev_str = f"R$ {total_revenue:,.0f}"

if total_orders >= 1000:
    order_str = f"{total_orders/1000:,.1f}K"
else:
    order_str = f"{total_orders:,}"

# C. Dynamic Executive Summary (Komprehensif Keseluruhan Tab)
st.sidebar.markdown("---")
st.sidebar.markdown("### Executive Summary")

if not filtered_orders.empty:
    # 1. Kalkulasi Top Kategori dan Delay Rate
    delivered_orders = filtered_orders[filtered_orders['order_status'] == 'delivered'].copy()
    if not delivered_orders.empty:
        # Kategori
        temp_items = pd.merge(items, delivered_orders[['order_id']], on='order_id', how='inner')
        temp_items = pd.merge(temp_items, products, on='product_id', how='left')
        temp_items = pd.merge(temp_items, translation, on='product_category_name', how='left')
        temp_items['category'] = temp_items['product_category_name_english'].fillna(temp_items['product_category_name'])
        temp_items['revenue'] = temp_items['price'] + temp_items['freight_value']
        top_cat = temp_items.groupby('category')['revenue'].sum().idxmax()
        
        # Logistik
        delivered_orders['delivery_delay'] = (delivered_orders['order_delivered_customer_date'] - delivered_orders['order_estimated_delivery_date']).dt.days
        delayed_count = (delivered_orders['delivery_delay'] > 0).sum()
        delay_rate = (delayed_count / len(delivered_orders)) * 100
    else:
        top_cat = "N/A"
        delay_rate = 0.0

    # 2. Kalkulasi Top Metode Pembayaran
    if not filtered_payments.empty:
        top_payment = filtered_payments['payment_type'].value_counts().index[0].replace('_', ' ').title()
    else:
        top_payment = "N/A"

    # 3. Menampilkan Summary
    st.sidebar.info(
        f"**Ringkasan Performa ({start_date.strftime('%Y')} - {end_date.strftime('%Y')}):**\n\n"
        f"• **Volume & Nilai:** Terdapat {total_orders:,} pesanan dengan total pendapatan {rev_str}.\n\n"
        f"• **Kategori Utama:** Pendapatan tertinggi disumbang oleh produk *{top_cat}*.\n\n"
        f"• **Pembayaran:** Metode *{top_payment}* mendominasi pilihan transaksi pelanggan.\n\n"
        f"• **Logistik:** Tingkat keterlambatan pengiriman barang berada di persentase {delay_rate:.1f}%."
    )
else:
    st.sidebar.warning("Tidak ada data transaksi pada rentang filter yang dipilih.")


# --- 4. MAIN DASHBOARD UI ---
st.title("Executive Performance Dashboard")
st.caption(f"Rentang Waktu: {start_date} hingga {end_date} | Lokasi: {state_text}")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div style="background-color: #1e2130; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
            <p style="margin:0; font-size:16px; color:#aeb6bf; font-weight:600;">Total Revenue</p>
            <h2 style="margin:0; font-size:32px; color:#ffffff;">{rev_str}</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="background-color: #1e2130; padding: 20px; border-radius: 10px; border-left: 5px solid #2ca02c; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
            <p style="margin:0; font-size:16px; color:#aeb6bf; font-weight:600;">Total Orders</p>
            <h2 style="margin:0; font-size:32px; color:#ffffff;">{order_str}</h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="background-color: #1e2130; padding: 20px; border-radius: 10px; border-left: 5px solid #ff7f0e; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
            <p style="margin:0; font-size:16px; color:#aeb6bf; font-weight:600;">Average Order Value (AOV)</p>
            <h2 style="margin:0; font-size:32px; color:#ffffff;">R$ {avg_order_value:,.0f}</h2>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("") 

# --- 5. TABS CONTENT ---
tab1, tab2, tab3 = st.tabs(["Performa Kategori Produk", "Preferensi Pembayaran", "Kinerja Logistik"])

# ================= TAB 1: KATEGORI PRODUK =================
with tab1:
    st.subheader("Performa Pendapatan Kategori Produk Tertinggi vs Terendah")
    
    q2_df = pd.merge(items, delivered_orders[['order_id']], on='order_id', how='inner')
    if not q2_df.empty:
        q2_df = pd.merge(q2_df, products, on='product_id', how='left')
        q2_df = pd.merge(q2_df, translation, on='product_category_name', how='left')
        q2_df['category'] = q2_df['product_category_name_english'].fillna(q2_df['product_category_name'])
        
        q2_df['revenue'] = q2_df['price'] + q2_df['freight_value']
        cat_sales = q2_df.groupby('category')['revenue'].sum().reset_index()
        
        col1, col2 = st.columns(2)
        
        # Grafik Top 5
        top_5_cat = cat_sales.sort_values(by='revenue', ascending=True).tail(5)
        text_top = top_5_cat['revenue'].apply(lambda x: f"{x:,.0f} BRL")
        
        fig_top5 = px.bar(top_5_cat, x='revenue', y='category', orientation='h', text=text_top, title="5 Kategori Produk Terlaris")
        fig_top5.update_traces(marker_color='#1f77b4', textposition='auto')
        fig_top5.update_layout(xaxis_title="Total Revenue (BRL)", yaxis_title="", plot_bgcolor='rgba(0,0,0,0)', margin=dict(r=50))
        col1.plotly_chart(fig_top5, use_container_width=True)
        
        # Grafik Bottom 5
        bottom_5_cat = cat_sales.sort_values(by='revenue', ascending=False).tail(5) 
        text_bot = bottom_5_cat['revenue'].apply(lambda x: f"{x:,.0f} BRL")
        
        fig_bot5 = px.bar(bottom_5_cat, x='revenue', y='category', orientation='h', text=text_bot, title="5 Kategori Produk Paling Sepi")
        fig_bot5.update_traces(marker_color='#1f77b4', textposition='auto')
        fig_bot5.update_layout(yaxis={'side': 'right'}, xaxis_title="Total Revenue (BRL)", yaxis_title="", xaxis=dict(autorange="reversed"), plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=50))
        col2.plotly_chart(fig_bot5, use_container_width=True)
    else:
        st.warning("Tidak ada data transaksi pada rentang tanggal & lokasi yang dipilih.")
    
    st.info(
        "**Strategic Insight & Business Action:**\n\n"
        "• **Optimalisasi Rantai Pasok:** Amankan ketersediaan stok (*inventory level*) pada 5 kategori terlaris (*cash cow*) untuk mencegah *lost sales* akibat kehabisan barang.\n\n"
        "• **Likuidasi Inventaris:** Terapkan strategi *product bundling* atau *clearance sale* (diskon cuci gudang) pada 5 kategori terbawah guna mencairkan aset yang tertahan dan memangkas biaya simpan di gudang (*holding cost*)."
    )

# ================= TAB 2: METODE PEMBAYARAN =================
with tab2:
    st.subheader("Analisis Volume dan Nilai Transaksi per Metode Pembayaran")
    
    q3_df = filtered_payments[filtered_payments['payment_type'] != 'not_defined'].copy()
    if not q3_df.empty:
        q3_df['payment_type'] = q3_df['payment_type'].str.replace('_', ' ').str.title()
        pay_summary = q3_df.groupby('payment_type').agg(total_transactions=('order_id', 'count'), avg_payment_value=('payment_value', 'mean')).reset_index()
        pay_summary = pay_summary.sort_values('total_transactions', ascending=False)
        
        col1, col2 = st.columns(2)
        fig_pay_vol = px.bar(pay_summary, x='payment_type', y='total_transactions', text_auto='.2s', title="Total Transaksi per Metode")
        fig_pay_vol.update_traces(marker_color='#1f77b4') 
        fig_pay_vol.update_layout(xaxis_title="Metode Pembayaran", yaxis_title="Jumlah Transaksi", plot_bgcolor='rgba(0,0,0,0)')
        col1.plotly_chart(fig_pay_vol, use_container_width=True)
        
        fig_pay_aov = px.bar(pay_summary.sort_values('avg_payment_value', ascending=False), x='payment_type', y='avg_payment_value', text_auto='.2f', title="Rata-rata Nilai Transaksi per Metode")
        fig_pay_aov.update_traces(marker_color='#1f77b4') 
        fig_pay_aov.update_layout(xaxis_title="Metode Pembayaran", yaxis_title="Rata-rata Nilai (BRL)", plot_bgcolor='rgba(0,0,0,0)')
        col2.plotly_chart(fig_pay_aov, use_container_width=True)
    else:
        st.warning("Tidak ada data pembayaran pada rentang tanggal & lokasi yang dipilih.")
        
    st.info(
        "**Strategic Insight & Business Action:**\n\n"
        "• **Efisiensi Biaya Transaksi:** Manfaatkan dominasi volume pada metode pembayaran utama sebagai daya tawar untuk menegosiasikan penurunan biaya admin (MDR - *Merchant Discount Rate*) dengan pihak bank atau penyedia *payment gateway*.\n\n"
        "• **Insentif Perilaku:** Rancang kampanye *cashback* atau poin loyalitas untuk metode pembayaran alternatif yang memiliki biaya MDR lebih rendah bagi perusahaan, guna mengalihkan kebiasaan bayar pelanggan."
    )

# ================= TAB 3: KINERJA LOGISTIK =================
with tab3:
    st.subheader("Dampak Keterlambatan Pengiriman terhadap Kepuasan Pelanggan")
    
    if not delivered_orders.empty:
        delivered_orders['status_pengiriman'] = delivered_orders['delivery_delay'].apply(lambda x: 'Terlambat' if x > 0 else 'Tepat Waktu')
        
        q1_df = pd.merge(delivered_orders, reviews[['order_id', 'review_score']], on='order_id', how='left')
        
        delay_summary = q1_df.groupby('status_pengiriman').agg(
            review_score=('review_score', 'mean'),
            total_orders=('order_id', 'count')
        ).reset_index()
        
        if not delay_summary.empty:
            col1, col2 = st.columns([1.2, 0.8])
            delay_summary['label_text'] = delay_summary.apply(lambda x: f"{x['review_score']:.2f}<br>(Vol: {x['total_orders']:,})", axis=1)
            
            fig_delay = px.bar(delay_summary, x='status_pengiriman', y='review_score', text='label_text', title="Rata-rata Skor Ulasan: Tepat Waktu vs Terlambat")
            fig_delay.update_traces(marker_color='#1f77b4', textposition='inside', textfont=dict(color='white'))
            fig_delay.update_layout(yaxis_range=[0, 5], xaxis_title="Status Pengiriman", yaxis_title="Rata-rata Skor (1-5)", plot_bgcolor='rgba(0,0,0,0)')
            col1.plotly_chart(fig_delay, use_container_width=True)
            
            with col2:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.info(
        "**Strategic Insight & Business Action:**\n\n"
        "• **Manajemen Ekspektasi (*Dynamic ETA*):** Kalibrasi ulang algoritma estimasi pengiriman di aplikasi dengan menambahkan *buffer* waktu 1-2 hari agar metrik keterlambatan menurun secara sistem.\n\n"
        "• **Service Recovery Strategy:** Implementasikan sistem otomatis yang mengirimkan permohonan maaf beserta *voucher* kompensasi (misal: gratis ongkir) tepat saat resi terdeteksi terlambat, guna meredam kekecewaan sebelum pelanggan memberikan ulasan bintang 1."
    )
        else:
            st.warning("Data ulasan tidak mencukupi pada rentang tanggal & lokasi terpilih.")
    else:
        st.warning("Tidak ada pesanan terkirim pada rentang tanggal & lokasi terpilih.")