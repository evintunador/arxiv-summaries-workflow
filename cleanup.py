import os
import shutil
import glob
import csv
from config import obsidian_vault_location, obsidian_vault_attachments_location, frontmatter_lines, send_to_obsidian

def make_folder_if_none(path):  
    if not os.path.exists(path):
        os.makedirs(path)

make_folder_if_none("pdfs-to-summarize")

def update_papers_kept_csv(base_filename):
    downloaded_csv = "papers_downloaded.csv"
    kept_csv = "papers_kept.csv"
    
    # Initialize the papers_kept.csv with headers if it doesn't exist
    if not os.path.isfile(kept_csv):
        with open(kept_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "ArXiv Link", "Paper Date", "Date Added"])

    # Read the row from papers_downloaded.csv
    row_to_add = None
    with open(downloaded_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # skip the header
        for row in reader:
            if row and row[0] == base_filename:  # Check if row is not empty and matches base_filename
                row_to_add = row
                break
    
    # Add the row to papers_kept.csv
    if row_to_add:
        with open(kept_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row_to_add)
        print(f"Added to {kept_csv}: {base_filename}")
    else:
        print(f"Error: Could not find {base_filename} in {downloaded_csv}")

def get_link(base_filename):
    with open('links.txt', 'r') as f:
        for line in f:
            title, link = line.strip().split(' | ')
            if title.lower() in base_filename.lower():
                return link
    return None

def process_files(pdf_folder, md_final_folder, pdf_final_folder):
    
    # Get all text files in the specified folder
    pdf_files = glob.glob(os.path.join(pdf_folder, '*.pdf'))

    count = 0
    for pdf_file in pdf_files:
        count += 1

        # Get the base filename without the extension
        base_filename = os.path.basename(pdf_file).rsplit('.', 1)[0]

        link = get_link(base_filename)
        
        md_file = os.path.join('pdfs-to-summarize', base_filename.title() + ' (pdf).md')
        with open(md_file, 'w') as f_out:
            f_out.write(f"{frontmatter_lines}")
            if link:
                f_out.write(f"Link: [{link}]({link})")
            f_out.write(f"\n\n![[{base_filename}.pdf]]")
            
        # Move the .md file to the final folder. Usually this error comes up because you tried to run the scrip twice
        try:
            shutil.move(md_file, md_final_folder)
        except shutil.Error as e:
            print(f"Error: {e}. Skipping file {md_file} because it already exists in the Obsidian Vault.")

        # Move the .pdf files to the final folder. the exception exists cuz sometimes i get antsy and add the pdf too soon
        try:
            shutil.move(pdf_file, pdf_final_folder)
        except shutil.Error as e:
            print(f"Error: {e}. Skipping file {pdf_file} because it already exists in the Obsidian Vault.")

        # Update papers_kept.csv
        update_papers_kept_csv(base_filename)

    print(f'{count} files added to vault assuming no skip errors')

if send_to_obsidian:
    # Call the function with your specified folders
    process_files('pdfs-to-summarize', 
                    obsidian_vault_location,
                    obsidian_vault_attachments_location)


def delete_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Couldn't delete {filename} file from {folder_path} folder bc Error occurred: \n{e}")

delete_all_files_in_folder("pdfs-to-summarize")
delete_all_files_in_folder("pdfs")
delete_all_files_in_folder("timestamps")

try:
    if os.path.isfile('links.txt'):
        os.remove('links.txt')
except Exception as e:
    print(f"Couldn't delete links.txt bc Error occurred: \n{e}")

try:
    if os.path.isfile('timestamps.txt'):
        os.remove('timestamps.txt')
except Exception as e:
    print(f"Couldn't delete timestamps.txt bc Error occurred: \n{e}")

try:
    if os.path.isfile('trimmed_timestamps.txt'):
        os.remove('trimmed_timestamps.txt')
except Exception as e:
    print(f"Couldn't delete trimmed_timestamps.txt bc Error occurred: \n{e}")

try:
    if os.path.isfile('timestamps_adjusted.txt'):
        os.remove('timestamps_adjusted.txt')
except Exception as e:
    print(f"Couldn't delete timestamps_adjusted.txt bc Error occurred: \n{e}")

try:
    if os.path.isfile('newsletter.txt'):
        os.remove('newsletter.txt')
except Exception as e:
    print(f"Couldn't delete newsletter.txt bc Error occurred: \n{e}")

try:
    if os.path.isfile('newsletter_podcast.mp3'):
        os.remove('newsletter_podcast.mp3')
except Exception as e:
    print(f"Couldn't delete newsletter_podcast.mp3 bc Error occurred: \n{e}")