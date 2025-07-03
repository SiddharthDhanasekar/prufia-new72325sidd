from difflib import SequenceMatcher
from collections import Counter, defaultdict
import math
import spacy
import string
import nltk
import re
from nltk.util import ngrams
from textstat import textstat
from nltk.tokenize import sent_tokenize, word_tokenize
from functools import lru_cache
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import textstat
from typing import Dict, Any
import os
from docx import Document


nltk.download('punkt')
nltk.download('punkt_tab')

@lru_cache(maxsize=2)
def load_spacy_model(model_name):
    """Load spaCy model with caching to avoid reloading"""
    return spacy.load(model_name)

class TextAnalyzer:
    def __init__(self):
        # Initialize models (will load on first use due to caching)
        self.nlp_sm = None  # Small model
        self.nlp_lg = None  # Large model
    
    def get_model(self, model_type='sm'):
        """Get the appropriate model instance"""
        if model_type == 'sm':
            if self.nlp_sm is None:
                self.nlp_sm = load_spacy_model('en_core_web_sm')
            return self.nlp_sm
        elif model_type == 'lg':
            if self.nlp_lg is None:
                self.nlp_lg = load_spacy_model('en_core_web_lg')
            return self.nlp_lg
        raise ValueError("Invalid model type. Use 'sm' or 'lg'")

# Create a global analyzer instance
analyzer = TextAnalyzer()

# • Sentence_Length_Variation (SF):         0.25
# • Punctuation_Rhythm (PF):                0.10
# • Passive_Voice (EB):                     0.10
# • Phrase_Reuse (SM):                      0.15
# • PGFI AI Mimicry Score (TT):             0.15
# • Opening_Closing Structure (MC):         0.05

def calculate_prufia_final_score(input_data):
    """
    Requires 7 signal inputs: sf, pf, eb, sm, tt, mc, pgfi
    Returns final score (0–100) and a match status.
    """
    weights = {
        'sf': 0.02,
        'pf': 0.01,
        'eb': 0.01,
        'sm': 0.41,
        'tt': 0.10,
        'mc': 0.05,
        'pgfi': 0.40
    }

    final_score = (
        input_data['sf'] * weights['sf'] +
        input_data['pf'] * weights['pf'] +
        input_data['eb'] * weights['eb'] +
        input_data['sm'] * weights['sm'] +
        input_data['tt'] * weights['tt'] +
        input_data['mc'] * weights['mc'] +
        input_data['pgfi'] * weights['pgfi']
    )

    final_score = max(0, min(final_score, 100))

    # Developer Note:
    # This match logic is currently based on weighted score from 7 traits (SF, PF, EB, SM, TT, MC, PGFI).
    # Once Echo is activated, this logic will be replaced or extended with:
    #     echo_result = check_vector_similarity_to_human_clusters(input_data)
    #     if echo_result == "Match":
    #         status = "Match (Green)"
    #     else:
    #         status = "Mismatch (Red)"
    # For now, scoring threshold is used: score ≥ 75 = Green, otherwise Red.

    if final_score >= 75:
        status = "Match (Green)"
    else:
        status = "Mismatch (Red)"

    return round(final_score, 2), status

    



def calculate_phrase_reuse_score(test_text, wall_text):
    def tokenize(text):
        return set(word.lower() for word in text.split() if word.isalnum())
    test_tokens = tokenize(test_text)
    tokens = tokenize(wall_text)
    if not test_tokens or not tokens:
        return 0.0
    overlap = test_tokens.intersection(tokens)
    reuse_ratio = len(overlap) / len(test_tokens)
    return round(reuse_ratio * 100, 2)

