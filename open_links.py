import webbrowser
import time

# Define the path to the file with links
file_path = 'bytez_links.txt'

# Open the file and read the links
with open(file_path, 'r') as file:
    for line in file:
        # Strip whitespace and newline characters
        link = line.strip()
        # Check if the line is not empty
        if link:
            webbrowser.open(link)
            time.sleep(2)
        else:
            print("Empty or invalid line detected.")

# Inform the user that the process is complete
print("All links have been opened in the browser.")
