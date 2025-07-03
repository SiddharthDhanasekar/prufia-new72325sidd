
# main_extractor.py
# PRUFIA Extractor – Core Stylometric Signal Collector (No Placeholders)

import re
from difflib import SequenceMatcher
import statistics
from collections import Counter

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

def extract_structure_fingerprint(text):
     # Split into sentences
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    sentence_lengths = [len(s.split()) for s in sentences if len(s.split()) > 0]

    if len(sentence_lengths) < 2:
        return 0.0  # not enough data to calculate variation

    try:
        std_dev = statistics.stdev(sentence_lengths)
        mean_len = statistics.mean(sentence_lengths)
        variation_ratio = std_dev / mean_len
        score = min(variation_ratio * 100, 100)  # scale and cap at 100
        return round(score, 2)
    except:
        return 0.0

def extract_punctuation_frequency(text):
    punctuation = re.findall(r'[.,!?;:]', text)
    sentence_count = max(1, len(re.split(r'[.!?]', text)))
    return round(len(punctuation) / sentence_count, 2)

def extract_entropy_balance(text):
    passive_phrases = re.findall(r'\b(is|was|were|are|been|being|be)\s+\w+ed\b', text.lower())
    total_clauses = max(1, len(re.findall(r'[.!?]', text)))
    passive_ratio = len(passive_phrases) / total_clauses
    active_ratio = 1 - passive_ratio
    return round(active_ratio * 100, 2)

def extract_sentence_mapping(text):
    '''
    Sentence Mapping (SM) – Normalized pattern-based reuse detection.
    Measures how often similar sentence starts appear across the document.

    Returns:
        float: Reuse percentage score (0–100)
    '''
    # Normalize text into sentence starts
    sentences = [s.strip().lower() for s in re.split(r'[.!?]', text) if s.strip()]
    sentence_starts = []

    for s in sentences:
        words = re.findall(r'\b\w+\b', s)
        start = ' '.join(words[:6])  # Only first 6 words of sentence
        if start:
            sentence_starts.append(start)

    seen = set()
    reused = 0
    for start in sentence_starts:
        if start in seen:
            reused += 1
        seen.add(start)

    reuse_ratio = reused / max(1, len(sentence_starts))
    return round(reuse_ratio * 100, 2)

def extract_typing_tempo(text):
    words = text.split()
    avg_length = sum(len(w) for w in words) / max(1, len(words))
    return round(avg_length * 10, 2)

def extract_memory_consistency(text):
    words = text.lower().split()
    unique_words = set(words)
    ratio = len(unique_words) / max(1, len(words))
    return round(ratio * 100, 2)

def extract_pgfi_display(text):
    """
    Original PGFI Scoring Logic – Prompt Generalization Forgiveness Index
    Measures generalized prompt reuse or templated formalism.

    Returns:
        float: PGFI score (0–100), where lower = more forgiving/general
    """
    # Generalized academic prompt phrases (low-variance writing indicators)
    pgfi_phrases = [
        'in this essay', 'this paper will', 'the purpose of this paper',
        'as mentioned above', 'we will explore', 'this document discusses',
        'an important topic', 'it is widely known', 'in conclusion',
        'throughout history', 'in today’s society', 'from the beginning of time',
        'the author believes', 'this clearly shows', 'as stated previously'
    ]

    # Normalize text
    lowered = text.lower()

    # Count phrase hits
    hits = sum(1 for phrase in pgfi_phrases if phrase in lowered)

    # Scale by document size
    total_words = len(re.findall(r'\b\w+\b', lowered))
    phrase_density = hits / max(1, total_words / 100)  # hits per 100 words

    # Map density to PGFI score (capped)
    score = min(phrase_density * 100, 100)

    return round(score, 2)

def extract_shell_reuse_score(text):
    """
    PRUFIA Shell Reuse Trap Extractor (4-gram fingerprint based)
    ------------------------------------------------------------
    This is NOT a scoring layer.
    It detects repeated 4-word phrases (n-grams) across the document
    to expose humanizer-style pattern loops and hidden mimicry.

    Usage:
    - Not part of trust score
    - Used in cluster traps or tentacation triggers

    Returns:
        float: Reuse score (0 to 100)
    """
    text = re.sub(r'[^\w\s]', '', text.lower())  # Normalize text
    tokens = text.split()

    phrase_counts = Counter()
    for i in range(len(tokens) - 3):
        phrase = ' '.join(tokens[i:i+4])  # 4-gram sliding window
        phrase_counts[phrase] += 1

    reused_count = sum(1 for _, count in phrase_counts.items() if count > 1)
    total_phrases = len(phrase_counts)

    if total_phrases == 0:
        return 0.0

    reuse_ratio = reused_count / total_phrases
    return round(reuse_ratio * 100, 2)

def run_extractor(text):
    return {
        'SF': extract_structure_fingerprint(text),
        'PF': extract_punctuation_frequency(text),
        'EB': extract_entropy_balance(text),
        'SM': calculate_sm(text),
        'TT': extract_typing_tempo(text),
        'MC': extract_memory_consistency(text),
        'PGFI': calculate_pgfi(text),
        'ShellReuse': extract_shell_reuse_score(text)
    }

if __name__ == "__main__":
    sample = "The process was completed. He was instructed to leave. The report was written by a student."
    output = run_extractor(sample)
    for k, v in output.items():
        print(f"{k}: {v}")
