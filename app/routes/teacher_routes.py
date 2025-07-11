import os
import time
import shutil
import unicodedata
import re
from flask import (
    Blueprint, request, jsonify, render_template,
    redirect, url_for, session, current_app
)
from run import socketio

# Service‐layer imports
from app.services.auth.login import handle_teacher_login

from app.services.teacher.business import workingScore
from app.services.common.fileread import read_file

# Utility functions from our utils module
from app.routes.utils import (
    allowed_file,
    make_json_serializable,
)

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/teacher')
def teacher_home():
    """
    Teacher’s dashboard: must be logged in (session['teacher_id']).
    """
    if 'teacher_id' not in session:
        return redirect(url_for('teacher.teacherlogin'))

    return render_template(
        'teacher_page.html',
    )



@teacher_bp.route('/teacher-login')
def teacherlogin():
    """
    Show teacher login form (GET).
    """
    return render_template('teacherlogin.html')


@teacher_bp.route('/teacher-login', methods=['POST'])
def teacher_login():
    """
    Handle teacher login (POST).
    """
    result, status_code = handle_teacher_login()
    if status_code != 200:
        return render_template('teacherlogin.html', error=result.get('error', 'Unknown error')), status_code

    session['teacher_id'] = result['teacher_id']
    session['teacher_email'] = result['email']

    return redirect(url_for('teacher.teacher_home'))

@teacher_bp.route('/validations-content')
def validations_content():
    """
    Dummy “validations” page (static data for now).
    """
    validations = [
        {'assignment': 'Assignment 1', 'status': 'Needs review'},
        {'assignment': 'Assignment 2', 'status': 'Needs review'}
    ]
    return render_template('teacher/validations.html', validations=validations)


# Existing constants
_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = ("CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", 
                        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", 
                        "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9")

def secure_filename(filename: str, teacher: str = "teacher1", semester: str = "semester1",timestamp:str="") -> str:
    """Generate a secure filename in format: OriginalName-teacher-semester-timestamp.ext
    
    Args:
        filename: Original filename (e.g., "My File.pdf")
        teacher: Teacher identifier (default: "teacher1")
        semester: Semester identifier (default: "semester1")
        
    Returns:
        Formatted filename (e.g., "My_File-john_doe-fall2023-20230615143022.pdf")
    """
    # 1. Process original filename
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")
    
    # Replace path separators and special chars
    for sep in os.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    
    # Clean while preserving spaces between words
    safe_name = _filename_ascii_strip_re.sub("", "_".join(filename.split())).strip("._")
    
    # 2. Split name and extension
    name_parts = safe_name.rsplit(".", 1)
    base_name = name_parts[0]
    ext = f".{name_parts[1]}" if len(name_parts) > 1 else ""
    
   # 4. Handle Windows reserved names
    if os.name == "nt" and base_name.upper() in _windows_device_files:
        base_name = f"_{base_name}"
    
    # 5. Combine all parts
    return f"{base_name}-{teacher}-{semester}-{timestamp}{ext}"



@teacher_bp.route('/upload_assignments', methods=['POST'])
def upload_assignments():
    """
    Endpoint to upload assignments (files). 
    Automatically attempts to save each file under ASSIGNMENT_FOLDER.
    """
    results = {}

    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist('files')
    timestamps = request.form.getlist('timestamps')
    original_names = request.form.getlist('original_names')
    teacher =  session['teacher_email']
    if not files or all(file.filename == '' for file in files):
        return jsonify({"error": "No selected files"}), 400

    for i, file in enumerate(files):
        if file and allowed_file(file.filename):
            timestamp = timestamps[i] if i < len(timestamps) else str(int(time.time()))
            # Keep the original secure filename (the extra args in the original code were incorrect);
            # Here we simply secure the filename itself.

            filename = secure_filename(file.filename,teacher, timestamp)

            folder_path = current_app.config['ASSIGNMENT_FOLDER']
            os.makedirs(folder_path, exist_ok=True)

            unique_filename = f"{filename}"
            file_path = os.path.join(folder_path, unique_filename)
            file.save(file_path)

            results = {
                'score': 'N/A',
                'interpretation': 'Manual Match Required',
                'saved_path': file_path
            }
        else:
            results[file.filename] = {
                'error': 'Invalid file type',
                'allowed_types': list(current_app.config['ALLOWED_EXTENSIONS'])
            }

    return jsonify(results)

@teacher_bp.route('/match_assignments', methods=['POST'])
def handle_match_assignments():
    """
    Given a list of timestamps  attempt to match
    assignment files (timestamp in filename) , then run workingScore().
    """
    data = request.get_json()
    timestamp = data.get('timestamp')
    print(f"Received timestamp: {timestamp}")

    assignments_dir = current_app.config['ASSIGNMENT_FOLDER']

    matching_files = []
    try:
        for filename in os.listdir(assignments_dir):
            if str(timestamp) in str(filename):
                file_path = os.path.join(assignments_dir, filename)
                if os.path.isfile(file_path):
                    try:
                        content = read_file(file_path)
                        matching_files.append({
                            'filename': filename,
                            'path': file_path,
                            'content': content,
                        })
                    except Exception as e:
                        matching_files.append({
                            'filename': filename,
                            'path': file_path,
                            'error': f"Could not read file: {str(e)}"
                        })

    except FileNotFoundError:
        return jsonify({'error': 'Assignments directory not found'}), 404

    matchdata = workingScore(matching_files, socketio)

    matchdata_serializable = make_json_serializable(matchdata)

    return jsonify({
        'status': 'success',
        'received_timestamp': timestamp,
        'data': matchdata_serializable
    })


@teacher_bp.route('/teacher-logout')
def teacher_logout():
    """
    Clear teacher session and redirect to login.
    """
    session.clear()
    return jsonify({'redirect_url': url_for('teacher.teacherlogin')})

