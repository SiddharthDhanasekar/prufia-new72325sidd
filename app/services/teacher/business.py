import re
import numpy as np

import base64
import time
from datetime import datetime
from app.services.admin.common import getTime
import json
from app.services.db.mysql import db_connection
from app.services.ai_engine.score import (
    calculate_sf,
    calculate_sm,
    calculate_pf,
    calculate_eb,
    calculate_tt,
    calculate_mc,
    calculate_pgfi,
    calculate_phrase_reuse_score,
    calculate_prufia_final_score,
    load_walls
)
from app.services.ai_engine.echo_scoring_clean import echo_decision, final_prufia_decision, check_htl, check_mdt, check_drift, check_fusion
from app.services.ai_engine.prufia_raw_human_extractor import extract_raw_metrics
from app.services.ai_engine.prufia_23layer_extractor.echo_match_23layer_threshold2 import run_echo_decision_logic
from app.services.ai_engine.update.run_pipeline import run_full_pipeline
from app.services.ai_engine.conciousness.prufia_consciousness_observer_23_24_30 import ConsciousnessObserver
from app.services.ai_engine.conciousness.simple_analyzer import SimpleAnalyzer

from flask import (
     current_app
)
from docx import Document

import json



def saveLog(teacher, action):
    
    conn = None
    try:
        conn = db_connection()
        
        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO logs (teacher, action)
                VALUES (%s, %s)""",
                (teacher, action))
            
            conn.commit()
            
            return 200, None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None, f"Unexpected error: {str(e)}"
    finally:
        if conn:
            conn.close()

# Global cache for walline loading
# walline_cache = {
#     'last_loaded': 0,
#     'timeout': 300,  # seconds (5 minutes)
#     'documents': []
# }


# For testing without wallines
# def select_best_wall(test_text, wall_dict):
#     """
#     wall_dict = {
#         'prince': 'text...',
#         'sinaii': 'text...',
#         ...
#     }
#     """
#     kt_score = calculate_kt_entropy(test_text)
#     best_wall = None
#     highest_sm = 0.0
#     for wall_name, wall_text in wall_dict.items():
#         sm = calculate_phrase_reuse_score(test_text, wall_text)
#         print("wall:", wall_name, "kt:", kt_score, "sm:", sm)
#         if kt_score >= 50 and sm >= 35:
#             if sm > highest_sm:
#                 best_wall = {
#                     'wall': wall_name,
#                     'kt': kt_score,
#                     'sm': sm
#                 }
#                 highest_sm = sm
#     return best_wall  # returns None if no match found


def saveResult(filename, teacher, input_data, final_score, timestamp):
    
    timestamp = datetime.strptime(timestamp, '%B %d, %Y %H:%M:%S')

    conn = None
    try:
        conn = db_connection()
        
        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO results (filename, teacher, sf, pgfi, pf, eb, sm, tt, mc, score, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (filename, teacher, input_data["sf"], input_data["pgfi"], input_data["pf"], input_data["eb"], input_data["sm"], input_data["tt"], input_data["mc"], final_score, timestamp))
            
            conn.commit()
            
            return 200, None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None, f"Unexpected error: {str(e)}"
    finally:
        if conn:
            conn.close()
