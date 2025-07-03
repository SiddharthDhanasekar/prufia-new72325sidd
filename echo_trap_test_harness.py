import json
import os
# Load Echo and trap bank modules
from app.services.ai_engine.echo_scoring_clean import echo_decision


file_path = "app/services/ai_engine/Trust_Fingerprint_Bank"

try:
    with open(os.path.join(file_path, "ai_wall_trap_bank.json"), "r") as f:
        traps = json.load(f)
except Exception as e:
    raise Exception(f"Error reading file {file_path}: {str(e)}")



# Known mimic profile: AI Test 3
ai_test_3_traits = {
    "SF": 35.59,
    "PF": 34.62,
    "EB": 100,
    "SM": 40,
    "TT": 50,
    "MC": 84.17,
    "PGFI": 11.2,
}

# Directly test each trap to confirm which ones should match
def evaluate_traps(traits):
    matches = []
    for cluster in traps:
        name = cluster.get("cluster", "Unnamed")
        rules = cluster.get("rules", {})
        match = True
        for key, value in rules.items():
            if key.endswith("_min") and traits.get(key[:-4], 0) < value:
                match = False
            elif key.endswith("_max") and traits.get(key[:-4], 0) > value:
                match = False
            elif "_range" in key:
                field = key.split("_range")[0]
                min_v, max_v = value
                if not (min_v <= traits.get(field, 0) <= max_v):
                    match = False
            elif key.endswith("_exact"):
                if traits.get(key[:-6], None) != value:
                    match = False
        if match:
            matches.append(name)
    return matches

if __name__ == "__main__":
    echo_result = echo_decision(ai_test_3_traits)
    # trap_hits = evaluate_traps(ai_test_3_traits)

    print("Echo Final Result:", echo_result)
    # print("Matched Trap Clusters:", trap_hits if trap_hits else "None")
