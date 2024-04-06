
import './App.css';

import { useEffect} from "react"

import { WavRecorder  } from 'webm-to-wav-converter';

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
  console.log("after cast to wav")
  console.log(blob)
  var reader = new FileReader();
  reader.readAsDataURL(blob);
  reader.onloadend = function() {
      var base64Data = reader.result;
      // Remove the prefix (data:image/png;base64,) from the base64 string if needed
      // For example, if the blob is an audio file, you might not have an image prefix.
    var base64WithoutPrefix = base64Data.split(',')[1];
    console.log("before callback")
    // console.log(base64WithoutPrefix)
      callback(base64WithoutPrefix);
  }
}

let wavRecorder 

function recordOneSec() {

console.log("took a clip")
  // To start recording
  wavRecorder.start();
  
  // To stop recording
  wavRecorder.stop();
  
  // // To get the wav Blob in 32-bit encoding with AudioContext options
  wavRecorder.getBlob(false, { sampleRate: 48000 }).then(wavBlob => {
    
    if (wavBlob) {
      
      console.log(wavBlob)
      
      blobToBase64(wavBlob, (b64encoding => {
        
        socket.emit("media", b64encoding)
        // console.log(b64encoding)
      }))
      
    }
    })
  
  // To download the wav file in 32-bit encoding with AudioContext options
  wavRecorder.download('myFile.wav',true, { sampleRate:  48000 });

}

let clipDuration = 3

function startRecording() {
  
  recordingMode = true
  recInterval = setInterval(recordOneSec,clipDuration * 1000)

}
function stopRecording() {
  
   
  clearInterval(recInterval)  
  recordingMode = false;
}




let recordingMode = false
let recInterval = null

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
        wavRecorder = new WavRecorder();// GLOBAL wavRecorder
        
        // console.log(mediaRecorder)
        

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
      wavRecorder = null
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
