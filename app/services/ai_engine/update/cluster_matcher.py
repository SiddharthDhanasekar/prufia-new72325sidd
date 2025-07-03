
# cluster_matcher.py
# PRUFIA Cluster Wall Matcher – Tiered Block Matching
# Matches input metrics against pre-defined AI/mimic clusters

# Example cluster definitions (PLACEHOLDERS)
CLUSTER_DATABASE = {
    "Cluster 4A": {"PF": "<2", "EB": ">95"},
    "Cluster 7B": {"SM": "==0", "MC": ">90"},
    "Cluster 3C": {"CharTransitionEntropy": "<45", "SyntacticChaos": ">88"},
    "Cluster 9X": {"CompressionResistance": "<50", "FrequencyDeviation": ">80"},
}

def evaluate_condition(value, condition):
    if condition.startswith("<"):
        return value < float(condition[1:])
    elif condition.startswith(">"):
        return value > float(condition[1:])
    elif condition.startswith("=="):
        return value == float(condition[2:])
    return False

def cluster_matcher(metrics):
    matched_clusters = []

    for cluster_name, conditions in CLUSTER_DATABASE.items():
        if all(evaluate_condition(metrics.get(key, 0), rule) for key, rule in conditions.items()):
            matched_clusters.append(cluster_name)

    return {
        'matched_clusters': matched_clusters,
        'status': 'BLOCKED' if matched_clusters else 'UNMATCHED'
    }

if __name__ == "__main__":
    test_metrics = {
        'PF': 1.4,
        'EB': 96.2,
        'SM': 0,
        'MC': 91.7,
        'CharTransitionEntropy': 39.4,
        'SyntacticChaos': 92.5,
        'CompressionResistance': 45.0,
        'FrequencyDeviation': 85.2
    }

    result = cluster_matcher(test_metrics)
    print(result)
