import os
import sqlite3
import requests
import sys

print("=" * 60)
print("       SYSTEM DIAGNOSTIC: DETECTOR API TO LARAVEL       ")
print("=" * 60)

# 1. CEK FILE DATABASE SQLITE
db_path = "/Volumes/DevDrive/dashboard-keamanan/database/database.sqlite"
print(f"[1/4] Memeriksa Database Lokal...")
if os.path.exists(db_path):
    print(f"  ✓ File database ditemukan di: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Cek apakah tabel fire_logs sudah terbuat dari migrasi
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fire_logs';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("  ✓ Tabel 'fire_logs' SUDAH BERHASIL dimigrasi.")
            cursor.execute("SELECT COUNT(*) FROM fire_logs")
            total_rows = cursor.fetchone()[0]
            print(f"  ✓ Jumlah log tersimpan saat ini: {total_rows} data.")
            
            if total_rows > 0:
                cursor.execute("SELECT status, confidence, created_at FROM fire_logs ORDER BY id DESC LIMIT 1")
                last_data = cursor.fetchone()
                print(f"  └── Data terakhir di DB: Status=[{last_data[0]}], Conf={last_data[1]}, Waktu={last_data[2]}")
        else:
            print("  ❌ ERROR: Tabel 'fire_logs' BELUM ADA. Silakan jalankan 'php artisan migrate'.")
        conn.close()
    except Exception as e:
        print(f"  ❌ ERROR saat membaca database: {e}")
else:
    print(f"  ❌ ERROR: File '{db_path}' tidak ditemukan! Periksa konfigurasi .env.")

print("-" * 60)

# 2. CEK SERVER LARAVEL (PORT 8000)
url_status = "http://127.0.0.1:8000/fire-status"
url_update = "http://127.0.0.1:8000/fire-update"
print("[2/4] Memeriksa Koneksi Server 'php artisan serve'...")

try:
    response = requests.get(url_status, timeout=3)
    print(f"  ✓ Server Laravel AKTIF (Status HTTP: {response.status_code})")
    print(f"  └── Data JSON saat ini yang dibaca browser: {response.text}")
except requests.exceptions.ConnectionError:
    print("  ❌ ERROR: Server Laravel MATI! Pastikan sudah menjalankan 'php artisan serve' di terminal.")
    sys.exit()
except Exception as e:
    print(f"  ❌ ERROR Koneksi: {e}")

print("-" * 60)

# 3. SIMULASI KIRIM DATA (TESTING API POST)
print("[3/4] Melakukan Simulasi Pengiriman Data dari Python...")
payload_test = {
    "status": "KRITIS",
    "confidence": 0.95,
    "image": "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" # Dummy base64 1 pixel
}

try:
    res = requests.post(url_update, json=payload_test, timeout=3)
    print(f"  ✓ Respons API /fire-update: Status Code [{res.status_code}]")
    if res.status_code == 201:
        print("  🎉 KESIMPULAN API: SUKSES! Laravel menerima data POST dari Python tanpa halangan CSRF.")
    elif res.status_code == 419:
        print("  ❌ KESIMPULAN API: GAGAL (CSRF Blocked)! Proteksi CSRF belum dimatikan di bootstrap/app.php.")
    elif res.status_code == 404:
        print("  ❌ KESIMPULAN API: GAGAL (404 Not Found)! Route::post('/fire-update') belum terdaftar di routes/web.php.")
    else:
        print(f"  ❌ KESIMPULAN API: GAGAL dengan kode error {res.status_code}. Isi error: {res.text}")
except Exception as e:
    print(f"  ❌ Gagal menembak API Update: {e}")

print("=" * 60)