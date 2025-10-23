# Real-Time Collaboration Server (Task 3)
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

# --- Configuration ---
app = Flask(__name__)
# IMPORTANT: For demonstration, we allow all origins.
# For production, replace "*" with your specific client URL.
app.config['SECRET_KEY'] = 'codtech_task3_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Global State ---
# This dictionary stores the content for the single shared document.
# 'document' is the name of the room all users join.
SHARED_TEXT = {
    'document': "Welcome to the real-time collaborative editor! Start typing below, and anyone else connected will see your changes instantly."
}

# --- Flask Routes ---

@app.route('/')
def index():
    """
    Main route. Confirms the server is running.
    """
    return "The SocketIO server is running! Open your browser to the client file (index.html) to connect.", 200

# --- Socket.IO Event Handlers ---

def get_user_count(room='document'):
    """Calculates the number of unique users currently connected to the specified room."""
    try:
        # Access the SocketIO internal structure to get session IDs in the room
        room_members = socketio.server.manager.rooms.get('/', {}).get(room, {})
        return len(room_members)
    except Exception:
        return 0

@socketio.on('connect')
def handle_connect():
    """Handles new client connections."""
    room = 'document'
    join_room(room) # Place the user in the 'document' room

    # 1. Send the current document state only to the connecting client
    emit('load_history', {'text': SHARED_TEXT[room]}, room=request.sid)

    # 2. Update and broadcast the new user count to all clients
    user_count = get_user_count(room)
    emit('user_count_update', {'count': user_count}, room=room, broadcast=True)
    print(f'Client {request.sid[:4]} joined room {room}. Total users: {user_count}')


@socketio.on('disconnect')
def handle_disconnect():
    """Handles client disconnections."""
    room = 'document'
    leave_room(room)

    # Update and broadcast the new user count to all clients
    user_count = get_user_count(room)
    emit('user_count_update', {'count': user_count}, room=room, broadcast=True)
    print(f'Client {request.sid[:4]} left room {room}. Total users: {user_count}')


@socketio.on('text_change')
def handle_text_change(data):
    """
    Handles real-time text updates from a client, updates the global state, and
    broadcasts the change to all other clients in the 'document' room.
    """
    new_text = data.get('text', '')
    room = 'document'

    # 1. Update the global shared state
    SHARED_TEXT[room] = new_text

    # 2. Broadcast the change to all *other* users in the room
    # 'skip_sid=request.sid' prevents echoing the change back to the sender
    emit('update_text', {'text': new_text}, room=room, skip_sid=request.sid)


# --- Run the Server ---
if __name__ == '__main__':
    # Use socketio.run instead of app.run for WebSocket capability
    print("Starting SocketIO Server on port 5000...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
