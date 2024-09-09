import arxiv
import time

# Simple query for recent computer science papers
query = "cat:cs.AI"

# Create a client
client = arxiv.Client(
    page_size=5,
    delay_seconds=3.0,
    num_retries=3
)

# Define the search parameters
search = arxiv.Search(
    query=query,
    max_results=5,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
)

print("Starting arXiv API test...")

try:
    results = client.results(search)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.title}")
        print(f"   Published: {result.published.date()}")
        print(f"   arXiv ID: {result.entry_id}")
        print()
        
        # Small delay to be nice to the API
        time.sleep(1)
    
    print("Test completed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

print("Test script finished.")