# Your commands.py remains unchanged
# Just ensure you don't use pyttsx3 or speak() in here unless you use the same queue mechanism

import os
import pywhatkit
import webbrowser
import pyautogui
import re
import time
import datetime
import random
import wmi
import subprocess
import glob
import urllib
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

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

def set_brightness(level):
    level = max(0, min(level, 100))
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(level, 0)

def set_volume(percent):
    percent = max(0, min(percent, 100))
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    min_vol, max_vol, _ = volume.GetVolumeRange()
    vol_db = min_vol + (percent / 100.0) * (max_vol - min_vol)
    volume.SetMasterVolumeLevel(vol_db, None)

def extract_number(command):
    number_words = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
        'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
        'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
        'eighty': 80, 'ninety': 90, 'hundred': 100
    }
    digits = re.findall(r'\d+', command)
    if digits:
        return int(digits[0])
    words = command.split()
    for word in words:
        if word in number_words:
            return number_words[word]
    return None

def find_and_open_game(game_name):
    game_extensions = ['.exe', '.lnk']
    search_locations = [
        os.path.expanduser("~/Desktop"),
        "C:/Desktop",
        "D:/Games",
    ]
    game_name_lower = game_name.lower()
    for location in search_locations:
        if os.path.exists(location):
            try:
                for root, dirs, files in os.walk(location):
                    for file in files:
                        file_lower = file.lower()
                        if game_name_lower in file_lower:
                            file_path = os.path.join(root, file)
                            file_ext = os.path.splitext(file)[1].lower()
                            if file_ext in game_extensions:
                                try:
                                    subprocess.Popen(file_path)
                                    print(f"Opening game: {file}")
                                    return True
                                except Exception as e:
                                    print(f"Could not open {file}: {e}")
                                    continue
            except Exception as e:
                continue
    return False

def find_and_open_movie(movie_name):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
    search_locations = [
        os.path.expanduser("~/Videos"),
        "D:/Movies",
        "D:/Videos",
        "C:/Videos",
    ]
    movie_name_lower = movie_name.lower()
    for location in search_locations:
        if os.path.exists(location):
            try:
                for root, dirs, files in os.walk(location):
                    for file in files:
                        file_lower = file.lower()
                        if movie_name_lower in file_lower:
                            file_path = os.path.join(root, file)
                            file_ext = os.path.splitext(file)[1].lower()
                            if file_ext in video_extensions:
                                try:
                                    os.startfile(file_path)
                                    speak(f"Opening movie: {file}")
                                    return True
                                except Exception as e:
                                    speak(f"Could not open {file}: {e}")
                                    continue
            except Exception as e:
                continue
    return False

def open_application(app_name):
    app_commands = {
        'file explorer': 'explorer',
        'explorer': 'explorer',
        'files': 'explorer',
        'folder': 'explorer',
        'folders': 'explorer',
        'notepad': 'notepad',
        'notebook': 'notepad',
        'text editor': 'notepad',
        'calculator': 'calc',
        'calc': 'calc',
        'paint': 'mspaint',
        'wordpad': 'wordpad',
        'control panel': 'control',
        'task manager': 'taskmgr',
        'cmd': 'cmd',
        'command prompt': 'cmd',
        'powershell': 'powershell',
        'edge': 'msedge',
        'vlc': 'vlc',
        'excel': 'excel',
        'word': 'winword',
        'powerpoint': 'powerpnt',
        'outlook': 'outlook'
    }
    for key, value in app_commands.items():
        if key in app_name.lower():
            try:
                subprocess.Popen(value)
                speak(f"Opening {key}...")
                return True
            except:
                speak(f"Could not open {key}")
                return False
    return False

