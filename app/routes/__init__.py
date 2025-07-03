from flask import Flask
from flask_socketio import SocketIO
import os

def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, '../templates')
    STATIC_DIR = os.path.join(BASE_DIR, '../static')

    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR,
    )
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    app.secret_key = 'prufia_user'
    app.config['ASSIGNMENT_FOLDER'] = 'assignments'
    app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB
    
    os.makedirs(app.config['ASSIGNMENT_FOLDER'], exist_ok=True)

    from .admin_routes import admin_bp
    from .teacher_routes import teacher_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')

    return app, socketio
