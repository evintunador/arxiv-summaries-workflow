import webbrowser
import time

# Define the path to the file with links
file_path = 'links.txt'

# Open the file and read the links
with open(file_path, 'r') as file:
    for line in file:
        # Strip whitespace and newline characters
        line = line.strip()

        # isolate links
        title, link1, link2 = line.split(' | ')
        print(f'{title} |{link1}|{link2}|')
        # Check if the line is not empty
        if link1 or link2:
            webbrowser.open(link2)
            time.sleep(2)
            webbrowser.open(link1)
            time.sleep(2)
        else:
            print("Empty or invalid line detected.")

# Inform the user that the process is complete
print("All links have been opened in the browser.")
