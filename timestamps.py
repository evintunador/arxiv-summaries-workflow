from pynput import keyboard
import time
import os
from config import hotkey, replacements, limit

timestamps = []
start_time = time.time()

links_file = "links.txt"
timestamps_file = "timestamps.txt"

# Check if timestamps.txt exists
first_run = not os.path.exists(timestamps_file)

if first_run:
    # Read the lines of the file in reverse order
    with open(links_file, "r") as f:
        lines = f.readlines()
    lines.reverse()  # Reverse the order
    file_iter = iter(lines)
else:
    # Read existing timestamps
    with open(timestamps_file, "r") as f:
        timestamps = f.read().splitlines()

def apply_replacements(text, replacements):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def calculate_total_characters(timestamps):
    return sum(len(timestamp) for timestamp in timestamps)

def trim_timestamps(timestamps, limit=limit):
    while calculate_total_characters(timestamps) > limit:
        min_diff = float('inf')
        min_index = -1

        for i in range(1, len(timestamps) - 1):
            curr_time = timestamps[i].split()[0]
            next_time = timestamps[i + 1].split()[0]

            curr_minutes, curr_seconds = map(int, curr_time.split(':'))
            next_minutes, next_seconds = map(int, next_time.split(':'))

            curr_total_seconds = curr_minutes * 60 + curr_seconds
            next_total_seconds = next_minutes * 60 + next_seconds

            diff = next_total_seconds - curr_total_seconds

            if diff < min_diff:
                min_diff = diff
                min_index = i

        if min_index != -1:
            del timestamps[min_index]

    return timestamps

def on_activate():
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)

    print(f"Hotkey activated {minutes}:{seconds:02d}")  # Debug line
    
    if first_run:
        global file_iter
        try:
            link = next(file_iter).strip()  # Get link and remove newline
            parts = link.split(' | ')
            line = parts[0]+' '+parts[1]
            # Apply replacements to the line
            line = apply_replacements(line, replacements)
        except StopIteration:
            line = "Outro"
        
        if not timestamps or not timestamps[-1].endswith("Outro"):
            timestamps.append(f"{minutes}:{seconds:02d} {line}")
    else:
        # For subsequent runs, just add the timestamp
        timestamps.append(f"{minutes}:{seconds:02d}")

if first_run:
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

# Trim timestamps if it's not the first run
if not first_run:
    timestamps = trim_timestamps(timestamps)

with open(timestamps_file, "w") as f:
    f.write("\n".join(timestamps))