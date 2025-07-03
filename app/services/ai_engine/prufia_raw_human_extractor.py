# prufia_raw_human_extractor.py
from app.services.ai_engine.score import (
    calculate_sf,
    calculate_sm,
    calculate_pf,
    calculate_eb,
    calculate_tt,
    calculate_mc,
    calculate_pgfi,
)

def extract_raw_metrics(text):
   
    return {
        "SF": calculate_sf(text),
        "SM": calculate_sm(text),
        "PF": calculate_pf(text),
        "EB": calculate_eb(text),
        "TT": calculate_tt(text),
        "MC": calculate_mc(text),
        "PGFI": calculate_pgfi(text),

    }

# Example usage:
if __name__ == "__main__":
    sample_text = """This is a sample human-authored document for extraction."""
    metrics = extract_raw_metrics(sample_text)
    for key, value in metrics.items():
        print(f"{key}: {value}")
