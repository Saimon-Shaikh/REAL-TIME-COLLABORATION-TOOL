from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store the current shared text
shared_text = ""

# Store connected users: { sid: username }
connected_users = {}

@app.route("/")
def index():
    return render_template("index.html")

# --- SOCKET EVENTS ---

@socketio.on("connect")
def handle_connect():
    sid = request.sid
    # Add temporary guest name
    connected_users[sid] = f"Guest-{sid[:5]}"
    # Send current shared text
    emit("load_history", {"text": shared_text})
    # Update all clients with current user list
    emit_user_list()

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    if sid in connected_users:
        del connected_users[sid]
        emit_user_list()

@socketio.on("text_change")
def handle_text_change(data):
    global shared_text
    shared_text = data.get("text", "")
    emit("update_text", {"text": shared_text}, broadcast=True, include_self=False)

@socketio.on("register_user")
def handle_register_user(data):
    sid = request.sid
    username = data.get("username", f"Guest-{sid[:5]}")
    connected_users[sid] = username
    emit_user_list()

# Utility function to update all clients with current users
def emit_user_list():
    user_list = list(connected_users.values())
    emit("user_list_update", {"users": user_list}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
