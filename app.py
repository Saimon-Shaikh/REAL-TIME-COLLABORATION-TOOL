# Real-Time Collaboration Server with Live User List
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

# --- Configuration ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'codtech_task3_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Global State ---
SHARED_TEXT = {
    'document': "Welcome to the real-time collaborative editor! Start typing below, and anyone else connected will see your changes instantly."
}

# Track connected users per room
CONNECTED_USERS = {
    'document': {}  # room_name: { sid: username }
}


# --- Flask Routes ---
@app.route('/')
def index():
    """Simple health check route."""
    return "The SocketIO server is running! Open index.html in your browser to connect.", 200


# --- Helper Functions ---
def get_user_count(room='document'):
    """Calculates the number of unique users currently connected to the specified room."""
    try:
        room_members = socketio.server.manager.rooms.get('/', {}).get(room, {})
        return len(room_members)
    except Exception:
        return 0


# --- Socket.IO Event Handlers ---
@socketio.on('connect')
def handle_connect():
    """Handles new client connections."""
    room = 'document'
    join_room(room)

    # Assign a temporary username (e.g., User-AB12)
    username = f"User-{request.sid[:4]}"
    CONNECTED_USERS[room][request.sid] = username

    # Send the current document content to the newly connected user
    emit('load_history', {'text': SHARED_TEXT[room]}, room=request.sid)

    # Update all clients about the new user list and count
    user_count = get_user_count(room)
    user_list = list(CONNECTED_USERS[room].values())

    emit('user_count_update', {'count': user_count}, room=room, broadcast=True)
    emit('user_list_update', {'users': user_list}, room=room, broadcast=True)

    print(f"[JOIN] {username} connected. Users now: {user_count}")


@socketio.on('disconnect')
def handle_disconnect():
    """Handles client disconnections."""
    room = 'document'
    leave_room(room)

    username = CONNECTED_USERS[room].pop(request.sid, None)
    user_count = get_user_count(room)
    user_list = list(CONNECTED_USERS[room].values())

    emit('user_count_update', {'count': user_count}, room=room, broadcast=True)
    emit('user_list_update', {'users': user_list}, room=room, broadcast=True)

    print(f"[LEAVE] {username or 'Unknown user'} disconnected. Users now: {user_count}")


@socketio.on('text_change')
def handle_text_change(data):
    """Handles real-time text updates and broadcasts them to all connected clients."""
    new_text = data.get('text', '')
    room = 'document'

    # Update global shared state
    SHARED_TEXT[room] = new_text

    # Broadcast update to everyone except sender
    emit('update_text', {'text': new_text}, room=room, skip_sid=request.sid)


# Optional: Support setting a custom username after connection
@socketio.on('register_user')
def register_user(data):
    """Allows clients to set a custom display name after connecting."""
    room = 'document'
    username = data.get('username', f"User-{request.sid[:4]}")
    CONNECTED_USERS[room][request.sid] = username

    user_list = list(CONNECTED_USERS[room].values())
    emit('user_list_update', {'users': user_list}, room=room, broadcast=True)
    print(f"[REGISTER] {username} updated their name.")


# --- Run the Server ---
if __name__ == '__main__':
    print("Starting SocketIO Server on port 5000...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
