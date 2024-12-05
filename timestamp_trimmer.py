import os
from config import limit
import argparse

def calculate_total_characters(timestamps):
    return sum(len(timestamp) for timestamp in timestamps)

def trim_timestamps(timestamps, limit):
    # First try removing descriptions from timestamps with smallest time gaps
    while calculate_total_characters(timestamps) > limit:
        min_diff = float('inf')
        min_index = -1
        
        for i in range(len(timestamps) - 1):
            try:
                # Split into timestamp, title, and link
                parts = timestamps[i].split(' ')
                if len(parts) < 3:  # Skip if no title and link
                    continue
                    
                curr_time = parts[0]
                next_time = timestamps[i + 1].split(' ')[0]
                
                if ':' not in curr_time or ':' not in next_time:
                    continue
                    
                curr_minutes, curr_seconds = map(int, curr_time.split(':'))
                next_minutes, next_seconds = map(int, next_time.split(':'))
                curr_total_seconds = curr_minutes * 60 + curr_seconds
                next_total_seconds = next_minutes * 60 + next_seconds
                
                diff = next_total_seconds - curr_total_seconds
                if diff < min_diff and len(parts) > 2:  # Check if there's a title to remove
                    min_diff = diff
                    min_index = i
            except (ValueError, IndexError):
                continue
                
        if min_index != -1:
            # Keep timestamp and link, remove title
            parts = timestamps[min_index].split(' ')
            timestamp = parts[0]
            link = parts[-1]
            timestamps[min_index] = f"{timestamp} {link}"
        else:
            break  # No more timestamps to modify
            
    return timestamps

def main(timestamps_file):
    output_file = f"{timestamps_file}_trimmed.txt"

    # Check if timestamps.txt exists
    if not os.path.exists(timestamps_file):
        print(f"Error: {timestamps_file} does not exist.")
        return

    # Read existing timestamps
    with open(timestamps_file, "r") as f:
        timestamps = f.read().splitlines()

    # Trim timestamps
    global limit
    trimmed_timestamps = trim_timestamps(timestamps, limit)

    # Write trimmed timestamps to a new file
    with open(output_file, "w") as f:
        f.write("\n".join(trimmed_timestamps))

    print(f"Trimmed timestamps have been written to {output_file}")
    print(f"Total characters: {calculate_total_characters(trimmed_timestamps)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trimm the shortest (time length) youtube timestamps from a text file")
    parser.add_argument('timestamps_file', type=str, help='Path to the timestamps file.')
    args = parser.parse_args()
    main(args.timestamps_file)