def load_walls(wall_dir="./walls/"):
    walls = {}
    for author_dir in os.listdir(wall_dir):
        path = os.path.join(wall_dir, author_dir)
        if os.path.isdir(path):
            texts = []
            for file in os.listdir(path):
                if file.endswith(".txt"):
                    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if len(content.split()) >= 30:
                            texts.append(content)
                elif file.endswith(".docx"):
                    try:
                        doc = Document(os.path.join(path, file))
                        content = "\n".join([para.text for para in doc.paragraphs]).strip()
                        if len(content.split()) >= 30:  # Avoid blank or useless
                            texts.append(content)
                    except Exception as e:
                        print(f"Skipping invalid file: {file} | Error: {e}")
            if texts:
                walls[author_dir] = " ".join(texts)
    return walls

def word_entropy(text):
    words = text.split()
    freq = Counter(words)
    total = sum(freq.values())
    return -sum((count/total) * math.log2(count/total) for count in freq.values())

def calculate_kt_entropy(text: str) -> float:
    """
        Calculates vocabulary entropy using Shannon entropy (KT score).
        Normalized to a 0–100 scale.
    """
    cleaned_text = ''.join(char.lower() for char in text if char.isalnum() or char.isspace())
    words = cleaned_text.split()
    if not words:
        return 0.0
    word_counts = Counter(words)
    total_words = len(words)
    entropy = -sum((count / total_words) * math.log2(count / total_words)
                   for count in word_counts.values())

    normalized_entropy = min(entropy * 20, 100)

    return round(normalized_entropy, 2)


# def calculate_ratio_vs_reference( ratio, reference_ratio):
#     try:
#         if reference_ratio == 0:
#             return "N/A (reference ratio is zero)"
#         if not (isinstance(ratio, (int, float)) and isinstance(reference_ratio, (int, float))):
#             return "N/A (invalid input)"
#         return f"{ratio/reference_ratio:.1%}"
#     except (TypeError, ValueError):
#         return "N/A (calculation error)"

# def punctuation_counts(text):
#     return {p: text.count(p) for p in string.punctuation if text.count(p) > 0}


