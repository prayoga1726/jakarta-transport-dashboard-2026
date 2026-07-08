import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page config
st.set_page_config(
    page_title="Dashboard Transportasi Publik DKI Jakarta 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("📊 Dashboard Transportasi Publik DKI Jakarta 2026")
st.markdown("Analisis Kinerja Harian, Pendapatan, dan Utilisasi MRT, LRT, dan TransJakarta.")

# Check for processed data
file_path = 'data/transportasi_jakarta_2026_clean.csv'
if not os.path.exists(file_path):
    st.error("Data bersih belum ditemukan! Harap jalankan script `generate_data.py` dan `process_data.py` terlebih dahulu.")
else:
    # Load dataset
    @st.cache_data
    def load_data():
        df = pd.read_csv(file_path)
        df['tanggal'] = pd.to_datetime(df['tanggal'])
        return df

    df = load_data()

    # Sidebar Filter
    st.sidebar.header("Filter Analisis")
    
    # 1. Filter Mode Transportasi
    modes = df['mode_transportasi'].unique().tolist()
    selected_modes = st.sidebar.multiselect(
        "Pilih Mode Transportasi:",
        options=modes,
        default=modes
    )
    
    # Filter data berdasarkan mode
    df_filtered = df[df['mode_transportasi'].isin(selected_modes)]
    
    # 2. Filter Tanggal
    min_date = df['tanggal'].min().date()
    max_date = df['tanggal'].max().date()
    start_date, end_date = st.sidebar.date_input(
        "Rentang Waktu:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data berdasarkan tanggal
    df_filtered = df_filtered[
        (df_filtered['tanggal'].dt.date >= start_date) & 
        (df_filtered['tanggal'].dt.date <= end_date)
    ]

    # --- KPI METRICS ---
    st.markdown("### 📈 Key Performance Indicators (KPI)")
    col1, col2, col3, col4 = st.columns(4)
    
    total_passengers = df_filtered['jumlah_penumpang'].sum()
    total_revenue = df_filtered['total_pendapatan'].sum()
    avg_fare = df_filtered['tarif_rata_rata'].mean()
    delay_rate = (df_filtered['status_operasional'] != 'Normal').mean() * 100
    
    col1.metric("Total Penumpang", f"{total_passengers:,}")
    col2.metric("Total Pendapatan", f"Rp {total_revenue:,.0f}")
    col3.metric("Rata-rata Tarif", f"Rp {avg_fare:,.2f}")
    col4.metric("Rasio Keterlambatan/Gangguan", f"{delay_rate:.2f}%")

    # --- VISUALIZATIONS ---
    st.markdown("---")
    
    # Row 1: Tren & Pembagian Mode
    col_row1_1, col_row1_2 = st.columns([2, 1])
    
    with col_row1_1:
        st.markdown("#### Tren Penumpang Harian")
        daily_passengers = df_filtered.groupby(df_filtered['tanggal'].dt.date)['jumlah_penumpang'].sum().reset_index()
        fig_trend = px.line(
            daily_passengers,
            x='tanggal',
            y='jumlah_penumpang',
            title='Tren Jumlah Penumpang Harian',
            labels={'tanggal': 'Tanggal', 'jumlah_penumpang': 'Jumlah Penumpang'},
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_row1_2:
        st.markdown("#### Distribusi Penumpang per Mode")
        mode_share = df_filtered.groupby('mode_transportasi')['jumlah_penumpang'].sum().reset_index()
        fig_pie = px.pie(
            mode_share,
            values='jumlah_penumpang',
            names='mode_transportasi',
            title='Pangsa Penumpang per Mode',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Row 2: Jam Sibuk & Status Operasional
    col_row2_1, col_row2_2 = st.columns(2)
    
    with col_row2_1:
        st.markdown("#### Pola Penumpang berdasarkan Jam")
        hourly_passengers = df_filtered.groupby('jam')['jumlah_penumpang'].mean().reset_index()
        fig_hour = px.bar(
            hourly_passengers,
            x='jam',
            y='jumlah_penumpang',
            title='Rata-rata Penumpang per Jam',
            labels={'jam': 'Jam', 'jumlah_penumpang': 'Rata-rata Penumpang'},
            color_discrete_sequence=['#2ca02c']
        )
        st.plotly_chart(fig_hour, use_container_width=True)
        
    with col_row2_2:
        st.markdown("#### Status Operasional Perjalanan")
        status_counts = df_filtered['status_operasional'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Jumlah']
        fig_status = px.bar(
            status_counts,
            x='Status',
            y='Jumlah',
            title='Status Keberangkatan',
            color='Status',
            color_discrete_map={'Normal': '#2ca02c', 'Terlambat': '#ff7f0e', 'Gangguan': '#d62728'}
        )
        st.plotly_chart(fig_status, use_container_width=True)

    # Row 3: Rute Terpopuler
    st.markdown("---")
    st.markdown("#### Rute Paling Padat (Top 10 Rute)")
    route_traffic = df_filtered.groupby(['mode_transportasi', 'rute'])['jumlah_penumpang'].sum().reset_index()
    route_traffic = route_traffic.sort_values(by='jumlah_penumpang', ascending=False).head(10)
    
    fig_route = px.bar(
        route_traffic,
        y='rute',
        x='jumlah_penumpang',
        color='mode_transportasi',
        title='10 Rute dengan Total Penumpang Tertinggi',
        orientation='h',
        labels={'jumlah_penumpang': 'Total Penumpang', 'rute': 'Rute'},
        category_orders={"rute": route_traffic['rute'].tolist()}
    )
    st.plotly_chart(fig_route, use_container_width=True)
