
import './App.css';

import { useEffect} from "react"


// // Create a new WebSocket connection
// const socket = new WebSocket('ws://127.0.0.1:5000');

import { io } from "socket.io-client";

const socket = io("ws://127.0.0.1:5000", {
  transports: ["websocket"],
  cors: {
    origin: "http://localhost:3000/",
  },
});

// Event listener for when the connection is opened
socket.on('open', function (event) {
    console.log('WebSocket connection established');
    
    // Send a "hi" message to the backend
    socket.send('hi');
});

// Event listener for receiving messages from the backend
socket.on('message', function (data) {
    console.log('Message from server:', data);
});

// Event listener for errors
socket.on('error', function (event) {
    console.error('WebSocket error:', event);
});

// Event listener for when the connection is closed
socket.on('close', function (event) {
    console.log('WebSocket connection closed');
});

function blobToBase64(blob, callback) {
  blob = new Blob([blob], { type: 'audio/wav' });
  console.log("after cast to wav")
  console.log(blob)
  var reader = new FileReader();
  reader.readAsDataURL(blob);
  reader.onloadend = function() {
      var base64Data = reader.result;
      // Remove the prefix (data:image/png;base64,) from the base64 string if needed
      // For example, if the blob is an audio file, you might not have an image prefix.
      var base64WithoutPrefix = base64Data.split(',')[1];
      callback(base64WithoutPrefix);
  }
}

function startRecording() {
  
  // navigator.mediaDevices.enumerateDevices().then(data => console.log(data))
  if (mediaRecorder == null) {
    console.log("media recorder not initialized!!")
    return
  }
  mediaRecorder.start(1000);
  console.log(mediaRecorder.state)
  
  mediaRecorder.ondataavailable = (e) => {
    
    blobToBase64(e.data, (b64encoding => {
      
      socket.emit("media", b64encoding)
      // console.log(b64encoding)
    }))
    
  };
}
function stopRecording() {
  
   
  mediaRecorder.stop();
  console.log(mediaRecorder.state)
  
  mediaRecorder.ondataavailable = null
}




let mediaRecorder = null

// this will initialize global mediaRecorder
function initializeMic() {
   
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    console.log("getUserMedia supported.");
    navigator.mediaDevices
      .getUserMedia(
        // constraints - only audio needed for this app
        {
          audio: true,
        },
      )
  
      // Success callback
      .then((stream) => {
        mediaRecorder = new MediaRecorder(stream);// GLOBAL mediaRecorder
        
        console.log(mediaRecorder)
        

      })
  
      // Error callback
      .catch((err) => {
        console.error(`The following getUserMedia error occurred: ${err}`);
      });
  } else {
    console.log("getUserMedia not supported on your browser!");
  }
}

function App() {

  useEffect(() => {
    initializeMic()
  
    return () => {
      mediaRecorder = null
    }
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <button onClick={startRecording}  >startRecording</button>
        <button onClick={stopRecording}  >stopRecording</button>
      </header>
    </div>
  );
}

export default App;
