import os
import numpy as np

from flask import current_app

def allowed_file(filename):
    """
    Check if the file has an allowed extension
    (reads from current_app.config['ALLOWED_EXTENSIONS']).
    """
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    )

def make_json_serializable(data):
    """
    Recursively convert numpy arrays/float32, lists, dicts
    into JSON-serializable Python types.
    """
    if isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, np.float32):
        return float(data)
    elif isinstance(data, list):
        return [make_json_serializable(item) for item in data]
    elif isinstance(data, dict):
        return {key: make_json_serializable(value) for key, value in data.items()}
    else:
        return data
