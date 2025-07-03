import json
import os
from app.services.ai_engine.prufia_23layer_extractor.prufia_extractor_23layers_plug_and_play import extract_23_layer_profile
from app.services.ai_engine.prufia_final_extractor_10layer_trust_protocol import PrufiaExtractor10Layer
from app.services.ai_engine.score import (
    calculate_sf,
    calculate_sm,
    calculate_pf,
    calculate_eb,
    calculate_tt,
    calculate_mc,
    calculate_pgfi,
    calculate_kt_entropy,
    calculate_phrase_reuse_score,
    calculate_prufia_final_score,
    load_walls
)

MATCH_THRESHOLD = 2  # Minimum cluster lines to count as match

# Load cluster banks
file_path = "app/services/ai_engine/Trust_Fingerprint_Bank"
with open(os.path.join(file_path, "human_trust_fingerprint_bank.json"), "r") as f:
    human_clusters = json.load(f)
with open(os.path.join(file_path, "ai_wall_trap_bank.json"), "r") as f:
    ai_clusters = json.load(f)

def match_against_authentic_clusters(metrics):
    """
    Evaluates whether document matches any of the installed cluster patterns.
    Must match threshold rules inside the actual installed cluster JSON.
    """
    match_found = False
    for cluster in human_clusters:
        try:
            if eval(cluster['logic'], {}, metrics):
                match_found = True
                break
        except Exception:
            continue
    return match_found

# def run_dualwall_echo(document_text: str):
#     traits = extract_23_layer_profile(document_text)
    
#     human_hits = match_against_clusters(traits, human_clusters)
#     ai_hits = match_against_clusters(traits, ai_clusters)

#     if human_hits > 0 and ai_hits == 0:
#         return "GREEN", traits
#     elif ai_hits >= 2:
#         return "RED", traits
#     else:
#         return "GRAY", traits  # Not enough confidence for either side

def run_echo_decision_logic(document_text: str):
    # Step 1: Extract 23 core traits
    traits_23 = extract_23_layer_profile(document_text)  # includes sf, pf, eb, sm, tt, mc, pgfi (short codes)

    # Step 2: Extract 6 stylometric traits with long-form labels
    external_stylos = extract_6_stylo_traits(document_text)  # includes Sentence Variation, etc.

    # Step 3: Manually preserve both sets without overwriting
    unified_metrics = {}

    # Load all original 23-layer traits (short codes)
    for key in traits_23:
        unified_metrics[key] = traits_23[key]

    # Load all new 6 stylometric traits (long-form names)
    unified_metrics["sentence_variation"] = external_stylos["Sentence Variation"]
    unified_metrics["punctuation_rhythm"] = external_stylos["Punctuation Rhythm"]
    unified_metrics["vocabulary_entropy"] = external_stylos["Vocabulary Entropy"]
    unified_metrics["phrase_reuse"] = external_stylos["Phrase Reuse"]
    unified_metrics["structure_consistency"] = external_stylos["Structure Consistency"]
    unified_metrics["pgfi_display"] = external_stylos["PGFI-AI Mimicry"]  # renamed

    # Step 4: Run decision logic using all 29 traits
    result = detect_content_with_imperfection_analysis(unified_metrics)

    return result, unified_metrics

def step0_authentic_imperfection_analysis(metrics):
    perfect_combo_1 = (
        metrics['sentence_variation'] >= 99.5 and 
        metrics['vocabulary_entropy'] >= 98 and
        metrics['eb'] <= 0.70
    )
    absolute_perfection = (
        metrics['sentence_variation'] == 100 and 
        metrics['vocabulary_entropy'] >= 97.5
    )
    gaming_pattern = (
        metrics['sentence_variation'] >= 99 and
        metrics['vocabulary_entropy'] >= 96 and
        metrics['eb'] <= 0.71 and
        80 <= metrics['structure_consistency'] <= 85
    )
    perfection_count = sum([
        metrics['sentence_variation'] >= 95,
        metrics['vocabulary_entropy'] >= 95,
        metrics.get('structure_consistency', 0) >= 95,
        metrics.get('vocab_diversity', 0) >= 0.95
    ])
    triple_perfection = (perfection_count >= 3)
    suspicious_optimization = (
        metrics['sentence_variation'] >= 95 and
        metrics['vocabulary_entropy'] >= 90 and
        metrics['eb'] <= 0.75 and
        metrics['pgfi'] <= 6 and
        75 <= metrics['structure_consistency'] <= 90
    )
    if any([perfect_combo_1, absolute_perfection, gaming_pattern, triple_perfection, suspicious_optimization]):
        return "HUMANIZER_DETECTED"
    return "CONTINUE"

def step1_nuclear_ai_detection(metrics):
    obvious_ai_signatures = [
        metrics['eb'] > 0.90,
        metrics['structure_consistency'] > 95,
        metrics['vocab_diversity'] > 0.90,
        metrics['vocabulary_entropy'] < 30,
        metrics['punctuation_rhythm'] < 8,
        metrics.get('sent_len_dist', 0) > 7.5,
        (metrics['eb'] > 0.88 and metrics['structure_consistency'] > 95),
        (metrics['vocab_diversity'] > 0.88 and metrics['vocabulary_entropy'] < 35),
        (metrics['structure_consistency'] > 96 and metrics['vocabulary_entropy'] < 40)
    ]
    return "AI_DETECTED" if any(obvious_ai_signatures) else "CONTINUE"

