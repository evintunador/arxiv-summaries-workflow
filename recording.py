import webbrowser
import time
import re
from pynput import keyboard
import os
from config import hotkey, replacements

# File paths
links_file = 'links.txt'
timestamps_file = 'timestamps.txt'

# Global variables
timestamps = []
start_time = None
current_link_index = 0
links = []

def extract_arxiv_id(url):
    match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', url)
    return match.group(1) if match else None

def open_links(arxiv_id, original_link):
    links_to_open = [
        f"https://alphaxiv.org/abs/{arxiv_id}",
        original_link,
        f"https://bytez.com/docs/arxiv/{arxiv_id}"
    ] if arxiv_id else [original_link]
    
    for link in links_to_open:
        print(f"Opening: {link}")
        webbrowser.open(link)
        time.sleep(2)  # Sleep for 2 seconds between each link

def apply_replacements(text, replacements):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def on_activate():
    global start_time, timestamps, current_link_index

    if start_time is None:
        # First hotkey press: start the timer
        start_time = time.time()
        print("Timer started!")
        timestamp = "0:00 Intro"
        timestamps.append(timestamp)
        print(timestamp)
        return

    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)

    if current_link_index < len(links):
        title, link = links[current_link_index]
        line = f"{title} {link}"
        line = apply_replacements(line, replacements)
        
        timestamp = f"{minutes}:{seconds:02d} {line}"
        timestamps.append(timestamp)
        print(timestamp)

        if current_link_index >= 1:  # Open links from the third hotkey press onwards
            arxiv_id = extract_arxiv_id(link)
            open_links(arxiv_id, link)
        
        current_link_index += 1
    else:
        timestamp = f"{minutes}:{seconds:02d} Outro"
        timestamps.append(timestamp)
        print(timestamp)

    # Write timestamps to file after each update
    with open(timestamps_file, "w") as f:
        f.write("\n".join(timestamps))

def on_press(key):
    if key == keyboard.KeyCode.from_char(hotkey):
        on_activate()
    elif key == keyboard.Key.esc:
        return False  # Stop listener

# Read links from file
with open(links_file, 'r') as file:
    for line in file:
        line = line.strip()
        try:
            title, link = line.split(' | ')
            links.append((title, link))
        except ValueError:
            print(f"Invalid line format: {line}")

if links:
    print("Opening the first link(s)...")
    title, link = links[0]
    arxiv_id = extract_arxiv_id(link)
    open_links(arxiv_id, link)
    #current_link_index = 1  # Set to 1 so the next hotkey press will open the second link
else:
    print("No links found in the file.")

print("The first link(s) will be opened when you run the script.")
print("Press the hotkey once to start the timer and record the intro.")
print("Press the hotkey again to record the timestamp for the first paper.")
print("Subsequent hotkey presses will record timestamps and open the next link(s).")
print("Press ESC to exit the program.")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Program ended.")