from flask import Flask
from flask_socketio import SocketIO
import logging

import io
import wave
import os

from flask_cors import CORS

def create_directory(directory_path):
    try:
        # Create directory
        os.mkdir(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def empty_directory(directory):
    # Check if the directory exists
    if os.path.exists(directory):
        # Iterate over all the files and subdirectories in the directory
        for file_or_dir in os.listdir(directory):
            # Construct the full path
            full_path = os.path.join(directory, file_or_dir)
            # If it's a file, remove it
            if os.path.isfile(full_path):
                os.remove(full_path)
            # If it's a directory, recursively empty it
            elif os.path.isdir(full_path):
                empty_directory(full_path)
        # Once all files and subdirectories are removed, remove the directory itself
        os.rmdir(directory)
        print(f"The directory '{directory}' has been emptied.")
    else:
        print(f"The directory '{directory}' does not exist.")



if __name__=="__main__":
    
    empty_directory("captured_audio")
    create_directory("captured_audio")
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

loop_should_run = False

# Event handler for when a client sends a message via WebSocket
@socketio.on('message')
def handle_message(message):
    global loop_should_run
    if message == "RECORD STOP":
        loop_should_run=False
    elif message == "RECORD START":
        loop_should_run=True
    print('Received message:', message)
    # You can broadcast the message to all connected clients, or perform any other actions here
    socketio.send('Message received: ' + message)


@app.route('/get_text')
def get_text():
    # Assuming your text file is named 'corrected.txt' and located in the same directory as your Flask app
    text_file_path = 'transcript.txt'
    
    try:
        with open(text_file_path, 'r') as file:
            text_content = file.read()
        return text_content
    except FileNotFoundError:
        return "Text file not found", 404
    
@app.route('/getc_text')
def getc_text():
    # Assuming your text file is named 'corrected.txt' and located in the same directory as your Flask app
    text_file_path = 'corrected.txt'
    
    try:
        with open(text_file_path, 'r') as file:
            text_content = file.read()
        return text_content
    except FileNotFoundError:
        return "Text file not found", 404
  
import json  
  
@app.route('/finalScore')
def getfinalScore():
    # Open the JSON file
    with open('frontend/src/metrics.json', 'r') as file:
        # Load JSON data from the file
        data = json.load(file)
    return str(data["master_score"])

num = 1

from scipy.signal import hann

def apply_fade(data):
    fade_len = 50
    fade_in_window = hann(fade_len * 2)[:fade_len]
    fade_out_window = hann(fade_len * 2)[fade_len:]

    # Create a writable copy of the data array
    data = data.astype(np.float64)

    # Apply fade-in and fade-out effects
    data[:fade_len] *= fade_in_window
    data[-fade_len:] *= fade_out_window
    
    return data.astype(np.int16)


import wave
import numpy as np


def concatenate_bytesio_to_wav(byteio_files, output_file):
    global num
    num+=1
    # Open the output WAV file for writing
    with wave.open(output_file, 'wb') as wav_out:
        
        # Initialize variables to hold parameters
        first_time =True
        
        # Iterate through each BytesIO file
        for byteio_file in byteio_files:
            # Reset the position to the beginning of the BytesIO file
            byteio_file.seek(0)
            
            # Read the BytesIO file content
            content = byteio_file.read()
            
            # If it's the first BytesIO file, extract the parameters and set them for the output WAV file
            if first_time:
                first_time=False
                # wav_in = wave.open(byteio_file, 'rb')
                # sample_width = wav_in.getsampwidth()
                # channels = wav_in.getnchannels()
                # frame_rate = wav_in.getframerate()
                # wav_in.close()
                
                # Set the parameters for the output WAV file
                wav_out.setparams((2, 2, 48000//2, 48000//5//2, 'NONE', 'compressed'))
            
            content_array = np.frombuffer(content, dtype=np.int16)
            content_array = apply_fade(content_array)
            content = content_array.tobytes()

            # Write the content of the BytesIO file to the output WAV file
            wav_out.writeframes(content)
    
    print("Concatenation completed successfully!")
    # num+=1

# Example usage:
# Assuming `byteio_files` is a list of io.BytesIO file-like objects and `output_file` is the output WAV file path
# concatenate_bytesio_to_wav(byteio_files, 'output.wav')


import time
import base64


def base64_to_blob(base64_string):
    # Decode the Base64 string to bytes
    blob_data = base64.b64decode(base64_string)
    
    # Create a BytesIO object to simulate a file-like object
    blob_file = io.BytesIO(blob_data)
    
    return blob_file

if __name__=="__main__":
    window =[]
    max_window_size = 2


@socketio.on('media')
def handle_media(message):
    blob = base64_to_blob(message)
    window.append(blob)
    print(type(blob),blob)
    if len(window)>max_window_size:
        window.pop(0)
    print(len(window))
    if(len(window)<max_window_size):return # concat file wont be generated
    t1= time.time()
    concatenate_bytesio_to_wav (window,f"captured_audio/concat_output{num}.wav")
    print (f"concatenation finished in { time.time() - t1} seconds" )
    
    

    
# Event handler for when a client disconnects from the WebSocket
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
  
    socketio.run(app   )
    # app.run(debug=True)