def step2_human_authenticity_verification(metrics):
    patterns = [
        metrics['structure_consistency'] <= 75 or
        (metrics['vocabulary_entropy'] <= 85 and metrics['sentence_variation'] <= 90),
        metrics['eb'] <= 0.82 and
        metrics['structure_consistency'] <= 92 and
        metrics['vocab_diversity'] <= 0.85 and
        metrics['sentence_variation'] <= 95 and
        35 <= metrics['vocabulary_entropy'] <= 95,
        (metrics['sentence_variation'] >= 90 and metrics['structure_consistency'] <= 80) or
        (metrics['structure_consistency'] >= 88 and metrics['sentence_variation'] <= 70) or
        (metrics['eb'] >= 0.75 and metrics['structure_consistency'] >= 85 and metrics['vocabulary_entropy'] <= 80),
        metrics['punctuation_rhythm'] >= 15 and
        metrics['mc'] >= 50 and
        metrics['pgfi'] <= 10 and
        metrics['sentence_variation'] >= 25,
        metrics['sentence_variation'] >= 95 or
        metrics['vocabulary_entropy'] >= 98 or
        metrics['eb'] <= 0.70 or
        metrics['structure_consistency'] <= 80 or
        metrics['punctuation_rhythm'] >= 40 or
        (metrics['pgfi'] <= 5.0 and metrics['eb'] <= 0.80)
    ]
    return "HUMAN_PROTECTED" if any(patterns) else "CONTINUE"

def step3_advanced_ai_humanizer_detection(metrics):
    high_metrics_ai = (
        metrics['eb'] >= 0.87 and
        metrics['structure_consistency'] >= 92 and
        metrics['vocab_diversity'] >= 0.87
    )
    mathematical_precision = (
        metrics['structure_consistency'] >= 95 or
        metrics['vocab_diversity'] >= 0.92 or
        metrics['eb'] >= 0.92
    )
    moderate_perfection_humanizer = (
        metrics['sentence_variation'] >= 85 and
        metrics['vocabulary_entropy'] >= 85 and
        0.75 <= metrics['eb'] <= 0.85 and
        metrics['structure_consistency'] >= 85 and
        4 <= metrics['pgfi'] <= 8
    )
    if any([high_metrics_ai, mathematical_precision, moderate_perfection_humanizer]):
        return "AI_DETECTED"
    return "CONTINUE"

def step4_final_human_safety_net(metrics):
    final_safety = (
        metrics['pgfi'] <= 15.0 or
        metrics['sentence_variation'] >= 20 or
        metrics['vocabulary_entropy'] >= 30 or
        metrics['structure_consistency'] <= 95 or
        metrics['punctuation_rhythm'] >= 5 or
        metrics['mc'] >= 30 or
        metrics['info_density'] <= 0.50 or
        metrics['eb'] <= 0.85 or
        metrics['vocab_diversity'] <= 0.90
    )
    return "HUMAN_PROTECTED" if final_safety else "AI_DETECTED"

def detect_content_with_imperfection_analysis(metrics):
    """
    Final unified Echo decision logic using full 23 extractor traits +
    6 new stylometric traits (by full name). No gray zone logic.
    """

    # Step 0 – Universal Humanizer Detection (Authentic Imperfection Wall)
    if step0_authentic_imperfection_analysis(metrics) == "HUMANIZER_DETECTED":
        return {
            'result': 'RED',
            'reason': 'Step 0 - Humanizer detected via engineered perfection',
            'step': 0
        }

    # Step 1 – Nuclear AI Detection
    if step1_nuclear_ai_detection(metrics) == "AI_DETECTED":
        return {
            'result': 'RED',
            'reason': 'Step 1 - Nuclear AI patterns detected',
            'step': 1
        }

    # Step 2 – Human Authenticity Verification
    if step2_human_authenticity_verification(metrics) == "HUMAN_PROTECTED":
        return {
            'result': 'GREEN',
            'reason': 'Step 2 - Human authenticity patterns confirmed',
            'step': 2
        }

    # Step 3 – Advanced AI & Humanizer Patterns
    if step3_advanced_ai_humanizer_detection(metrics) == "AI_DETECTED":
        return {
            'result': 'RED',
            'reason': 'Step 3 - Advanced AI or humanizer pattern detected',
            'step': 3
        }

    # Step 4 – Final Human Safety Net
    if step4_final_human_safety_net(metrics) == "HUMAN_PROTECTED":
        return {
            'result': 'GREEN',
            'reason': 'Step 4 - Final safety net validated human traits',
            'step': 4
        }

    # Step 5 – Cluster Magic (Match-based logic for red if failure)
    cluster_match = match_against_authentic_clusters(metrics)
    if cluster_match:
        return {
            'result': 'GREEN',
            'reason': 'Step 5 - Matched human-authored wall cluster',
            'step': 5
        }

    # Final Fallback: If none of the above matched, return RED
    return {
        'result': 'RED',
        'reason': 'No human traits confirmed across steps 0-5',
        'step': -1
    }

# Required Cluster Matching Logic


# Dummy placeholder functions to guide Soumya — will be replaced by live extractors
def extract_6_stylo_traits(text):
    return {
        "Sentence Variation": calculate_sf(text),
        "Punctuation Rhythm": calculate_pf(text),
        "Vocabulary Entropy": calculate_tt(text),
        "Phrase Reuse": calculate_sm(text),
        "Structure Consistency": calculate_mc(text),
        "PGFI-AI Mimicry": calculate_pgfi(text),
    }

# Example
if __name__ == "__main__":
    with open("example_doc.txt", "r") as f:
        document = f.read()
    result, extracted = run_dualwall_echo(document)
    print("Verdict:", result)
    print("Traits:", extracted)