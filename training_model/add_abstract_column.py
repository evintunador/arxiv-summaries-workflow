import arxiv
import csv
import os
# from tqdm import tqdm

# Define the path to the dataset you want to update
csv_file = "papers_dataset.csv"

# Create an arXiv client
client = arxiv.Client(
    page_size=1,
    delay_seconds=5.0,
    num_retries=50
)

# Function to retrieve the abstract of a paper using arXiv API
def fetch_abstract(arxiv_id):
    search = arxiv.Search(id_list=[arxiv_id])
    result = next(client.results(search), None)
    if result:
        return result.summary
    else:
        return "Abstract not found"

# Check if the 'Abstract' column exists; if not, add it to the CSV
if not os.path.isfile(csv_file):
    raise FileNotFoundError(f"{csv_file} does not exist.")

# Read the current contents of the CSV
papers = []
with open(csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames
    papers = list(reader)

# Check if the 'Abstract' column exists in the CSV
if 'Abstract' not in fieldnames:
    fieldnames.append('Abstract')

# Fetch abstracts and add to the CSV dataset
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    
    tot = len(papers)
    for i, paper in enumerate(papers):#tqdm(papers):
        arxiv_url = paper['ArXiv Link']
        arxiv_id = arxiv_url.split('/')[-1]  # Extract arXiv ID from the link
        if 'Abstract' not in paper or not paper['Abstract']:
            paper['Abstract'] = fetch_abstract(arxiv_id)  # Fetch abstract if missing
        writer.writerow(paper)
        print(f'finished row {i} of {tot}')

print(f"Abstracts successfully added to {csv_file}")

