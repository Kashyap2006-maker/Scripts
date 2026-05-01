import json
import csv

# --- Configuration ---
INPUT_JSON = "input.json"    # Path to your JSON file
OUTPUT_CSV = "output.csv"    # Path to save the CSV

def json_to_csv(json_path, csv_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not data:
        print("No data found in JSON.")
        return
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"CSV saved to {csv_path}")

if __name__ == "__main__":
    json_to_csv(INPUT_JSON, OUTPUT_CSV)
