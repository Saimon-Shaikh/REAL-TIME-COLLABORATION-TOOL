from flask import Flask, request
from flask_socketio import SocketIO, emit
import random
import secrets
import os

app = Flask(__name__)
# IMPORTANT: Use a secure secret key for session management in production.
app.config['SECRET_KEY'] = 'codtech_task3_secret_key_' + secrets.token_hex(8)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Global State ---
# Store the current shared text (Volatile storage for demonstration)
SHARED_TEXT = "Welcome to the real-time collaborative editor! Start typing below, and anyone else connected will see your changes instantly."

# Store connected users: { sid: username }
CONNECTED_USERS = {}

def generate_username(sid):
    """Generates a friendly and unique initial username."""
    adjectives = ['Agile', 'Bright', 'Quick', 'Fast', 'Clever', 'Witty', 'Smart', 'Ready']
    nouns = ['Coder', 'Dev', 'Writer', 'Collaborator', 'Explorer', 'Thinker', 'Editor']
    # Use part of the SID as a unique suffix
    random_suffix = sid[:4]
    return f"{random.choice(adjectives)}{random.choice(nouns)}-{random_suffix}"

def emit_user_list():
    """Calculates user list and broadcasts the update to all connected clients."""
    user_list = list(CONNECTED_USERS.values())
    emit("user_list_update", {"users": user_list}, broadcast=True)

# --- FLASK ROUTE (Simple health check) ---
@app.route("/")
def index():
    """Simple health check route."""
    return "The SocketIO server is running! Open index.html in your browser to connect.", 200

# --- SOCKET EVENTS ---

@socketio.on("connect")
def handle_connect():
    sid = request.sid
    # 1. Assign a unique, friendly initial name
    CONNECTED_USERS[sid] = generate_username(sid) 
    
    # 2. Send current shared text to the connecting user
    emit("load_history", {"text": SHARED_TEXT})
    
    # 3. Update all clients with current user list
    emit_user_list()
    print(f"[JOIN] {CONNECTED_USERS[sid]} connected.")

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    if sid in CONNECTED_USERS:
        username = CONNECTED_USERS.pop(sid)
        # Update all clients with current user list
        emit_user_list()
        print(f"[LEAVE] {username} disconnected.")

@socketio.on("text_change")
def handle_text_change(data):
    """Updates global state and broadcasts change to others."""
    global SHARED_TEXT
    new_text = data.get("text", "")
    SHARED_TEXT = new_text
    # Broadcast to all clients EXCEPT the sender (include_self=False)
    emit("update_text", {"text": new_text}, broadcast=True, include_self=False)

@socketio.on("register_user")
def handle_register_user(data):
    """Updates the username for the current session ID and broadcasts the new list."""
    sid = request.sid
    username = data.get("username", "").strip()
    
    # Basic validation for name length
    if not username or len(username) < 3:
        return 
        
    CONNECTED_USERS[sid] = username
    # Update all clients with current user list
    emit_user_list()
    print(f"[REGISTER] SID {sid[:4]} set name to {username}")

if __name__ == "__main__":
    print("Starting SocketIO Server on port 5000...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
