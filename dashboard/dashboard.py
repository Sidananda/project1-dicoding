import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'dashboard/main_data.csv'
main_data = pd.read_csv(file_path)

st.title("Dashboard Analisis E-commerce Sida Nanda")

# Menghitung jumlah pesanan per bulan
main_data['order_purchase_timestamp'] = pd.to_datetime(main_data['order_purchase_timestamp'])
main_data['order_month_year'] = main_data['order_purchase_timestamp'].dt.to_period('M')
monthly_sales = main_data.groupby('order_month_year').size().reset_index(name='sales_count')
monthly_sales['order_month_year'] = monthly_sales['order_month_year'].astype(str)

# Visualisasi tren penjualan bulanan menggunakan Line Chart
st.subheader("Tren Penjualan Setiap Bulan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='order_month_year', y='sales_count', data=monthly_sales, marker='o', ax=ax)
plt.xticks(rotation=45)
ax.set_title('Tren Penjualan Setiap Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penjualan')
ax.grid(True)
st.pyplot(fig)

# Menghitung frekuensi penggunaan setiap metode pembayaran
payment_counts = main_data['payment_type'].value_counts().reset_index(name='count')
payment_counts.columns = ['method', 'count']

# Visualisasi metode pembayaran yang paling populer menggunakan Pie Chart
st.subheader("Perbandingan Metode Pembayaran")
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(payment_counts['count'], labels=payment_counts['method'], autopct='%1.1f%%', startangle=270)
ax.set_title('Perbandingan Metode Pembayaran')
ax.axis('equal')  # Membuat pie chart menjadi lingkaran sempurna
st.pyplot(fig)

# Mengelompokkan data berdasarkan kota dan negara bagian, menghitung jumlah pesanan di setiap wilayah
location_sales = main_data.groupby(['customer_city', 'customer_state']).size().reset_index(name='order_count')

# Mengurutkan wilayah dengan pesanan terbanyak
top_locations = location_sales.sort_values(by='order_count', ascending=False).head(10)

# Visualisasi wilayah dengan pesanan terbanyak menggunakan Bar Chart
st.subheader("Kota dengan Pesanan Terbanyak")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='order_count', y='customer_city', data=top_locations, palette='viridis', ax=ax)
ax.set_title('Kota dengan Pesanan Terbanyak')
ax.set_xlabel('Jumlah Pesanan')
ax.set_ylabel('Kota')
st.pyplot(fig)
