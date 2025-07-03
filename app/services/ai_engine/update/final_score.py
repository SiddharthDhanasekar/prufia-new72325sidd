
# final_score.py
# PRUFIA Final Score Logic – Binary MATCH/MISMATCH Output

def evaluate_clearance(tentacation_result, cluster_result):
    '''
    Determines final result based on trap/cluster matching:
    - If ANY traps or clusters are hit, return MISMATCH
    - If NONE are hit, return MATCH
    '''
    trap_hits = tentacation_result.get('trap_count', 0)
    matched_clusters = len(cluster_result)

    if trap_hits > 0 or matched_clusters > 0:
        return {
            "status": "MISMATCH",
            "reason": f"{trap_hits} trap(s), {matched_clusters} cluster(s) matched"
        }
    else:
        return {
            "status": "MATCH",
            "reason": "No traps or clusters matched"
        }

if __name__ == "__main__":
    tentacation_result = {"trap_count": 1}
    cluster_result = {"match_count": 0}
    print(evaluate_clearance(tentacation_result, cluster_result))
