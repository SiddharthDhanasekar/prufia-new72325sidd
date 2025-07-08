
# final_score.py
# PRUFIA Final Score Logic – Binary MATCH/MISMATCH Output

def evaluate_clearance(cluster_result):
    '''
    Determines final result based on trap/cluster matching:
    - If ANY traps or clusters are hit, return MISMATCH
    - If NONE are hit, return MATCH
    '''
    match_count = 0
    
    # Iterate through each dictionary in the list
    for result in cluster_result:
        # Check if the outcome is 'match'
        if result.get('outcome') == 'match':
            # Increment the counter
            match_count += 1
            

    if match_count > 0:
        return "match"
    else:
        return "mismatch"
