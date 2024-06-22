import os
import re
import requests
import arxiv
import sys
import csv
from datetime import datetime

def download_pdf(url, filepath):
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)

def add_to_links_file(title, arxiv_url):
    line = f'{title} | {arxiv_url}'
    try:
        with open('links.txt', 'r') as file:
            existing_lines = file.readlines()
            if any(line.strip() == l.strip() for l in existing_lines):
                print(f'Line already exists in links.txt - Skipping')
                return
    except FileNotFoundError:
        pass

    with open('links.txt', 'a') as file:
        file.write(line + '\n')
    print(f"Added to links.txt: {line}")

def add_to_csv_file(title, arxiv_url, published_date):
    csv_file_seen = "papers_seen.csv"
    csv_file_downloaded = "papers_downloaded.csv"
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # Initialize CSV file with headers if it doesn't exist
    if not os.path.isfile(csv_file_seen):
        with open(csv_file_seen, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "ArXiv Link", "Paper Date", "Date Added"])
    if not os.path.isfile(csv_file_downloaded):
        with open(csv_file_downloaded, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "ArXiv Link", "Paper Date", "Date Added"])
    
    # Write to CSVs
    with open(csv_file_seen, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([title, arxiv_url, published_date, today_date])
    print(f"Added to {csv_file_seen}: {title}")
    with open(csv_file_downloaded, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([title, arxiv_url, published_date, today_date])
    print(f"Added to {csv_file_downloaded}: {title}")

def process_arxiv_url(arxiv_url):
    # Extract the arXiv ID from the URL
    arxiv_id = re.sub(r'v\d+$', '', arxiv_url.split('/')[-1])
    search = arxiv.Search(id_list=[arxiv_id])
    paper = next(arxiv.Client().results(search))

    # Create a valid filename from the paper title
    safe_title = re.sub(r'[<>:"/\\|?*]', ' -', paper.title)  # Replace invalid filename characters
    filename = f"{safe_title}.pdf"
    filepath = os.path.join("pdfs", filename)

    # Download the PDF
    download_pdf(paper.pdf_url, filepath)
    print(f"Downloaded: {filepath}")

    # Add to links.txt
    add_to_links_file(safe_title, arxiv_url)

    # Add to CSV files
    add_to_csv_file(safe_title, arxiv_url, paper.published.date())

def main(arxiv_urls):
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")

    for arxiv_url in arxiv_urls:
        process_arxiv_url(arxiv_url)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_arxiv.py <arxiv_url_1> <arxiv_url_2> ... <arxiv_url_n>")
    else:
        main(sys.argv[1:])



