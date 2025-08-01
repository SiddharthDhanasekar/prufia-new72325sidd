
# PRUFIA Safe Logic – Developer Version (Abbreviated Signal Names Only)

def matches_hard_traps(doc):
    """Hard Trap Detection – Includes individual and advanced combo conditions."""
    return (
        doc.get("PGFI", 0) > 55 or
        doc.get("PGFI", 100) < 5.5 or
        doc.get("SyntacticChaos", 100) < 13 or
        doc.get("TT", 0) > 59 or
        doc.get("TT", 100) < 31 or
        doc.get("MicroRhythmVariance", 0) > 100 or
        doc.get("PF", 0) > 5.5 or
        doc.get("PunctuationRhythm", 0) > 60 or
        doc.get("SentenceVariation", 0) > 850 or
        (
            # Combo Hard Trap: MRV + TT + PGFI + SF/SM
            doc.get("MicroRhythmVariance", 0) > 17 and
            doc.get("TT", 0) > 49.99 and
            doc.get("PGFI", 0) > 8 and
            (doc.get("SF", 100) < 45 or doc.get("SM", 100) < 52)
        ) or
        (
            11 <= doc.get("PGFI", 0) <= 17 and
            doc.get("PF", 0) >= 2.0 and
            doc.get("SyntacticChaos", 100) <= 75 and
            doc.get("SM", 0) <= 54 and
            doc.get("TT", 0) >= 45
        ) or
        (
            doc.get("PF", 0) >= 2.25 and
            doc.get("SM", 0) < 58 and
            doc.get("SF", 0) < 43 and
            doc.get("SyntacticChaos", 100) < 80 and
            doc.get("PGFI", 0) < 17
        ) or
        (
            doc.get("PF", 0) > 1.85 and
            doc.get("SM", 0) < 58 and
            doc.get("SF", 0) < 48 and
            doc.get("SyntacticChaos", 100) < 80 and
            doc.get("PGFI", 0) < 17.5 and
            doc.get("TT", 0) > 45
        ) or
        (
            doc.get("MC", 0) >= 63 and
            doc.get("SM", 0) <= 56 and
            doc.get("SyntacticChaos", 100) <= 75 and
            doc.get("PF", 0) >= 2.1
        ) or
        (
            doc.get("PGFI", 0) < 17.5 and
            doc.get("PF", 0) > 2.1 and
            doc.get("TT", 0) > 46.5 and
            doc.get("SM", 0) < 52 and
            doc.get("SyntacticChaos", 100) < 78
        ) or
        (
            doc.get("PF", 0) > 2.2 and
            doc.get("StructureConsistency", 0) > 25 and
            doc.get("SyntacticChaos", 100) < 75 and
            10 <= doc.get("PGFI", 0) <= 18 and
            doc.get("SM", 0) < 53
        ) or
        (
            doc.get("PF", 0) > 2.15 and
            doc.get("SyntacticChaos", 100) < 60 and
            doc.get("SF", 0) < 42 and
            doc.get("SM", 0) < 55
        ) or
        (
            doc.get("SyntacticChaos", 100) >= 80 and
            doc.get("StructureConsistency", 0) < 25 and
            doc.get("PGFI", 0) < 19 and
            doc.get("PF", 0) > 2
        )
    )

    
def count_violation_points(doc):
    """Soft Trap: 5-point violation system"""
    points = 0
    if doc.get("SF", 100) < 60:
        points += 1
    if doc.get("PGFI", 100) < 15:
        points += 1
    if doc.get("PF", 0) > 2.10:
        points += 1
    if doc.get("SM", 100) < 50:
        points += 1
    if doc.get("TT", 0) > 50:
        points += 1
    return points

def matches_safe_human_rescue(doc):
    """Human Trust Layer Rescue (if 3+ point violations)"""
    return (
        doc.get("TT", 100) < 50 and
        doc.get("PF", 100) < 2.5 and
        doc.get("SentenceVariation", 0) > 49.99
    )


def evaluate_document_prufia_expanded_trust(doc):
    """
    PRUFIA Developer Logic (Abbreviated Traits):
    1. Hard Trap → Mismatch
    2. If passed, count violations:
        - If 2 or fewer violations → Match
        - If 3 or more → Run rescue check:
            - If passed → Match
            - Else → Mismatch
    """
    if matches_hard_traps(doc):
        return "Mismatch"

    violations = count_violation_points(doc)

    if violations <= 2:
        return "Match"

    if matches_safe_human_rescue(doc):
        return "Match"
    else:
        return "Mismatch"
