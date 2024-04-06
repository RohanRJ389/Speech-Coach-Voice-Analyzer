
import './App.css';

import { useEffect, useState} from "react"

import { WavRecorder  } from 'webm-to-wav-converter';

import LineChart from './LineChart.js';
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

let recordingMode = false

// this will initialize global mediaRecorder

function App() {
  
  
  let clipDuration = 5  
  
  function startRecording() {
    
    recordingMode = true
    recordOneSec()
    socket.emit("message","RECORD START")
  
  }
  function stopRecording() {
    
    socket.emit("message","RECORD STOP")
     
    recordingMode = false;
  }
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
  const [numBlobs, setnumBlobs] = useState(2)

  function recordOneSec() {

    console.log("took a clip")
    setnumBlobs(prev=>prev-1)
    // To start recording
    wavRecorder.start();
    
    setTimeout(() => {
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
        if (recordingMode) {
          recordOneSec()
        }
        })
      }, 1000  * clipDuration);
  
  
    // // To download the wav file in 32-bit encoding with AudioContext options
    // wavRecorder.download('myFile.wav',true, { sampleRate:  48000 });
  }
  

  useEffect(() => {
    initializeMic()
  
    return () => {
      wavRecorder = null
    }
  }, [])

  return (
    <div className="App">
      <header className="App-header">
  
        
    {   numBlobs<0 ?  <p>
          Recording is on
        </p> : 
        <p>
          Recording is off
        </p>}
        <div style={{"display" : "flex" , "flexDirection" : "row"}} >
          
          <button onClick={startRecording} style={{ fontSize: 20 }}  >START </button>
          <div style={{width : 20}} ></div>
        <button onClick={stopRecording} style={{fontSize : 20}}  >STOP </button>
        
  </div>
      <LineChart/>
      
      </header>

    </div>
  );
}

export default App;
