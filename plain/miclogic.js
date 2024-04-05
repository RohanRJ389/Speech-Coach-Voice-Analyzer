function init() {
    
    
    let audfile = document.getElementById("temp source")
    
    // for legacy browsers
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    
    const audioContext = new AudioContext();
    
    const track = audioContext.createMediaElementSource(audfile)
    
    track.connect(audioContext.destination);
}


// Create a new WebSocket connection
const socket = new WebSocket('ws://127.0.0.1:5000');

// Event listener for when the connection is opened
socket.addEventListener('open', function (event) {
    console.log('WebSocket connection established');
    
    // Send a "hi" message to the backend
    socket.send('hi');
});

// Event listener for receiving messages from the backend
socket.addEventListener('message', function (event) {
    console.log('Message from server:', event.data);
});

// Event listener for errors
socket.addEventListener('error', function (event) {
    console.error('WebSocket error:', event);
});

// Event listener for when the connection is closed
socket.addEventListener('close', function (event) {
    console.log('WebSocket connection closed');
});
