
# run_pipeline.py
# PRUFIA Integration Launcher – Full End-to-End Execution

from app.services.ai_engine.update.main_extractor import run_extractor
from app.services.ai_engine.update.behavioral_engine import run_behavioral_engine
from app.services.ai_engine.update.resistance_engine import run_resistance_engine
from app.services.ai_engine.update.tentacation_logic import tentacation_decision
from app.services.ai_engine.update.cluster_matcher import cluster_matcher
from app.services.ai_engine.update.updated_cluster_matcher import run_all_clusters
from app.services.ai_engine.update.final_score import evaluate_clearance
from app.services.ai_engine.update.evaluate_document_prufia_abbreviated_only import evaluate_document_prufia_expanded_trust

import json

def run_full_pipeline(text):
    # Step 1: Run all extractors
    metrics = {}
    metrics.update(run_extractor(text))
    metrics.update(run_behavioral_engine(text))
    metrics.update(run_resistance_engine(text))

    # Step 2: Tentacation trap logic
    tentacation_result = tentacation_decision(metrics)

    # Step 3: Cluster wall logic
    # cluster_result = run_all_clusters(metrics)
    # Step 4: Final clearance result
    # final_result = evaluate_clearance(cluster_result)

    final_result = evaluate_document_prufia_expanded_trust(metrics)

    return {
        "metrics": metrics,
        "tentacation_result": tentacation_result,
        # "cluster_result": cluster_result,
        "final_result": final_result
    }

if __name__ == "__main__":
    sample_text = """Humans don't just write sentences. They reveal rhythm. They pause, they run on, they repeat.
    Sometimes they contradict themselves. But that's the chaos we trust."""
    cluster_file = "Updated_3_Echo_Cluster_30Layer_Strategy.json"
    result = run_full_pipeline(sample_text, cluster_file)
    print(json.dumps(result, indent=2))
