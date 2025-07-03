import json
import os
import operator
import re

# Load cluster banks

file_path = "app/services/ai_engine/Trust_Fingerprint_Bank"
try:
    
    with open(os.path.join(file_path, "human_trust_fingerprint_bank.json"), "r") as f:
        human_clusters = json.load(f)
except Exception as e:
    raise Exception(f"Error reading file {file_path}: {str(e)}")

try:
    with open(os.path.join(file_path, "ai_wall_trap_bank.json"), "r") as f:
        ai_clusters = json.load(f)
except Exception as e:
    raise Exception(f"Error reading file {file_path}: {str(e)}")


# def matches_cluster(traits, rules):
#     for key, value in rules.items():
#         if key.endswith("_min"):
#             metric = key[:-4]
#             if traits.get(metric, float("-inf")) < value:
#                 return False
#         elif key.endswith("_max"):
#             metric = key[:-4]
#             if traits.get(metric, float("inf")) > value:
#                 return False
#         elif key.endswith("_exact"):
#             metric = key[:-6]
#             if traits.get(metric) != value:
#                 return False
#         elif key.endswith("_range"):
#             metric = key[:-6]
#             if not (value[0] <= traits.get(metric, 0) <= value[1]):
#                 return False
#         else:
#             return False  # Unsupported rule type
#     return True


def evaluate_logic_string(logic_str, traits):
    try:
        # Replace metric names in the logic string with their actual values
        for metric, value in traits.items():
            logic_str = logic_str.replace(metric, str(value))
        return eval(logic_str)
    except Exception as e:
        print("Logic evaluation error:", e)
        return False

def echo_decision(traits):
    # Step 1: Check Human Trust Clusters first
    for cluster in human_clusters.get("clusters", []):
        logic = cluster.get("logic", "")
        if evaluate_logic_string(logic, traits):
            return "green"

    # Step 2: Check AI Trap Clusters
    # for cluster in ai_clusters.get("clusters", []):
    #     logic = cluster.get("logic", "")
    #     if evaluate_logic_string(logic, traits):
    #         return "red"

    # Step 3: No match
    return "gray"

def final_prufia_decision(echo_score, mdt_passed=False, drift_passed=False, fusion_passed=False):
    """
    Evaluates the final decision score based on Echo result and optional validators MDT, Drift, and Fusion.

    Parameters:
    - echo_score (str): 'Green', 'Red', or 'Gray'
    - mdt_passed (bool): True if MDT validator passed
    - drift_passed (bool): True if Drift validator passed
    - fusion_passed (bool): True if Fusion validator passed

    Returns:
    - final_score (str): 'Green', 'Red'
    - reason (str): Explanation of final decision
    """
    if echo_score.lower() == 'green':
        return 'green', 'Echo locked. No override allowed.'

    elif echo_score.lower() == 'red':
        if mdt_passed and drift_passed and fusion_passed:
            return 'green', 'Echo failed but rescued by MDT/Drift/Fusion.'
        else:
            return 'red', 'Echo failed and validators confirm failure.'

    return 'red', 'Unexpected input state.'


def check_htl(traits):
    """
    Human Trust Layer - clears deep, diverse human authorship. Tiered structure.
    """
    if (
        traits.get("EB", 0) == 0 and
        85 <= traits.get("MC", 0) <= 92 and
        traits.get("PF", 0) >= 10 and
        traits.get("TT", 0) >= 40 and
        traits.get("Sentence_Variation", "High") == "Low" and
        traits.get("SM", 0) == 0 and
        traits.get("revision_artifacts", False) == True and
        traits.get("metacognitive_awareness", False) == True
    ):
        return "HTL Tier 1"
    elif (
        traits.get("SF", 0) > 70 and
        traits.get("SM", 0) > 45 and
        traits.get("MC", 0) < 92 and
        traits.get("emotion_gradient", 0) > 3 and
        traits.get("discourse_flow", 0) > 7
    ):
        return "HTL Tier 2"
    elif (
        traits.get("SF", 0) > 35 and
        traits.get("TT", 0) > 40 and
        traits.get("MC", 0) > 95 and
        traits.get("PGFI", 0) > 10 and
        traits.get("attention_fragmentation", False) == True
    ):
        return "HTL Tier 3"
    else:
        return False

    
def check_mdt(traits):
    """
    Micro Discrepancy Tracker - detects mimic-level inconsistency.
    Combines stylometric irregularity with human-behavioral absence.
    """
    return (
        traits.get("SM", 0) < 35 and
        traits.get("MC", 0) > 92 and
        traits.get("EB", 0) == 100 and
        traits.get("TT", 0) < 40 and
        traits.get("attention_fragmentation", False) == False and
        traits.get("revision_artifacts", False) == False
    )

def check_drift(traits):
    """
    Drift Detection - flags documents lacking natural human pacing and information variation.
    """
    return (
        traits.get("TT", 0) < 30 and
        traits.get("PF", 0) > 35 and
        traits.get("SF", 0) > 50 and
        traits.get("MC", 0) > 90 and
        traits.get("info_density", 0) > 9 and
        traits.get("context_adaptation", False) == False
    )

def check_fusion(traits):
    """
    Fusion Layer - detects hybrid mimic patterns with rhythm, behavior, and concept overlap.
    """
    return (
        traits.get("SF", 0) > 55 and
        traits.get("PF", 0) > 30 and
        traits.get("SM", 0) > 45 and
        traits.get("PGFI", 0) < 15 and
        traits.get("creative_synthesis", False) == False and
        traits.get("domain_expertise", False) == False
    )




# Developer note:
# Call echo_decision(traits_dict) using real trait output from prufia_raw_human_extractor.py
# This module does not include placeholder or sample data.

def evaluate_logic_expression(expression, traits):
    # Define supported operators
    ops = {
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
    }

    # Tokenize the expression
    tokens = re.findall(r'\w+|>=|<=|!=|==|>|<|\(|\)|AND|OR', expression)

    def get_value(token):
        try:
            return float(token)
        except ValueError:
            return traits.get(token, None)

    def apply_op(op, a, b):
        if isinstance(a, str):
            a = get_value(a)
        if isinstance(b, str):
            b = get_value(b)
        return ops[op](a, b)

    def precedence(op):
        return 2 if op == "AND" else 1

    def eval_tokens(tokens):
        values = []
        ops_stack = []

        def apply():
            right = values.pop()
            left = values.pop()
            op = ops_stack.pop()
            values.append(left and right if op == "AND" else left or right)

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in ops:
                left = tokens[i - 1]
                right = tokens[i + 1]
                result = apply_op(token, left, right)
                values.append(result)
                i += 2
            elif token in ("AND", "OR"):
                while ops_stack and precedence(ops_stack[-1]) >= precedence(token):
                    apply()
                ops_stack.append(token)
                i += 1
            elif token == "(":
                start = i + 1
                depth = 1
                while depth > 0:
                    i += 1
                    if tokens[i] == "(":
                        depth += 1
                    elif tokens[i] == ")":
                        depth -= 1
                values.append(eval_tokens(tokens[start:i]))
                i += 1
            else:
                i += 1

        while ops_stack:
            apply()
        return values[0]

    return eval_tokens(tokens)

def matches_cluster(traits, cluster):
    logic = cluster.get("logic", "")
    return evaluate_logic_expression(logic, traits)