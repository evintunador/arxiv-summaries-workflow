from pynput import keyboard
import time
import os
from config import display_reverse_alphabetical, hotkey

timestamps = []
start_time = time.time()
folder_path = "pdfs"

# reverse=True because when I bulk open files in safari it displays them in reverse-chronological order. 
pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.pdf')], reverse=display_reverse_alphabetical)
file_iter = iter(pdf_files)

def on_activate():
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)

    print(f"Hotkey activated {minutes}:{seconds:02d}")  # Debug line
    global file_iter
    try:
        filename = next(file_iter).replace('.pdf', '')
    except StopIteration:
        filename = "Outro"
    
    timestamps.append(f"{minutes}:{seconds:02d} {filename}")

timestamps.append("0:00 Intro")

current_keys = set()

def on_press(key):
    if key == keyboard.KeyCode.from_char(hotkey):
        on_activate()
    elif key == keyboard.Key.esc:
        return False  # Stop listener

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


with open(f"timestamps.txt", "w") as f:
    f.write("\n".join(timestamps))
