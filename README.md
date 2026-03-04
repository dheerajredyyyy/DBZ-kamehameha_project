# Kamehameha Hand-Tracking Effect

<p align="center">
  <img src="https://media.giphy.com/media/dmFXUZ5up1T896HP8B/giphy.gif" width="600"/>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-blue?logo=numpy)
![Pygame](https://img.shields.io/badge/Pygame-Audio%20Engine-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

</p>

---

An **interactive Dragon Ball–inspired Kamehameha simulation** built using **Python**, **MediaPipe**, **OpenCV**, **NumPy**, and **Pygame**.  
This project uses real-time **webcam-based hand tracking** to allow users to charge and release a cinematic energy blast with particle effects, bloom lighting, screen shake, sound effects, and a custom end screen UI.

---

# Features

- Real-time **hand tracking** using MediaPipe
- **Interactive energy charging and release**
- **Particle effects and bloom lighting**
- **Screen shake and heat distortion effects**
- **Sound effects for charging and blast release**
- **Stylized end screen UI**
- Fully **webcam-based interaction**

---

# Technologies Used

- **Python 3**
- **MediaPipe** – hand tracking
- **OpenCV (cv2)** – video capture, image processing, rendering
- **NumPy** – numerical operations and image buffers
- **Pygame** – audio playback and sound effects

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

## 2. (Optional) Create and Activate a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Ensure that a **working webcam** is connected to your system.

---

# How to Run

From the project root directory:

```bash
python main.py
```

This will:

- Open the **default webcam** using OpenCV
- Detect **both hands using MediaPipe**
- Allow you to **charge and release a Kamehameha-style blast**
- Display a **stylized end screen with UI elements**

Press **`q`** to quit the application at any time.

---

# Folder Structure

```text
.
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
└── media/                # Assets (audio + images)
    ├── Basechargeloop1.wav
    ├── Escalation2.wav
    ├── Release3.wav
    ├── background.jpg
    └── logo.png
```

> Note: A `venv/` directory is recommended for local development but should not be committed; it is already covered by `.gitignore`.

---

# Assets and Paths

All assets are referenced using **relative paths**, allowing the project to run correctly regardless of installation location.

### Audio

```
media/Basechargeloop1.wav
media/Escalation2.wav
media/Release3.wav
```

### Images

```
media/background.jpg
media/logo.png
```

Ensure the **`media/` folder sits next to `main.py`**.

---

# Project Information

**Owner:** Dheeraj Reddy  
**Author:** Dheeraj Reddy  

### Developer Watermark

```
Developed by Dheeraj Reddy
```

This watermark is also displayed on the **end screen UI**.

### Description

This project demonstrates how **computer vision and real-time interaction** can be used to create engaging visual effects inspired by anime. Using **MediaPipe hand tracking**, the system detects user gestures through a webcam and generates a **Dragon Ball–style Kamehameha energy blast** enhanced with particle systems, bloom effects, sound design, and a stylized interface.

---

# Notes for Contributors

- Place all new assets inside the **`media/` directory**
- Reference files using **relative paths**
- Avoid committing local environment or IDE files such as:

```
venv/
__pycache__/
.env
.vscode/
.idea/
```

These are already excluded via `.gitignore`.
