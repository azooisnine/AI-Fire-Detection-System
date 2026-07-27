import cv2
import threading
import requests
import time
from ultralytics import YOLO
from ui import FireVisualUI
from logger import FireLogger

# ================================
# KONFIGURASI
# ================================
URL_LARAVEL = "http://127.0.0.1:8000/api/fire-update"

# sementara
# PERSON = API
DETECTION_CLASS = 0

# ================================
# KIRIM DATA KE WEBSITE
# ================================

def kirim_ke_laravel(status_text, confidence_score, person_count):

    try:

        payload = {
            "status": status_text,
            "confidence": float(confidence_score),
            "person": person_count,
            "system": "AKTIF",
            "image": ""
        }

        print("URL:", URL_LARAVEL)

        response = requests.post(
            URL_LARAVEL,
            json=payload,
            timeout=3
        )

        print("\n========== LARAVEL ==========")
        print("Payload     :", payload)
        print("Status Code :", response.status_code)
        print("Response    :", response.text)
        print("=============================\n")

    except Exception as e:

        print("ERROR:", e)


# ================================
# MAIN
# ================================

def main():

    print("Loading Fire Model...")
    fire_model = YOLO("weights/best.pt")

    print("Loading Person Model...")
    person_model = YOLO("yolov8n.pt")

    ui_system = FireVisualUI()
    logger_system = FireLogger()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera tidak ditemukan")
        return

    print("System Running...")

    alarm_aktif = False

    waktu_deteksi = None

    durasi_alarm = 3

    status_sebelumnya = ""

    sync_terakhir = 0

    interval_sync = 1

    confidence_tertinggi = 0

    waktu_hilang = None

    durasi_hilang = 2

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # Deteksi api
        hasil_fire = fire_model(
            frame,
            conf=0.25,
            verbose=False,
            stream=True
        )

        # Deteksi manusia
        hasil_person = person_model(
            frame,
            conf=0.5,
            classes=[0],   # class 0 = person
            verbose=False,
            stream=True
        )

        ada_objek = False
        current_conf = 0
        jumlah_orang = 0

        frame_tampilan = frame.copy()

        # ==========================
        # HASIL DETEKSI API
        # ==========================
        for r in hasil_fire:

            frame_tampilan = r.plot()

            for box in r.boxes:

                ada_objek = True

                current_conf = float(box.conf[0])

                if current_conf > confidence_tertinggi:
                    confidence_tertinggi = current_conf

        # ==========================
        # HASIL DETEKSI MANUSIA
        # ==========================

        # ==========================
        # HASIL DETEKSI MANUSIA
        # ==========================
            for r in hasil_person:

                for box in r.boxes:

                    jumlah_orang += 1

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(
                        frame_tampilan,
                        (x1, y1),
                        (x2, y2),
                        (255, 0, 0),
                        2
                    )

                    cv2.putText(
                        frame_tampilan,
                        "Person",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 0, 0),
                        2
                    )

        # ==========================
        # LOGIKA DETEKSI
        # ==========================

# ==========================
# LOGIKA DETEKSI
# ==========================

        if ada_objek:

            waktu_hilang = None

            if waktu_deteksi is None:
                waktu_deteksi = time.time()

            if time.time() - waktu_deteksi >= durasi_alarm:
                alarm_aktif = True

        else:

            if waktu_hilang is None:
                waktu_hilang = time.time()

            if time.time() - waktu_hilang >= durasi_hilang:

                waktu_deteksi = None

                if alarm_aktif:
                    logger_system.catat_selesai(confidence_tertinggi)

                alarm_aktif = False
                confidence_tertinggi = 0

        status = "KRITIS" if alarm_aktif else "AMAN"

        # ==========================
        # SYNC WEBSITE
        # ==========================

        sekarang = time.time()

        if sekarang - sync_terakhir >= interval_sync or status != status_sebelumnya:

            sync_terakhir = sekarang
            status_sebelumnya = status

            threading.Thread(
                target=kirim_ke_laravel,
                args=(
                    status,
                    current_conf if alarm_aktif else 0,
                    jumlah_orang
                ),
                daemon=True
            ).start()

        # ==========================
        # LOGGER
        # ==========================

        if alarm_aktif:

            logger_system.catat_mulai()

        # ==========================
        # UI
        # ==========================

        frame_ui = ui_system.gambar_ui(
            frame_tampilan,
            alarm_aktif
        )

        cv2.imwrite(
            "/Volumes/DevDrive/dashboard-keamanan/public/camera/latest.jpg",
            frame_ui
        )

        cv2.imshow(
            "Fire Detection",
            frame_ui
        )

        tombol = cv2.waitKey(1)

        if tombol & 0xFF == ord('q'):

            try:

                requests.post(

                    URL_LARAVEL,

                    json={
                        "status": "AMAN",
                        "confidence": 0,
                        "system": "NONAKTIF",
                        "image": ""
                    },

                    timeout=3

                )

            except:
                pass

            break

    try:

        import os

        os.remove(
            "/Volumes/DevDrive/dashboard-keamanan/public/camera/latest.jpg"
        )

    except:
        pass

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()