def execute_command(command):
    command = command.lower().strip()
    brightness_patterns = [
        r'(brightness|light|screen|display).*?(set|to|at|make).*?(\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)',
        r'(set|make|change|adjust).*?(brightness|light|screen|display).*?(to|at).*?(\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)',
        r'(brightness|light|screen|display).*?(\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)'
    ]
    for pattern in brightness_patterns:
        if re.search(pattern, command):
            level = extract_number(command)
            if level is not None:
                set_brightness(level)
                speak(f"Brightness set to {level}%")
                return

    volume_patterns = [
        r'(volume|sound|audio|speaker).*?(set|to|at|make).*?(\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)',
        r'(set|make|change|adjust).*?(volume|sound|audio|speaker).*?(to|at).*?(\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)',
        r'(volume|sound|audio|speaker).*?(\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)'
    ]
    for pattern in volume_patterns:
        if re.search(pattern, command):
            percent = extract_number(command)
            if percent is not None:
                set_volume(percent)
                speak(f"Volume set to {percent}%")
                return

    game_patterns = [
        r'(open|start|launch|run|play).*?(game).*?(.*)',
        r'(game).*?(open|start|launch|run|play).*?(.*)',
    ]
    for pattern in game_patterns:
        match = re.search(pattern, command)
        if match:
            game_name = match.group(3) if len(match.groups()) >= 3 else match.group(1)
            if game_name and len(game_name.strip()) > 2:
                game_name = game_name.strip()
                if find_and_open_game(game_name):
                    return
                else:
                    print(f"Could not find game: {game_name}")
                    return

    movie_patterns = [
        r'(open|start|play|watch).*?(movie).*?(.*)',
        r'(movie).*?(open|start|play|watch).*?(.*)',
    ]
    for pattern in movie_patterns:
        match = re.search(pattern, command)
        if match:
            movie_name = match.group(3) if len(match.groups()) >= 3 else match.group(1)
            if movie_name and len(movie_name.strip()) > 2:
                movie_name = movie_name.strip()
                if find_and_open_movie(movie_name):
                    return
                else:
                    print(f"Could not find movie: {movie_name}")
                    return

    search_patterns = [
        r'(search|find|look up|google)\s+(.*)'
    ]
    for pattern in search_patterns:
        match = re.search(pattern, command)
        if match:
            query = match.group(2).strip()

            # Remove filler words
            query = query.replace("on google", "").replace("in google", "").strip()
            query = query.replace("on youtube", "").replace("in youtube", "").strip()

            if "google" in command:
                search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                webbrowser.open(search_url)
                speak(f"Searching for '{query}' on Google...")
                return
            else:
                search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                webbrowser.open(search_url)
                speak(f"Searching for '{query}' on YouTube...")
                return
            
    open_patterns = [
        r'(open|start|launch|run).*?(.*)',
        r'(.*)',
    ]
    for pattern in open_patterns:
        match = re.search(pattern, command)
        if match:
            app_name = match.group(2) if len(match.groups()) >= 2 else match.group(1)
            if app_name and len(app_name.strip()) > 2:
                app_name = app_name.strip()
                if any(word in app_name for word in ['gmail', 'email', 'mail']):
                    webbrowser.open("https://mail.google.com")
                    speak("Opening Gmail")
                    return
                if any(word in app_name for word in ['youtube', 'yt', 'video']):
                    webbrowser.open("https://www.youtube.com")
                    speak("Opening YouTube...")
                    return
                if any(word in app_name for word in ['Leetcode']):
                    webbrowser.open("https://leetcode.com/problemset/")
                    speak("Opening Leetcode...")
                    return
                if any(word in app_name for word in ['google', 'search']):
                    webbrowser.open("https://www.google.com")
                    speak("Opening Google...")
                    return
                if any(word in app_name for word in ['instagram', 'insta']):
                    webbrowser.open("https://www.instagram.com")
                    speak("Opening Instagram...")
                    return
                if open_application(app_name):
                    return
   

    # ✅ Play patterns (only if "search" not mentioned)
    play_patterns = [
        r'(play|start|put on)\s+(?:song|music|track|video)?\s*(.+)',
        r'(song|music|track)\s+(.+)'
    ]
    for pattern in play_patterns:
        match = re.search(pattern, command)
        if match:
            song_name = match.group(2) if len(match.groups()) >= 2 else match.group(1)
            if song_name and len(song_name.strip()) > 2:
                song_name = song_name.strip()
                pywhatkit.playonyt(song_name)
                speak(f"Playing '{song_name}' on YouTube...")
                return

    time_patterns = [
        r'(what|tell me|show me).*?(time|hour)',
        r'(time|hour).*?(now|current)',
        r'(current|now).*?(time|hour)'
    ]
    for pattern in time_patterns:
        if re.search(pattern, command):
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {now}")
            return

    screenshot_patterns = [
        r'(screenshot|screen shot|capture|take picture|take photo)',
        r'(take|make|create).*?(screenshot|screen shot|capture)'
    ]
    for pattern in screenshot_patterns:
        if re.search(pattern, command):
            filename = f"screenshot_{int(time.time())}.png"
            filepath = os.path.join(r"C:\Users\subha\OneDrive\Pictures\Screenshots", filename)
            pyautogui.screenshot(filepath)
            speak("Screenshot captured")
            return

    if any(word in command for word in ['help', 'what can you do', 'commands', 'options']):
        print("\nAvailable commands:")
        print("- Brightness: 'set brightness to 50', 'brightness 30', 'make screen brighter'")
        print("- Volume: 'set volume to 70', 'volume 50', 'make it louder'")
        print("- Play music: 'play despacito', 'play song shape of you', 'start music'")
        print("- Open apps: 'open file explorer', 'open notepad', 'open calculator'")
        print("- Web apps: 'open gmail', 'open youtube', 'open google'")
        print("- Games: 'open game minecraft', 'play game fortnite', 'launch game' (requires 'game' keyword)")
        print("- Movies: 'open movie avengers', 'play movie', 'watch movie' (requires 'movie' keyword)")
        print("- Search: 'search for python tutorial', 'find weather', 'google restaurants'")
        print("- Time: 'what time is it', 'tell me the time', 'current time'")
        print("- Screenshot: 'take screenshot', 'capture screen', 'screenshot'")
        print("- Voice: 'voice' for single voice command, 'voice mode' for continuous")
        return
    else:
        print(f"Sorry, I didn't understand: '{command}'")
        print("Say 'help' to see available commands")