def convert_for_json(data):
    """Recursively convert objects for JSON serialization."""
    if isinstance(data, np.bool_):
        return bool(data)
    elif isinstance(data, list):
        return [convert_for_json(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_for_json(value) for key, value in data.items()}
    else:
        return data
def workingScore(assesses, socketio):

    matchresult = []
    if (len(assesses)) != 0:
        step = 100 / (len(assesses))
        pros = 0
        
        for assess in assesses:
            try:
                
                # wall_dir = current_app.config['WALL_FOLDER']

                # Parse file metadata
                parts = assess['filename'].split('-')
                if len(parts) >= 4:
                    filename, teacher, timestamp_f = parts[0], parts[1], parts[2]
                    timestamp = getTime(timestamp_f.split('.')[0])
                else:
                    raise ValueError(f"Invalid filename format: {assess.filename}")

                # Stylometric scoring
                # kt = calculate_kt_entropy(assess['content'])             

                # walline_walls = load_walls(wall_dir)
                # wall_match = select_best_wall(assess['content'], walline_walls)
                sf = calculate_sf(assess['content'])
                sm = calculate_sm(assess['content'])
                pf = calculate_pf(assess['content'])
                eb = calculate_eb(assess['content'])
                tt = calculate_tt(assess['content'])
                mc = calculate_mc(assess['content'])
                pgfi = calculate_pgfi(assess['content'])
                input_data = {
                    "sf": sf,
                    "pf": pf,
                    "eb": eb,
                    "sm": sm,
                    "tt": tt,
                    "mc": mc,
                    "pgfi": pgfi
                }

                pros += step

                # final_score, status = calculate_prufia_final_score(input_data)

                # Label & flag logic based on stylometric overall_score
                # if final_score >= 72:
                #     label, flag = "Match", "green"
                # elif final_score >= 0:
                #     label, flag = "Possible Mismatch", "red"
                # else:
                #     label, flag = "Insufficient Stylometric Data", "Incomplete Submission"
                #     final_score = "N/A"
                # traits = extract_raw_metrics(assess['content'])
                # echo = echo_decision(traits)

                # result, traits = run_echo_decision_logic(assess['content'])
                # echo_result = result["result"]
                sentences = [s.strip() for s in re.split(r'[.!?]', assess['content']) if s.strip()]
                analyzer_instance = SimpleAnalyzer()
                observer = ConsciousnessObserver(analyzer_instance)
                conciousness = observer.observe_layers(assess['content'], sentences)
                results_as_dicts = [convert_for_json(result.to_dict()) for result in conciousness]

                result = run_full_pipeline(assess['content'])
                traits = result["metrics"]
                print("Traits:", traits)
                final_result = result["final_result"]
                
                # htl_result = check_htl(traits)
                # mdt_passed = check_mdt(traits)
                # drift_passed = check_drift(traits)
                # fusion_passed = check_fusion(traits)
                
                # echo_result, reason = final_prufia_decision(echo, mdt_passed=True, drift_passed=True, fusion_passed=True)
                
                # print("htl_result:", htl_result, "Echo before drift:", echo, "mdt_passed:", mdt_passed, "drift_passed:", drift_passed, "fusion_passed:", fusion_passed, "Echo after drift:", echo_result)

                if final_result.lower() == "match":
                    label, flag = "Match", "green"
                elif final_result.lower() == "mismatch":
                    label, flag = "Mismatch", "red"
                else:
                    label, flag = "Needs Review", "gray"  # Escalation zone – pass to MDT, HTL, or Drift"

                # final_score = max(round(final_score, 2), 0) if isinstance(final_score, float) or isinstance(final_score, int) else 0

                item = {
                    "flag": flag,
                    # "base_score": round(final_score, 2),
                    "echo_result": final_result,
                    "reason": "",
                    "filename": filename,
                    "name_or_alias": "",
                    "time": timestamp,
                    "teacher": teacher,
                    "label": label,
                    "traits": traits,
                    "conciousness": results_as_dicts,
                    # "htl_result": htl_result,
                    # "mdt_passed": mdt_passed,
                    # "drift_passed": drift_passed,
                    # "fusion_passed": fusion_passed,
                    # "edit_analysis": edit_results,
                    "stylometrics": {
                        "SentenceVariation": traits['SentenceVariation'],
                        "punctual": traits["PunctuationRhythm"],
                        "vocabulary_entropy": traits["VocabularyEntropy"],
                        "pgfi_display": traits["PGFIDisplay"],
                        "StructureConsistency": traits["StructureConsistency"],
                        "TemporalTempo": traits["TemporalTempo"],
                        "PhraseReuse": traits["PhraseReuse"],
                    }
                }
                matchresult.append(item)
                
                saveResult(filename, teacher, input_data, 0, timestamp)

                socketio.emit('progress', {
                    'func_name': assess['filename'],
                    'value': int(pros)
                }, room='admin-room')

            except (AttributeError, IndexError, ValueError) as e:
                print(f"Error processing: {str(e)}")
                continue
        saveLog(teacher, "triger_score_logic")
        
    return matchresult

# Disabled for later integrated



def apply_prufia_patch_v1_2(final_score, pgfi, sm, kt, structure_consistency):
    if sm == 0 and pgfi < 15 and kt > 85:
        final_score -= 15
    if final_score < 75 and pgfi < 30 and sm > 25:
        final_score += 10
    if final_score < 75 and structure_consistency > 0.85:
        final_score += 5
    return final_score

