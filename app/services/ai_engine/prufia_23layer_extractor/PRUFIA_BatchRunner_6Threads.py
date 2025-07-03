
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.services.ai_engine.prufia_23layer_extractor.prufia_extractor_23layers_plug_and_play import extract_23_layer_profile

INPUT_FOLDER = "input_docs"
OUTPUT_FOLDER = "output_profiles"
THREADS = 6  # Set to 6 for safe Mac performance

def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        result = extract_23_layer_profile(text)
        filename = os.path.basename(file_path).replace(".txt", ".json")
        out_path = os.path.join(OUTPUT_FOLDER, filename)
        with open(out_path, "w", encoding="utf-8") as out:
            json.dump(result, out, indent=2)
        return f"✅ Processed: {file_path}"
    except Exception as e:
        return f"❌ Error: {file_path} — {str(e)}"

def run_batch_extraction():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    files = [os.path.join(INPUT_FOLDER, f) for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")]

    print(f"📂 Found {len(files)} documents. Starting extraction with {THREADS} threads...")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(process_file, file): file for file in files}
        for future in as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    run_batch_extraction()
