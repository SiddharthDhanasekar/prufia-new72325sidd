from flask import Blueprint, render_template, redirect, url_for
from run import socketio

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Show the landing page (index.html).
    """
    # return render_template('index.html')
    return redirect(url_for('teacher.teacher_home'))


# @socketio.on('join-admin-room')
# def handle_join_admin_room():
#     """
#     When an admin‐client joins the 'admin-room' (via SocketIO),
#     add them to that room so we can emit passcode/reset events.
#     """
#     from flask_socketio import join_room
#     join_room('admin-room')
#     print("Admin joined admin-room")
