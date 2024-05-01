from pynput import keyboard
import time
import os
from config import hotkey

timestamps = []
start_time = time.time()

links_file = "links.txt"  # Specify the links file

# Read the lines of the file in reverse order
with open(links_file, "r") as f:
    lines = f.readlines()
lines.reverse()  # Reverse the order
file_iter = iter(lines)

def on_activate():
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)

    print(f"Hotkey activated {minutes}:{seconds:02d}")  # Debug line
    global file_iter
    try:
        link = next(file_iter).strip()  # Get link and remove newline
    except StopIteration:
        link = "Outro"
    
    timestamps.append(f"{minutes}:{seconds:02d} {link}")

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
