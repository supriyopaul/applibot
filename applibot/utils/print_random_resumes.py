import csv
import argparse
import random

def print_random_resumes(file_path: str, num_resumes: int):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Read all rows into a list
        rows = list(reader)
        
        # If the file has fewer resumes than requested, print a warning and adjust the number
        if len(rows) < num_resumes:
            print(f"Warning: The file only contains {len(rows)} resumes. Adjusting the number to {len(rows)}.")
            num_resumes = len(rows)
        
        # Select random rows
        selected_rows = random.sample(rows, num_resumes)
        
        # Print the selected rows
        for i, row in enumerate(selected_rows, start=1):
            print(f"{row['Resume']}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print random resumes from a CSV file.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file containing resumes.')
    parser.add_argument('-n', '--num_resumes', type=int, default=1, help='Number of random resumes to print.')
    
    args = parser.parse_args()
    
    print_random_resumes(args.file_path, args.num_resumes)
