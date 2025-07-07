
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def text_to_vectors(self, sentences):
        # Converts list of sentences to tf-idf vectors
        try:
            tfidf = self.vectorizer.fit_transform(sentences)
            return tfidf.toarray()
        except ValueError:
            return [np.zeros(1) for _ in sentences]

    def calculate_complexity(self, sentence):
        # Approximate complexity using avg word length + punctuation density
        words = sentence.split()
        if not words:
            return 0.0
        avg_word_len = sum(len(word) for word in words) / len(words)
        punct_count = sum(sentence.count(p) for p in [',', ';', ':'])
        return avg_word_len + (punct_count / max(1, len(sentence)))
