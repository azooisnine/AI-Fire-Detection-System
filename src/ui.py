import cv2
import os
import threading
import time

class FireVisualUI:
    def __init__(self):
        self.api_terdeteksi_aktif = False
        self.thread_audio_berjalan = False
    def _loop_suara_alarm(self):
        """
        Menggunakan suara Damayanti (Bahasa Indonesia asli di macOS)
        """
        self.thread_audio_berjalan = True

        while self.api_terdeteksi_aktif:
            # -v Damayanti untuk memanggil suara Indonesia
            os.system("say -v Damayanti 'Peringatan! Api terdeteksi. Segera periksa lokasi.'")
            time.sleep(0.5)

        self.thread_audio_berjalan = False

    def gambar_ui(self, frame, api_terdeteksi):
        """
        Menggambar overlay visual merah dan mengatur siklus looping suara alarm.
        """
        h, w, _ = frame.shape
        self.api_terdeteksi_aktif = api_terdeteksi

        if api_terdeteksi:
            
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 255), -1)
            cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)

            
            cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 255), 8)

            
            cv2.putText(frame, "CRITICAL: FIRE DETECTED", (30, 60), 
                        cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.putText(frame, "SYSTEM ALARM: LOOPING", (30, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2, cv2.LINE_AA)
            
        
            if not self.thread_audio_berjalan:
                threading.Thread(target=self._loop_suara_alarm, daemon=True).start()
        else:
            # Tampilan standar saat kondisi AMAN
            cv2.rectangle(frame, (0, 0), (w, h), (0, 255, 0), 2)
            cv2.putText(frame, "SYSTEM STATUS: SECURE", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            
        return frame