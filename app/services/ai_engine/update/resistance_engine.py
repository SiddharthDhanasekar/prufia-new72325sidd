
# resistance_engine.py
# PRUFIA AI Resistance Engine – No Placeholders

import math
import re
from collections import Counter

def extract_char_transition_entropy(text):
    chars = list(text.replace(" ", ""))
    transitions = [(chars[i], chars[i+1]) for i in range(len(chars)-1)]
    freq = Counter(transitions)
    total = len(transitions)
    entropy = -sum((count/total) * math.log2(count/total) for count in freq.values() if count > 0)
    return round(entropy * 10, 2)

def extract_micro_rhythm_variance(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    syllable_counts = [len(re.findall(r'[aeiouy]+', s.lower())) for s in sentences]
    if len(syllable_counts) <= 1:
        return 0
    diffs = [abs(syllable_counts[i] - syllable_counts[i-1]) for i in range(1, len(syllable_counts))]
    return round(sum(diffs) / len(diffs), 2)

def extract_frequency_distribution_deviation(text):
    words = text.lower().split()
    freq = Counter(words)
    sorted_freqs = sorted(freq.values(), reverse=True)
    zipf_ideal = [sorted_freqs[0] / (i+1) for i in range(len(sorted_freqs))]
    deviation = sum(abs(a - b) for a, b in zip(sorted_freqs, zipf_ideal)) / max(1, len(sorted_freqs))
    return round(deviation, 2)

def extract_syntactic_chaos(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    structures = [len(s.split()) for s in sentences]
    chaos = sum(abs(structures[i] - structures[i-1]) for i in range(1, len(structures)))
    return round(min(chaos, 100), 2)

def extract_compression_resistance(text):
    raw_length = len(text.encode("utf-8"))
    import zlib
    compressed = len(zlib.compress(text.encode("utf-8")))
    ratio = compressed / raw_length if raw_length else 1
    resistance = 1 - ratio
    return round(resistance * 100, 2)

def run_resistance_engine(text):
    return {
        'CharTransitionEntropy': extract_char_transition_entropy(text),
        'MicroRhythmVariance': extract_micro_rhythm_variance(text),
        'FrequencyDeviation': extract_frequency_distribution_deviation(text),
        'SyntacticChaos': extract_syntactic_chaos(text),
        'CompressionResistance': extract_compression_resistance(text)
    }

if __name__ == "__main__":
    sample = "Synthetic language outputs often compress well. They follow patterns and repeat forms."
    output = run_resistance_engine(sample)
    for k, v in output.items():
        print(f"{k}: {v}")
