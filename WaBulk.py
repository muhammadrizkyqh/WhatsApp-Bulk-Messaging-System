from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import urllib.parse

# ======================================
# KONFIGURASI EDGE WEBDRIVER
# ======================================
# 1. Download Edge WebDriver sesuai versi Edge Anda:
#    - Cek versi Edge: buka edge://settings/help
#    - Unduh dari: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# 2. Ganti path ke msedgedriver.exe di bawah ini:
edge_driver_path = r"C:\Penyimpanan Utama\Download\edgedriver_win64\msedgedriver.exe"

# Atur opsi Edge
edge_options = Options()
edge_options.add_argument("--disable-notifications")  # Matikan notifikasi
edge_options.add_argument("--start-maximized")        # Buka browser maksimal
edge_options.use_chromium = True                      # Pastikan pakai Chromium

# Inisialisasi WebDriver
driver = webdriver.Edge(
    service=Service(edge_driver_path),
    options=edge_options
)

# ======================================
# BUKA WHATSAPP WEB
# ======================================
driver.get("https://web.whatsapp.com")
print("\n⚠️ SCAN QR CODE WHATSAPP WEB DALAM 30 DETIK!")
time.sleep(30)  # Beri waktu untuk scan QR code

# ======================================
# BACA DATA PENERIMA
# ======================================
data = pd.read_csv("data_penerima.csv")
link_grup = "https://chat.whatsapp.com/xxxxxxxxxxx"  # Ganti dengan link grup Anda

# ======================================
# LOOP PENGIRIMAN PESAN
# ======================================
for index, row in data.iterrows():
    nama = row['nama']
    dept = row['departemen']
    nomor = row['nomor']
    
    # Format pesan
    pesan = (
        f"PEMBERITAHUAN‼️\n"
        f"Atas nama *{nama}* telah diterima menjadi staff resmi HMSI 2025 pada departemen *{dept}*.\n\n"
        f"KAMI UCAPKAN SELAMAT BERGABUNG DAN BERKONTRIBUSI UNTUK HMSI 💜\n\n"
        f"Silakan join grup kabinet:\n{link_grup}"
    )
    
    # Encode pesan untuk URL
    pesan_encoded = urllib.parse.quote(pesan)
    
    # Buka URL WhatsApp
    driver.get(f"https://web.whatsapp.com/send?phone={nomor}&text={pesan_encoded}")
    time.sleep(15)  # Tunggu halaman terbuka
    
    try:
        # Cari elemen input pesan dan tekan ENTER
        input_box = driver.find_element(
            By.XPATH, 
            '//div[@contenteditable="true"][@data-tab="10"]'
        )
        input_box.send_keys(Keys.ENTER)
        print(f"✅ BERHASIL: Pesan ke {nama} ({nomor})")
    except Exception as e:
        print(f"❌ GAGAL: {nama} ({nomor}) - Error: {str(e)}")
    
    time.sleep(10)  # Jeda 10 detik antar pesan

# ======================================
# TUTUP BROWSER
# ======================================
driver.quit()
print("\n✅ SEMUA PESAN TELAH DI PROSES!")