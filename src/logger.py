import csv
import os
from datetime import datetime

class FireLogger:
    def __init__(self, filename="weights/riwayat_kebakaran.csv"):
        # Menyimpan file di folder weights (atau root DevDrive)
        self.filename = filename
        self.waktu_mulai_terdeteksi = None
        
        # Buat file CSV beserta Header-nya jika belum ada
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Tanggal", "Waktu Mulai", "Waktu Selesai", "Durasi (Detik)", "Akurasi Tertinggi (%)"])

    def catat_mulai(self):
        """Mencatat waktu awal ketika api pertama kali terdeteksi"""
        if self.waktu_mulai_terdeteksi is None:
            self.waktu_mulai_terdeteksi = datetime.now()

    def catat_selesai(self, akurasi_tertinggi):
        """Mencatat waktu ketika api padam dan menghitung durasinya ke CSV"""
        if self.waktu_mulai_terdeteksi is not None:
            waktu_selesai = datetime.now()
            durasi = (waktu_selesai - self.waktu_mulai_terdeteksi).total_seconds()
            
            # Filter: Hanya catat jika api menyala minimal 1 detik (menghindari false alarm sekilas)
            if durasi >= 1.0:
                tanggal = self.waktu_mulai_terdeteksi.strftime("%Y-%m-%d")
                jam_mulai = self.waktu_mulai_terdeteksi.strftime("%H:%M:%S")
                jam_selesai = waktu_selesai.strftime("%H:%M:%S")
                
                with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([tanggal, jam_mulai, jam_selesai, f"{durasi:.2f}", f"{akurasi_tertinggi * 100:.1f}%"])
                print(f"[LOG] Data kebakaran berhasil disimpan ke {self.filename} (Durasi: {durasi:.2f}s)")
            
            # Reset status untuk deteksi berikutnya
            self.waktu_mulai_terdetrows = None
            self.waktu_mulai_terdeteksi = None