# Output: ['in conclusion', 'this means that', 'therefore']
def safe_divide(numerator, denominator, default="N/A"):
    """Safe division with zero denominator handling"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ValueError):
        return default


def semantic_flow(text):
    nlp = analyzer.get_model('lg')
    doc = nlp(text)
    sentences = [sent for sent in doc.sents]
    paragraphs = text.split('\n\n') if '\n\n' in text else [text]
    
    analysis = {
        'cohesion': {'score': 0, 'transitions': defaultdict(int)},
        'referential_clarity': {'score': 0, 'references': []},
        'topic_drift': {'warnings': [], 'avg_similarity': 0},
        'transition_smoothness': {'scores': [], 'avg_score': 0}
    }
    
    # 1. Cohesion Scoring
    cohesive_words = ['however', 'therefore', 'thus', 'meanwhile']
    transition_count = 0
    
    for sent in sentences:
        for token in sent:
            if token.text.lower() in cohesive_words:
                transition_count += 1
                analysis['cohesion']['transitions'][token.text.lower()] += 1
    
    analysis['cohesion']['score'] = float(transition_count / len(sentences)) if sentences else 0.0
    
    # 2. Referential Clarity
    pronouns = ['this', 'that', 'these', 'those', 'it', 'they']
    reference_phrases = ['this', 'that', 'these', 'those']
    link_count = 0
    unclear_references = []
    
    for i, sent in enumerate(sentences):
        for token in sent:
            if token.text.lower() in pronouns:
                link_count += 1
                # Check if reference is clear
                if not any(np.dot(token.vector, prev_token.vector) > 0.6 
                          for prev_sent in sentences[:i] 
                          for prev_token in prev_sent):
                    unclear_references.append((i, token.text))
            
            # Check for reference phrases ("this idea")
            if token.text.lower() in reference_phrases and i > 0:
                head_noun = next((child for child in token.children 
                                if child.dep_ in ('attr', 'dobj')), None)
                if head_noun:
                    analysis['referential_clarity']['references'].append(
                        f"{token.text} {head_noun.text}"
                    )
    
    analysis['referential_clarity']['score'] = float((link_count - len(unclear_references)) / len(sentences) if sentences else 0.0)
    
    # 3. Topic Drift
    if len(paragraphs) > 1:
        similarities = []
        for i in range(len(paragraphs)-1):
            doc1 = nlp(paragraphs[i])
            doc2 = nlp(paragraphs[i+1])
            sim = doc1.similarity(doc2)
            similarities.append(float(sim))  # Convert to Python float
            if sim < 0.6:
                analysis['topic_drift']['warnings'].append(
                    f"Low similarity ({float(sim):.2f}) between paragraphs {i+1}-{i+2}"
                )
        analysis['topic_drift']['avg_similarity'] = float(sum(similarities)/len(similarities)) if similarities else 1.0
    
    # 4. Transition Smoothness
    if len(sentences) > 1:
        smoothness_scores = []
        for i in range(len(sentences)-1):
            # Get last word of current sentence and first word of next
            last_word = sentences[i][-1]
            first_word = sentences[i+1][0]
            
            # Calculate cosine similarity between embeddings
            if last_word.has_vector and first_word.has_vector:
                sim = cosine_similarity(
                    last_word.vector.reshape(1, -1), 
                    first_word.vector.reshape(1, -1)
                )[0][0]
                smoothness_scores.append(float(sim))  # Convert to Python float
        
        analysis['transition_smoothness']['scores'] = smoothness_scores
        analysis['transition_smoothness']['avg_score'] = float(sum(smoothness_scores)/len(smoothness_scores)) if smoothness_scores else 1.0
    
    return analysis
def calculate_sf(text):
    sentences = re.split(r'[.!?]', text)
    lengths = [len(s.strip().split()) for s in sentences if len(s.strip().split()) > 2]
    if len(lengths) < 3:
        return 0.0
    from statistics import stdev
    try:
        std = stdev(lengths)
    except:
        return 0.0
    # Normalize to 0–100 range
    return round(min(100, std * 10), 2)

def calculate_eb(text):
    # Normalize and split sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if len(s.strip().split()) > 0]

    passive_count = 0
    for sentence in sentences:
        # Broad passive voice detection patterns
        if re.search(r'\b(?:was|were|is being|are being|had been|has been|have been|being|be)\b\s+(\w+ed|\w+en)\b', sentence, re.IGNORECASE):
            passive_count += 1
        elif re.search(r'\b(get|got|gets|getting)\b\s+(\w+ed|\w+en)\b', sentence, re.IGNORECASE):
            passive_count += 1
        elif re.search(r'\b(by the|by a|by an)\b', sentence, re.IGNORECASE) and re.search(r'\w+ed\b', sentence):
            passive_count += 1

    total = len(sentences)
    ratio = passive_count / total if total > 0 else 0

    # Score: 0 = fully passive, 100 = fully active
    score = (1 - ratio) * 100
    return round(max(0, min(score, 100)), 2)

def calculate_pf(text):
    punctuations = [char for char in text if char in string.punctuation]
    if not punctuations:
        return 0.0

    counts = Counter(punctuations)
    unique_count = len(counts)
    total = sum(counts.values())

    diversity_ratio = unique_count / total if total > 0 else 0
    score = diversity_ratio * 100

    return round(min(100, score * 1.5), 2)


def calculate_sm(text):
    words = re.findall(r'\b\w+\b', text.lower())
    total = len(words)
    if total == 0:
        return 0.0

    counts = Counter(words)
    repeated = sum([count for word, count in counts.items() if count > 1])
    repetition_ratio = repeated / total

    return round(min(100, repetition_ratio * 100), 2)



def calculate_mc(text):
    """
    Calculates Meaning Curve (MC) score as a float (0–100 scale).
    Approximates semantic shift by measuring sentence uniqueness and content pacing.
    """

    def get_sentences(text):
        return re.split(r'[.!?]', text.strip())

    sentences = get_sentences(text)
    sentences = [s.strip() for s in sentences if len(s.strip().split()) > 3]

    if len(sentences) < 3:
        return 0.0  # Not enough content to compute curve

    # Measure word uniqueness across sentences
    sentence_tokens = [set(s.lower().split()) for s in sentences]
    shifts = []

    for i in range(1, len(sentence_tokens)):
        overlap = sentence_tokens[i].intersection(sentence_tokens[i - 1])
        shift_score = 1 - (len(overlap) / max(1, len(sentence_tokens[i])))
        shifts.append(shift_score)

    avg_shift = sum(shifts) / len(shifts)

    # Normalize to 0–100 (higher = more semantic shift = more human)
    mc_score = round(min(100, max(0, avg_shift * 100)), 2)

    return mc_score

def calculate_tt(text):
    """
    Calculates Temporal Transition score as a float (0–100 scale).
    Measures how sentence structure and thematic transitions behave over time.
    """

    def get_sentences(text):
        return re.split(r'[.!?]', text.strip())

    sentences = get_sentences(text)
    sentences = [s.strip() for s in sentences if len(s.strip().split()) > 2]

    if len(sentences) < 3:
        return 0.0  # Not enough sentence data

    # Measure change in sentence lengths between transitions
    transitions = []
    for i in range(1, len(sentences)):
        len_diff = abs(len(sentences[i].split()) - len(sentences[i - 1].split()))
        transitions.append(len_diff)

    avg_diff = sum(transitions) / len(transitions)

    # Normalize to 0–100 scale (higher = more variation = more human)
    tt_score = min(100, max(0, avg_diff * 10))  # Stretch difference into scale

    return round(tt_score, 2)

def calculate_pgfi(text):

    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    repeated = total_words - len(set(words))
    repetition_ratio = repeated / total_words if total_words else 0

    passive_matches = re.findall(r'\b(was|were|is being|are being|been)\b\s+\w+ed\b', text.lower())
    passive_ratio = len(passive_matches) / total_words if total_words else 0

    gpt_flags = 0
    if len(set(words)) < total_words * 0.4:
        gpt_flags += 1
    if any(p in text.lower() for p in ["in conclusion", "this essay", "it is important to note"]):
        gpt_flags += 1

    # Weighted sum to simulate internal suppression scoring
    score = (
        (repetition_ratio * 100 * 0.4) +
        (passive_ratio * 100 * 0.4) +
        (gpt_flags * 10)
    )

    return round(min(score, 100), 2)

# def calculate_passive_voice(text):
    """
    PRUFIA Passive Voice Master Patch
    Built to detect deep and deceptive passive constructs in AI and mimic documents.
    - Captures agentless passive forms
    - Detects 'by'-phrases, get-passives, indirect passives
    - Prioritizes broad linguistic coverage without hallucination
    """

    # Preprocess and break into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    passive_count = 0
    flagged_sentences = []

    for sentence in sentences:
        is_passive = False

        # Pattern 1: be-verb + past participle
        if re.search(r'\b(?:is|are|was|were|be|been|being|has been|have been|had been)\b\s+\w+(ed|en)\b', sentence, re.IGNORECASE):
            is_passive = True

        # Pattern 2: get/got + past participle
        elif re.search(r'\b(?:get|got|gets|getting)\b\s+\w+(ed|en)\b', sentence, re.IGNORECASE):
            is_passive = True

        # Pattern 3: 'by' phrase with past participle verb before or after
        elif re.search(r'\bby\b\s+(the|a|an)?\s*\w+', sentence, re.IGNORECASE) and re.search(r'\w+(ed|en)\b', sentence):
            is_passive = True

        # Pattern 4: noun + 'was' or 'were' used with likely irregular participles (e.g., thrown, written, built)
        elif re.search(r'\b(?:was|were)\b\s+(thrown|written|built|driven|caught|left|sent|held|known|won|taken|seen|taught)\b', sentence, re.IGNORECASE):
            is_passive = True

        if is_passive:
            passive_count += 1
            flagged_sentences.append(sentence)

    total_sentences = len(sentences)
    if total_sentences == 0:
        return 0.0

    passive_ratio = passive_count / total_sentences
    return round(passive_ratio * 100, 2)