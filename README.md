
🎱CueX8 – Gesture Controlled 8 Ball Pool

Control 8 Ball Pool using your hand gestures with the power of OpenCV, MediaPipe, and PyAutoGUI.  
This project turns your webcam into a motion controller, allowing you to "aim, lock, select power, and shoot" with simple finger gestures.  

---
🚀 Features:
- 🖐️ **Finger Detection** using MediaPipe Hands.  
- 🎯 **Aim Mode** – Move your cue by showing 1 finger.  
- 🔒 **Lock Target** – Show 2 fingers to lock the aim.  
- ⚡ **Power Selection** – Show 3 fingers and drag to adjust power.  
- 🎮 **Shoot** – Show all 5 fingers to release and strike.  
- 🎥 Real-time webcam input with OpenCV.  
- 🖱️ Seamless integration with mouse/keyboard using PyAutoGUI.  

---

🛠️ Tech Stack
- [OpenCV](https://opencv.org/) – Image processing & webcam input  
- [MediaPipe](https://developers.google.com/mediapipe) – Hand landmarks & gesture recognition  
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) – Mouse & keyboard automation  

---

📦 Installation

1. Clone this repository:
   git clone https://github.com/your-username/8-pool-cue.git
   cd 8-pool-cue

2. Install dependencies:
   pip install opencv-python mediapipe pyautogui

3. Run the project:
   python main.py

---

## 🎮 Controls (State Machine)

| **State** | **Gesture** (Finger Count) | **Action**                    |
| --------- | -------------------------- | ----------------------------- |
| **AIM**   | 1 finger                   | Move cue left/right           |
| **AIM**   | 2 fingers                  | Lock target & switch to POWER |
| **POWER** | 3 fingers                  | Drag to adjust power          |
| **POWER** | 5 fingers                  | Shoot & reset to AIM          |

---

🖼️ Demo

👉 Coming Soon – GIFs/Screenshots of gameplay with gestures.

---

📌 Notes

* Ensure your webcam has a clear view of your hand.
* Background noise (other hands, objects) may affect detection.
* Use in a well-lit environment for best accuracy.

---

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

## 📜 License

This project is licensed under the MIT License.

---

👨‍💻 Author

Built with ❤️ by Ruthvej Giduturi....^(-_-)^
