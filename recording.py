import webbrowser
import time
import re
from pynput import keyboard
import os
from config import next_hotkey, delete_hotkey, replacements

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
        # optionally might add these back in later
        #f"https://bytez.com/docs/arxiv/{arxiv_id}",
        #f"https://alphaxiv.org/abs/{arxiv_id}",
        original_link
    ] if arxiv_id else [original_link]
    
    for link in links_to_open:
        print(f"Opening: {link}")
        webbrowser.open(link)
        if len(links_to_open) > 1:
            time.sleep(2)  # Sleep for 2 seconds between each link

def apply_replacements(text, replacements):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def next_paper():
    global start_time, timestamps, current_link_index, links

    if start_time is None:
        # First hotkey press: start the timer
        start_time = time.time()
        print("Timer started!")
    
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)

    if current_link_index < len(links):
        title, link = links[current_link_index]
        line = f"{title} {link}"
        line = apply_replacements(line, replacements)
        
        timestamp = f"{minutes}:{seconds:02d} {line}"
        timestamps.append(timestamp)
        print(timestamp)

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

def delete_last_timestamp():
    global timestamps, current_link_index, start_time
    if timestamps:
        removed_timestamp = timestamps.pop()
        print(f"Deleted timestamp: {removed_timestamp}")
        
        # Write updated timestamps to file
        with open(timestamps_file, "w") as f:
            f.write("\n".join(timestamps))
    else:
        print("No timestamps to delete")

def on_press(key):
    if key == keyboard.KeyCode.from_char(next_hotkey):
        next_paper()
    elif key == keyboard.KeyCode.from_char(delete_hotkey):
        delete_last_timestamp()
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

if not links:
    print("No links found in links.txt")

print("The first link(s) will be opened and timer will be started when you first hit the `next_hotkey` as defined in config.py")
print("Subsequent next_hotkey presses will record timestamps and open the next link(s).")
print("Triggers of the `delete_hotkey` as defined in config.py will delete the last line from timestamps.txt")
print("Press ESC to exit the program.")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Program ended.")