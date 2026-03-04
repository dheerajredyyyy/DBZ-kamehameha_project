# Kamehameha Hand-Tracking Effect

An interactive webcam-based Kamehameha-style energy blast effect built with **Python**, **MediaPipe**, **OpenCV**, **NumPy**, and **Pygame**.  
Raise both hands in front of the camera, charge the energy ball, and unleash a cinematic blast with particles, bloom, screen shake, audio, and a custom end screen.

---

## Technologies Used

- **Python 3**
- **MediaPipe** (hand tracking)
- **OpenCV (cv2)** (video capture, image processing, rendering)
- **NumPy** (numeric operations, image buffers)
- **Pygame** (audio playback, sound effects)

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

2. **(Optional) Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

Make sure you have a working webcam connected to your system.

---

## How to Run

From the project root, run:

```bash
python main.py
```

This will:

- Open your default webcam using OpenCV.
- Track both hands via MediaPipe.
- Allow you to charge and fire a Kamehameha-style blast.
- Display a stylized end screen with a background image and UI.

Press **`q`** to quit the application at any time.

---

## Folder Structure

```text
.
├── main.py               # Main entry point for the experience
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules (created for GitHub use)
└── media/                # Game assets (audio + images)
    ├── Basechargeloop1.wav
    ├── Escalation2.wav
    ├── Release3.wav
    ├── background.jpg
    └── logo.png
```

> Note: A `venv/` directory is recommended for local development but should not be committed; it is covered by `.gitignore`.

---

## Assets and Paths

All assets are referenced using **relative paths** so the project works when cloned anywhere:

- Sounds: `media/Basechargeloop1.wav`, `media/Escalation2.wav`, `media/Release3.wav`
- Images: `media/background.jpg`, `media/logo.png`

As long as the `media/` folder sits next to `main.py`, the project can be run from any directory location.

---

## Project Information

- **Owner**: Dheeraj Reddy  
- **Author**: Dheeraj Reddy  
- **Developer Watermark**: `@Developed by Dheeraj Reddy` (also shown on the end screen UI)

**Description**  
This project was developed by **Dheeraj Reddy** using **Python** and **MediaPipe** to create an interactive Kamehameha-style visual effect with real-time hand tracking, particle effects, bloom, heat distortion, audio, and a polished end screen UI.

---

## Notes for Contributors

- Keep all new assets inside the `media/` directory and reference them with **relative paths** (for example, `media/new_sound.wav`).
- Avoid committing local environment or IDE files (`venv/`, `.env`, `__pycache__/`, etc.) which are already covered in `.gitignore`.

# kamehameha
