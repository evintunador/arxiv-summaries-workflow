import webbrowser  # Module to open web pages
import time  # Module to handle time-related tasks
import re  # Module for regular expressions
from pynput import keyboard  # Module to listen to keyboard events
import os  # Module to interact with the operating system
from config import next_hotkey, delete_hotkey, replacements  # Importing configurations
import glob 

# File paths for storing links and timestamps
links_file = 'links.txt'
timestamps_file = 'timestamps/timestamps_part1.txt'

# Global variables
timestamps = []
start_time = None
current_link_index = 0
links = []

def extract_arxiv_id(url):
    """
    Extracts the arXiv ID from a given URL using a regular expression.
    Returns the ID if found, otherwise returns None.
    """
    match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', url)
    return match.group(1) if match else None

def open_links(arxiv_id, original_link):
    """
    Opens a list of links in the web browser.
    If an arXiv ID is found, it can open additional links (currently commented out).
    """
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
    """
    Applies a series of text replacements based on a dictionary.
    Replaces each occurrence of a key in the text with its corresponding value.
    """
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def next_paper():
    """
    Handles the logic for moving to the next paper.
    Starts a timer on the first call, records timestamps, and opens links.
    """
    global start_time, timestamps, current_link_index, links

    if start_time is None:
        # First hotkey press: start the timer
        start_time = time.time()
        print("Timer started!")
    
    # Calculate elapsed time since the timer started
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)

    if current_link_index < len(links):
        # Get the current link and title
        title, link = links[current_link_index]
        line = f"{title} {link}"
        line = apply_replacements(line, replacements)
        
        # Create a timestamp and add it to the list
        timestamp = f"{minutes}:{seconds:02d} {line}"
        timestamps.append(timestamp)
        print(timestamp)

        # Extract arXiv ID and open the link(s)
        arxiv_id = extract_arxiv_id(link)
        open_links(arxiv_id, link)
        current_link_index += 1
    else:
        # If no more links, add an outro timestamp
        timestamp = f"{minutes}:{seconds:02d} Outro"
        timestamps.append(timestamp)
        print(timestamp)

    # Write timestamps to file after each update
    with open(timestamps_file, "w") as f:
        f.write("\n".join(timestamps))

def delete_last_timestamp():
    """
    Deletes the last recorded timestamp and updates the file.
    """
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
    """
    Handles keyboard events.
    Calls next_paper() or delete_last_timestamp() based on the key pressed.
    Stops the listener if the ESC key is pressed.
    """
    if key == keyboard.KeyCode.from_char(next_hotkey):
        next_paper()
    elif key == keyboard.KeyCode.from_char(delete_hotkey):
        delete_last_timestamp()
    elif key == keyboard.Key.esc:
        return False  # Stop listener

def get_existing_timestamp_files():
    """
    Scans the directory for timestamp files and returns them sorted by part number.
    Returns: List of filenames sorted by their part number
    """
    # Find all files matching the pattern
    files = glob.glob('timestamps/timestamps_part*.txt')
    
    # Extract the part number from each filename and sort
    def get_part_number(filename):
        try:
            return int(filename.split('part')[1].split('.')[0])
        except (IndexError, ValueError):
            return 0
    
    return sorted(files, key=get_part_number)

def check_last_timestamp(timestamp_file, links):
    """
    Checks if the last timestamp in the file corresponds to a link in the current links list.
    Args:
        timestamp_file (str): Path to the timestamp file
        links (list): List of tuples (title, link) from links.txt
    Returns:
        tuple: (bool: matches current links, int: index of next link to process)
    """
    # Extract just the links from the list of tuples
    link_only_list = [link for title, link in links]

    try:
        with open(timestamp_file, 'r') as f:
            lines = f.readlines()
            if not lines:
                return False, 0
            
            prev_file_links = []
            for line in lines:
                # Extract the link
                prev_file_links.append(line.strip().split()[-1])
                # extracting title would be more confusing bc at some point in these scripts i mess with the titles
            
            for prev_link in prev_file_links:
                if prev_link not in link_only_list:
                    return False, 0
            
            return True, link_only_list.index(prev_link) + 1
            
    except FileNotFoundError:
        return False, 0

def prompt_delete_old_files(files):
    """
    Prompts the user to confirm deletion of old timestamp files.
    Args:
        files (list): List of old timestamp files to delete
    """
    if not files:
        return

    print("Old timestamp files detected:")
    for file in files:
        print(f" - {file}")

    confirm = input("Do you want to delete these files? (y/n): ").strip().lower()
    if confirm == 'y':
        for file in files:
            try:
                os.remove(file)
                print(f"Deleted {file}")
            except OSError as e:
                print(f"Error deleting {file}: {e}")
    else:
        print("Old files not deleted.")

def create_new_timestamp_file(n):
    """
    Creates a new timestamp file for the current session.
    Args:
        n (int): The part number for the new file
    Returns:
        str: The filename of the new timestamp file
    """
    filename = f'timestamps/timestamps_part{n}.txt'
    with open(filename, 'w') as f:
        f.write("")  # Create an empty file
    print(f"Created new timestamp file: {filename}")
    return filename

# Read links from file and populate the links list
with open(links_file, 'r') as file:
    for line in file:
        line = line.strip()
        try:
            title, link = line.split(' | ')
            links.append((title, link))
        except ValueError:
            print(f"Invalid line format: {line}")

# Check if any links were found
if not links:
    print("No links found in links.txt")
    exit()

# Determine the starting point for the session
existing_files = get_existing_timestamp_files()
if existing_files:
    latest_file = existing_files[-1]
    matches, next_index = check_last_timestamp(latest_file, links)
    if matches:
        print(f"Continuing from {latest_file}, starting with link index {next_index}.")
        current_link_index = next_index
        new_file_number = int(latest_file.split('part')[1].split('.')[0]) + 1
    else:
        prompt_delete_old_files(existing_files)
        current_link_index = 0
        new_file_number = 1
else:
    current_link_index = 0
    new_file_number = 1

# Create a new timestamp file for the session
timestamps_file = create_new_timestamp_file(new_file_number)

# Instructions for the user
print("The first link(s) will be opened and timer will be started when you first hit the `next_hotkey` as defined in config.py")
print("Subsequent next_hotkey presses will record timestamps and open the next link(s).")
print("Triggers of the `delete_hotkey` as defined in config.py will delete the last line from timestamps.txt")
print("Press ESC to exit the program.")

# Start listening for keyboard events
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Program ended.")