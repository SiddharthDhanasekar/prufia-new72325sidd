
# PRUFIA Layer 23: Conceptual Network Authenticity (Fixed Version)
# Plug-and-Play Module

def evaluate_conceptual_network(words):
    if len(words) < 100:
        return 0.0

    sophisticated_words = [w for w in words if len(w) >= 6]
    unique_sophisticated = set(sophisticated_words)

    linkage_bonus = 0.0
    abstract_terms = ["ontology", "epistemology", "heuristic", "paradigm", "inference", "dichotomy"]
    match_abstract = sum(1 for w in words if w.lower() in abstract_terms)
    if match_abstract > 3:
        linkage_bonus = 10.0

    sophistication_ratio = len(unique_sophisticated) / len(words)
    density_score = min(100, (sophistication_ratio * 100) + linkage_bonus)

    return round(density_score, 2)

# Example usage
if __name__ == "__main__":
    test_text = "This framework operates within a paradigm of layered inference and conceptual grounding..."
    words = test_text.split()
    score = evaluate_conceptual_network(words)
    print("Conceptual Network Score:", score)
