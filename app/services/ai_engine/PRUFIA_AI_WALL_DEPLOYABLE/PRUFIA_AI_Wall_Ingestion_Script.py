import os
import csv
from app.services.ai_engine.prufia_raw_human_extractor import extract_raw_metrics

INPUT_FOLDER = "ai_test_docs"
OUTPUT_FILE = "trait_results.csv"

def ingest_and_extract():
    results = []
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".txt"):
            filepath = os.path.join(INPUT_FOLDER, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            metrics = extract_raw_metrics(text)
            metrics["filename"] = filename
            results.append(metrics)

    fieldnames = ["filename", "sf", "sm", "pf", "eb", "tt", "mc", "pgfi"]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    ingest_and_extract()
