
# dynamic_cluster_matcher.py
# PRUFIA Cluster Wall Matcher (Dynamic Logic Edition)
# Loads cluster logic strings and evaluates them against document metrics

import json

def safe_eval(expr, metrics):
    try:
        # Evaluate the expression safely using only the metrics as variables
        return eval(expr, {"__builtins__": {}}, metrics)
    except Exception as e:
        return False

def load_clusters(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data.get("clusters", [])

def match_clusters(metrics, clusters):
    matched = []
    for cluster in clusters:
        logic = cluster.get("logic", "")
        if safe_eval(logic, metrics):
            matched.append({
                "name": cluster.get("name", "Unnamed Cluster"),
                "description": cluster.get("description", ""),
                "logic": logic
            })
    return {
        "matched_clusters": matched,
        "status": "BLOCKED" if matched else "UNMATCHED",
        "match_count": len(matched)
    }

if __name__ == "__main__":
    # Sample input (replace with real document metrics)
    sample_metrics = {
        "sentence_variation": 100,
        "vocabulary_entropy": 97.8,
        "eb": 0.68,
        "structure_consistency": 94,
        "vocab_diversity": 0.91,
        "pgfi": 5.5,
        "punctuation_rhythm": 12,
        "mc": 52,
        "info_density": 0.48
    }

    # Load sample clusters from external JSON
    clusters = load_clusters("Updated_3_Echo_Cluster_30Layer_Strategy.json")
    result = match_clusters(sample_metrics, clusters)
    print(json.dumps(result, indent=2))
