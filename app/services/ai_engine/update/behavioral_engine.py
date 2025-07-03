
# behavioral_engine.py
# PRUFIA Behavioral Stylometry Engine (No Placeholders)

import math
import re
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
def extract_sentence_variation(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    lengths = [len(s.split()) for s in sentences]
    return round((max(lengths) - min(lengths)) * 5, 2) if lengths else 0

def extract_vocabulary_entropy(text):
    words = text.lower().split()
    freq = Counter(words)
    total = len(words)
    entropy = -sum((count/total) * math.log2(count/total) for count in freq.values() if count > 0)
    return round(entropy * 10, 2)

def extract_punctuation_rhythm(text):
    sentences = re.split(r'[.!?]', text)
    counts = [len(re.findall(r'[.,;:!?]', s)) for s in sentences if s.strip()]
    if len(counts) <= 1:
        return 0
    avg = sum(counts) / len(counts)
    return round(avg * 10, 2)

def extract_behavioral_phrase_reuse(text):
    '''
    Phrase Reuse – Behavioral Layer
    Detects repeated 5-10 word phrases across the document.
    Returns:
        float: Reuse percentage (0–100)
    '''
    tokens = re.findall(r'\b\w+\b', text.lower())
    phrases = [' '.join(tokens[i:i+n]) for n in range(5, 11) for i in range(len(tokens) - n + 1)]
    phrase_counts = Counter(phrases)
    reused_count = sum(1 for phrase, count in phrase_counts.items() if count > 1)
    reuse_ratio = reused_count / max(1, len(phrases))
    return round(reuse_ratio * 100, 2)

def extract_structure_consistency(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    lengths = [len(s.split()) for s in sentences]
    if len(lengths) < 2:
        return 100
    variance = sum(abs(lengths[i] - lengths[i-1]) for i in range(1, len(lengths)))
    return round(100 - min(variance, 100), 2)

def extract_pgfi_display(text):
    """
    PRUFIA PGFI Display – Dynamic Variance Detector (100-point scale)

    Calculates how much "padding" or generic phrasing is used to inflate content,
    typically observed in AI or humanizer documents trying to appear thoughtful.

    The score is dynamic based on:
    - Passive constructions
    - Vague terms
    - Filler intros/outros
    - Phrase structure uniformity

    Returns:
        float: Score between 0 (highly generic) and 100 (clear and authentic)
    """
    text = text.lower()

    vague_terms = ['something', 'anything', 'things', 'stuff', 'important']
    vague_hits = sum(text.count(term) for term in vague_terms)

    padding_phrases = [
        'in conclusion', 'this essay', 'the purpose of this paper',
        'it is important to note', 'we will explore', 'this document discusses',
        'as mentioned above', 'in summary'
    ]
    padding_hits = sum(text.count(phrase) for phrase in padding_phrases)

    passive_matches = re.findall(r'\b(was|were|is being|are being|been)\b\s+\w+ed\b', text)
    passive_hits = len(passive_matches)

    total_hits = vague_hits + padding_hits + passive_hits
    penalty = min(total_hits * 5, 100)

    return round(100 - penalty, 2)

def extract_temporal_tempo(text):
    sentences = [len(s.strip().split()) for s in re.split(r'[.!?]', text) if s.strip()]
    tempo_shifts = [abs(sentences[i] - sentences[i-1]) for i in range(1, len(sentences))]
    return round(sum(tempo_shifts) / max(1, len(tempo_shifts)) * 10, 2)

def run_behavioral_engine(text):
    return {
        'SentenceVariation': extract_sentence_variation(text),
        'VocabularyEntropy': extract_vocabulary_entropy(text),
        'PunctuationRhythm': extract_punctuation_rhythm(text),
        'PhraseReuse': extract_behavioral_phrase_reuse(text),
        'StructureConsistency': extract_structure_consistency(text),
        'PGFIDisplay': extract_pgfi_display(text),
        'TemporalTempo': extract_temporal_tempo(text)
    }

if __name__ == "__main__":
    sample = "Some things are very important. Something should be done. Things like these are common."
    output = run_behavioral_engine(sample)
    for k, v in output.items():
        print(f"{k}: {v}")
