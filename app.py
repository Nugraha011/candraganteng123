import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Mengatur konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Saham TLKM", layout="wide")

st.title("📈 Dashboard Pergerakan Saham Telkom Indonesia (TLKM.JK)")
st.markdown("Aplikasi ini menampilkan pergerakan harga saham dan volume perdagangan berdasarkan data historis.")

# Fungsi untuk memuat dan membersihkan data
@st.cache_data
def load_data():
    # Pastikan nama file CSV sesuai dengan yang ada di direktori Anda
    file_name = "SAHAM - PT Telekomunikasi Indonesia Tbk (TLKM.JK) - Sheet1.csv"
    df = pd.read_csv(file_name)
    
    # Konversi format kolom 'Date' menjadi tipe datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    
    # Membersihkan kolom 'Volume' (menghapus titik sebagai pemisah ribuan)
    if df['Volume'].dtype == 'O':
        df['Volume'] = df['Volume'].str.replace('.', '', regex=False).astype(float)
        
    # Mengurutkan data berdasarkan tanggal dari yang paling lama ke terbaru
    df = df.sort_values('Date')
    
    return df

try:
    # Memanggil data
    df = load_data()
    
    # 1. Menampilkan Tabel Data Terbaru
    st.subheader("Data Historis Terbaru")
    st.dataframe(df.tail(10).reset_index(drop=True), use_container_width=True)
    
    # 2. Membuat Grafik Candlestick menggunakan Plotly
    st.subheader("Grafik Harga Saham (Candlestick)")
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Harga Saham'
    )])
    
    # Mengatur layout grafik
    fig.update_layout(
        xaxis_title="Tanggal",
        yaxis_title="Harga (IDR)",
        xaxis_rangeslider_visible=False, # Menyembunyikan slider di bawah grafik agar lebih rapi
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. Menampilkan Grafik Volume Perdagangan
    st.subheader("Volume Perdagangan")
    # Menggunakan bar chart bawaan dari Streamlit
    st.bar_chart(data=df.set_index('Date')['Volume'], height=300)

except FileNotFoundError:
    st.error("File CSV tidak ditemukan! Pastikan file 'SAHAM - PT Telekomunikasi Indonesia Tbk (TLKM.JK) - Sheet1.csv' berada di dalam folder yang sama dengan app.py.")
except Exception as e:
    st.error(f"Terjadi kesalahan saat memproses data: {e}")