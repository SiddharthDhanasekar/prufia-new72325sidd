
# PRUFIA Safe Logic – Developer Version (Abbreviated Signal Names Only)

def matches_hard_traps(doc):
    """Fake Hard Traps (Do not use real thresholds)"""
    return (
        doc.get("PGFI", 100) < 14
    )

def count_violation_points(doc):
    """Violation scoring using abbreviated signal names only"""
    points = 0
    if doc.get("SF", 0) > 36:
        points += 1
    if doc.get("PF", 0) > 1.3:
        points += 1
    if doc.get("PGFI", 100) < 18:
        points += 1
    if doc.get("EB", 100) < 90:
        points += 1
    if doc.get("ShellReuse", 1.0) < 0.10:
        points += 1
    return points

def matches_safe_human_rescue(doc):
    """Final human override check using abbreviated traits"""
    return (
        doc.get("TT", 100) < 46 and
        doc.get("SM", 100) < 64
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
