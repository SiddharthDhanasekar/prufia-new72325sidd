import os
import json

CLUSTER_RULES_DIR = "app/services/ai_engine/update/cluster_rules"

def load_cluster_rules():
    rules = []
    for file_name in os.listdir(CLUSTER_RULES_DIR):
        if file_name.endswith(".json"):
            path = os.path.join(CLUSTER_RULES_DIR, file_name)
            with open(path, "r") as f:
                rule = json.load(f)
                rules.append(rule)
    return rules

def check_condition(value, min_val=None, max_val=None):
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True

def evaluate_rule(rule, traits):
    logic = rule.get("logic", "AND")
    result = rule.get("result", "mismatch")
    fail_result = rule.get("failure_result", "mismatch")

    # Handle all 19 supported traits
    trait_keys = [
        "SyntheticChaos", "StructureConsistency", "PGFI", "TT", "MC", "PF",
        "SF", "SM", "EB", "VocabularyEntropy", "TemporalTempo", "SentenceVariation",
        "CharTransitionEntropy", "CompressionResistance", "FrequencyDeviation",
        "micro_rhythm_variance", "PGFIDisplay", "PunctuationRhythm", "ShellReuse"
    ]

    conditions = []
    for key in trait_keys:
        min_key = f"{key}_min"
        max_key = f"{key}_max"
        min_val = rule.get("conditions").get(min_key)
        max_val = rule.get("conditions").get(max_key)
        if min_val is not None or max_val is not None:
            trait_val = traits.get(key)

            if trait_val is None:
                conditions.append(False)
            else:
                conditions.append(check_condition(trait_val, min_val, max_val))

    if logic == "CUSTOM":
        required = rule.get("required_matches", len(conditions))
        return result if sum(conditions) >= required else fail_result

    if logic == "AND":
        return result if all(conditions) else fail_result

    return "mismatch"

def run_all_clusters(traits):
    rules = load_cluster_rules()
    results = []
    for rule in rules:
        outcome = evaluate_rule(rule, traits)
        results.append({
            "rule": rule.get("rule_name", "unknown"),
            "outcome": outcome
        })
    return results