from flask import Flask
from flask_socketio import SocketIO
import logging

from flask_cors import CORS

app = Flask(__name__ )
CORS(app)
socketio = SocketIO(app, cors_allowed_origins = "*")

# Route to serve the HTML page with the JavaScript WebSocket code
@app.route('/')
def index():
    return "hello server is on"

# Event handler for when a client connects to the WebSocket
@socketio.on('connect')
def handle_connect():
    socketio.emit("message","how are you?")
    print('Client connected')

# Event handler for when a client sends a message via WebSocket
@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    # You can broadcast the message to all connected clients, or perform any other actions here
    socketio.send('Message received: ' + message)

window =[]

@socketio.on('media')
def handle_media(message):
    window.append(message)
    if len(window)>10:
        window.pop(0)
    print(len(window))
    
    

    
# Event handler for when a client disconnects from the WebSocket
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app   )
    # app.run(debug=True)
