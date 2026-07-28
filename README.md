# AI Fire Detection Monitoring System

An Artificial Intelligence based Fire Detection System using **YOLOv8 Computer Vision** for real-time fire detection. The system monitors live camera input, detects fire automatically, records detection history, and sends detection results to a Laravel Dashboard.

---

## 📌 Features

- 🔥 Real-Time Fire Detection
- 📹 Live Camera Monitoring
- 📊 Detection Confidence Score
- 👤 Person Detection Counter
- 📝 Detection History Logging
- 🌐 Laravel Dashboard Integration
- 📡 REST API Communication
- 🤖 YOLOv8 Object Detection

---

# Project Structure

```
AI-Fire-Detection-System
│
├── src/
│   ├── detector.py
│   ├── logger.py
│   └── ui.py
│
├── weights/
│   ├── best.pt
│   ├── fire_smoke.pt
│   └── riwayat_kebakaran.csv
│
├── public/
│
├── stream_server.py
├── cek_error.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Technologies

- Python 3.9+
- YOLOv8 (Ultralytics)
- OpenCV
- NumPy
- Requests
- Flask (Streaming Server)
- Laravel API
- HTML
- CSS
- JavaScript

---

# Installation

Clone repository

```bash
git clone https://github.com/azooisnine/AI-Fire-Detection-System.git
```

Masuk ke folder project

```bash
cd AI-Fire-Detection-System
```

Buat Virtual Environment

```bash
python -m venv venv
```

Aktifkan Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Install dependency

```bash
pip install -r requirements.txt
```

---

# Run Application

Jalankan sistem deteksi

```bash
python src/detector.py
```

Jalankan streaming server

```bash
python stream_server.py
```

---

# Dashboard

Detection results are sent automatically to the Laravel Dashboard using REST API.

Information displayed:

- Fire Status
- Confidence Score
- Person Detection
- Detection History
- Last Update
- Live Camera

---

# Detection Workflow

Camera

↓

YOLOv8 Model

↓

Fire Detection

↓

Confidence Calculation

↓

Detection Logger

↓

REST API

↓

Laravel Dashboard

---

# Example Output

Status

```
KRITIS
```

Confidence

```
98.71 %
```

Detected Person

```
1
```

---

# Future Improvements

- Smoke Detection
- Telegram Notification
- Firebase Integration
- Multi Camera Support
- Fire Alarm Integration

---

# Author

**Rasya Muzakki Junior**

SMK Telkom Banjarbaru

Software Engineering (RPL)

GitHub

https://github.com/azooisnine