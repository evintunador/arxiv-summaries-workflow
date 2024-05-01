import arxiv
import time
from datetime import datetime, timedelta
import textwrap
import tkinter as tk
from tkinter import ttk
import requests
from threading import Thread
from config import restrict_to_most_recent, max_results
import os
import re


if not os.path.exists("pdfs"):
    os.makedirs("pdfs")

# Python function to read words from a text file and store each line as a string in a list.
def read_lines_from_file(filename):
    """
    Read lines from a text file and store them as strings in a list.
    
    Parameters:
    - filename (str): The name of the text file to read from.
    
    Returns:
    - List[str]: A list containing each line from the text file as a string.
    """
    lines = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                lines.append(line.strip())  # Remove leading/trailing whitespace
    except FileNotFoundError:
        print("File not found: {filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return lines



# Most Recent Days Checker. Sometimes arxiv posts papers w multiple dates on one day so we really just want to make sure we're checking whatever came out since we last queried
with open('most_recent_day_searched.txt', 'r') as file:
    most_recent = file.read()
print(f'most recent day searched: {most_recent}')
try:
    most_recent_check = datetime.strptime(most_recent, '%Y-%m-%d').date()
except ValueError:
    most_recent_check = datetime.now().date() - timedelta(days=2)

    with open('most_recent_day_searched.txt', 'w') as file:
            file.write(most_recent_check.strftime('%Y-%m-%d'))

    print("No date listed in most_recent_day_searched.txt. Two days ago's date inserted, but arXiv frequently publishes papers with older dates on a given day (yes it's confusing) so you may want to edit the text file to an even earlier date. If today is a weekend then the script may return nothing.")



# search terms
include_terms = read_lines_from_file("search_terms_include.txt")
exclude_terms = read_lines_from_file("search_terms_exclude.txt")

include, exclude = 'all:"', 'all:"'
for term in include_terms: 
    include += term + '" OR all:"'
for term in exclude_terms: 
    exclude += term + '" OR all:"'
include = include[:-9]
exclude = exclude[:-9]
print("\nIncluded Terms:\n", include)
print("\nExcluded Terms:\n", exclude)

categories = "cat:cs.AI OR cat:stat.ML OR cat:cs.CL OR cat:cs.CV OR cat:cs.LG OR cat:cs.MA OR cat:cs.NE OR cat:cs.HC OR cat:cs.MA" # 
if len(include_terms) > 0 & len(exclude_terms) > 0:
    query = f'({categories}) AND ({include}) ANDNOT ({exclude})'
elif len(include_terms) > 0:
    query = f'({categories}) AND ({include})'
elif len(exclude_terms) > 0:
    query = f'({categories}) ANDNOT ({exclude})'
else:
    query = categories
print("\nQuery:\n", query)


client = arxiv.Client(
  page_size = 1,
  delay_seconds = 5.0,
  num_retries = 50
)
# Define the search parameters
search = arxiv.Search(
    query = query,
    max_results=max_results,  
    sort_by=arxiv.SortCriterion.SubmittedDate,  # Sort by submission date
    sort_order=arxiv.SortOrder.Descending  # In descending order, so the most recent articles come first
)

results = client.results(search)
papers = []


def safe_iterator(iterable):
    it = iter(iterable)  # Get an iterator object from the iterable
    while True:
        try:
            yield next(it)  # Yield the next item from the iterator
        except StopIteration:
            print("got to StopIteration")
            break  # StopIteration means there are no more items
        except Exception as e:
            # Handle the exception or simply pass to skip to the next item
            pass


i = 0
for result in safe_iterator(results):

    if i == 0:
        new_most_recent = result.published.date()#.strftime('%Y-%m-%d')
    
    if restrict_to_most_recent & (result.published.date() < most_recent_check):
        print(f"GOT TO MOST RECENT DATE RESET: {result.published.date()} <= {most_recent_check}")
        # Write new_most_recent to .txt file
        # we only want to do that here bc if restrict_to_most_recent=False then we don't want to change the value
        with open('most_recent_day_searched.txt', 'w') as file:
            file.write(new_most_recent.strftime('%Y-%m-%d'))

        # In case you need to run it back
        print(f"If you need to run back the most recent check, then edit the date in most_recent_day_searched.txt to be '{most_recent_check.strftime('%Y-%m-%d')}'.")

        # bc we've hit files we likely already downloaded before we'll end here
        break
    
    try:
        papers.append({"title": result.title, "url": result.pdf_url})
        print('Title: ', result.title)
        print('Publishing date ', result.published)
        #print(result.categories)
        #print('Abstract: ', textwrap.fill(result.summary, width=220))
        print('PDF URL: ', result.pdf_url)
        #print('DOI ', result.doi)
    except UnexpectedEmptyPageError:
        continue
    
    #print('\n')

    # Sleep for 5 seconds to avoid overloading the server
    time.sleep(5)
    i += 1

print(f"Total papers: {i}")



# Function to download PDF from arXiv
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)

def on_button_click(url, filename):
    # Constructing bytez.com URL from arXiv URL
    arxiv_id = re.sub(r'v\d+$', '', url.split('/')[-1])
    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
    arxiv_id_no_version = arxiv_id.split('v')[0]
    bytez_url = f"https://bytez.com/docs/arxiv/{arxiv_id_no_version}/paper"
    line = f'{filename[5:-4]} | {bytez_url} | {arxiv_url}'

    # Duplicate check:
    try:
        with open('links.txt', 'r') as file:
            existing_lines = file.readlines()
            if any(l.strip() == line for l in existing_lines):
                print(f'Line already exists in chapters.txt - Skipping')
                return  # Skip if the URL already exists
    except FileNotFoundError:
        pass  # Ignore if the file doesn't exist yet

    # Write the bytez.com URL to a text file
    with open('links.txt', 'a') as file:
        file.write(line + '\n')

    # Download the PDF in a new thread
    thread = Thread(target=download_pdf, args=(url, filename))
    thread.start()





# Create the main window
root = tk.Tk()
root.title("arXiv Paper Downloader")

# Create a canvas and a vertical scrollbar
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = ttk.Frame(canvas)

# Configure canvas and add the frame to it
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

for i, paper in enumerate(papers):
    #label = ttk.Label(frame, text=paper["title"])
    #label.grid(row=i, column=0, sticky=tk.W)
    #print(paper['url'])
    button = ttk.Button(frame, text=paper['title'], command=lambda url=paper['url'], fn=f"pdfs/{paper['title']}.pdf".replace(":", " -"): on_button_click(url, fn))
    button.grid(row=i, column=1)

# Update frame size and set canvas scroll region
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Place canvas and scrollbar in the GUI
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Enable resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()