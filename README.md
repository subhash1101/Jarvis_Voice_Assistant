# 🎙️ Jarvis Voice Assistant

A Python-based voice assistant that activates on a **wake word ("Jarvis")** and executes spoken commands.  
It uses **SpeechRecognition**, **pyttsx3**, **sounddevice**, and **Porcupine** for wake word detection.

---

## 🚀 Features
- Wake word detection (**"Jarvis"**)  
- Offline + Online **speech recognition** (Google Speech API used here)  
- Voice feedback with **pyttsx3**  
- Modular command execution (extend via `commands.py`)  
- Multithreaded queue for **non-blocking speech output**  
- Easily extensible for personal assistant functions

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jarvis-assistant.git
   cd jarvis-assistant
   ```
2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Download Porcupine SDK**
   - Get the Porcupine SDK and place the required files (libpv_porcupine, .ppn keyword files) inside the pvporcupine/ directory.
7. **Set your Access Key**
   - Replace the ACCESS_KEY in jarvis_assistant.py with your Porcupine key from Picovoice Console.
