def evaluate_clearance(cluster_result):
    # Sort clusters by trap priority — traps must be named clearly
    trap_keywords = ["trap", "block", "firewall"]
    trap_mismatches = [r for r in cluster_result if r['outcome'].lower() == 'mismatch' and any(k in r['rule'].lower() for k in trap_keywords)]

    if trap_mismatches:
        return {
            "status": "MISMATCH",
            "reason": f"Blocked by trap: {trap_mismatches[0]['rule']}"
        }

    # Check if any matching cluster passed (soft identity confirmation)
    has_match = any(r['outcome'].lower() == 'match' or r['outcome'].lower() == 'pass' for r in cluster_result)
    if has_match:
        return {
            "status": "MATCH",
            "reason": "At least one cluster passed"
        }

    # Default: nothing matched, no trap hit — deny access
    return {
        "status": "MISMATCH",
        "reason": "No matching cluster"
    }



