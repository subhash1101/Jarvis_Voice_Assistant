import pvporcupine
import sounddevice as sd
import speech_recognition as sr
import numpy as np
import os
import sys
import threading
import time
import queue
from datetime import datetime
from commands import execute_command

# ---------------------- CONFIG ----------------------
ACCESS_KEY = "5AGyRzeaksvWwAH6GVMgfFLzOIOzfpKbYdtIa84e/kCNJZiMRZE9Gw=="  # Replace with your actual key

# ---------------------- SPEAK QUEUE + THREAD ----------------------
speak_queue = queue.Queue()
running = True

def speak(text):
    """Speak the given text and also print it."""
    print("Jarvis:", text)
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Use first available voice
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Speak Error] {e}")

def speak_from_queue():
    while running:
        try:
            text = speak_queue.get(timeout=0.2)
            # Debug print for diagnosis
            print(f"[DEBUG] About to speak: {text}")
            speak(text)
        except queue.Empty:
            continue

# ---------------------- VOICE RECOGNITION ----------------------
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
            print("Processing command...")
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No command detected. Returning to wake word listening...")
            return None
        except sr.UnknownValueError:
            print("Could not understand. Returning to wake word listening...")
            return None
        except sr.RequestError as e:
            print(f"Speech service error: {e}")
            return None

# ---------------------- PORCUPINE WAKE WORD ----------------------
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def create_porcupine():
    keyword_file = resource_path("pvporcupine/resources/keyword_files/windows/jarvis_windows.ppn")
    library_path = resource_path("pvporcupine/lib/windows/amd64/libpv_porcupine.dll")
    return pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[keyword_file],
        library_path=library_path
    )

# ---------Below code only for running in powershell and above code for running .exe file-------
# def create_porcupine(): 
#     pvporcupine_path = os.path.dirname(pvporcupine.__file__) 
#     keyword_path = os.path.join(pvporcupine_path, "resources", "keyword_files", "windows") 
#     keyword_file = os.path.join(keyword_path, "jarvis_windows.ppn") 
#     return pvporcupine.create( access_key=ACCESS_KEY, keyword_paths=[keyword_file] )

# ---------------------- STATE FLAGS ----------------------
stream = None
wake_word_detected = False
listening_for_command = False

# ---------------------- COMMAND HANDLER ----------------------
def process_command():
    global wake_word_detected, listening_for_command
    command = listen_for_command()
    if command:
        execute_command(command)
    wake_word_detected = False
    listening_for_command = False
    print("Listening for 'Jarvis' again...")

# ---------------------- CALLBACK ----------------------
def callback(indata, frames, time_info, status):
    global wake_word_detected, listening_for_command
    if status:
        print("Status:", status)
    try:
        pcm = (indata[:, 0] * 32767).astype(np.int16).tolist()
        result = porcupine.process(pcm)

        if result >= 0 and not wake_word_detected and not listening_for_command:
            wake_word_detected = True
            listening_for_command = True
            speak_queue.put("Yes sir")
            print("Wake word detected!")
            threading.Thread(target=process_command, daemon=True).start()
    except Exception as e:
        print("Error in callback:", e)

# ---------------------- WAKE WORD DETECTION LOOP ----------------------
def start_wake_word_detection():
    global stream, porcupine, running
    if not running:
        return
    try:
        porcupine = create_porcupine()
    except Exception as e:
        print(f"Error creating Porcupine: {e}")
        return
    frame_length = porcupine.frame_length
    sample_rate = porcupine.sample_rate

    print("Listening for 'Jarvis'...")
    try:
        stream = sd.InputStream(
            channels=1,
            samplerate=sample_rate,
            blocksize=frame_length,
            dtype='float32',
            callback=callback
        )
        stream.start()
        while stream.active and running:
            time.sleep(0.1)
    except Exception as e:
        print(f"Error in wake word detection: {e}")
    finally:
        if stream and stream.active:
            stream.stop()
            stream.close()

# ---------------------- MAIN ----------------------
print("Jarvis Voice Assistant is ready!")
print("Say 'Jarvis' to activate, then give your command")
print("Press Ctrl+C to exit")
speak_queue.put("Jarvis is online and ready")

threading.Thread(target=speak_from_queue, daemon=True).start()

try:
    start_wake_word_detection()
except KeyboardInterrupt:
    print("Shutting down Jarvis...")
    running = False
    speak_queue.put("Goodbye sir")
finally:
    running = False
    if stream and stream.active:
        stream.stop()
        stream.close()
    if 'porcupine' in locals():
        porcupine.delete()
