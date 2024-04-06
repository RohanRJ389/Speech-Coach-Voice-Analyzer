# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import speech_recognition as sr

import threading

# Define a timeout handler
def timeout_handler(signum, frame):
    raise TimeoutError("Function call timed out")



def speech2Text(speechFile):
    
    # Set the alarm signal
    timer = threading.Timer(10, timeout_handler)

    

    def foo():
        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Load audio file
        with sr.AudioFile(speechFile) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            
            # Read the audio data
            audio_data = recognizer.record(source)
            
        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        return ""  # Return empty string if speech recognition fails
    
    try:
    # Start the timer
        timer.start()

    # Call your function
        val = foo()

    except TimeoutError as e:
        print(e)
        return ""

    finally:
        # Cancel the timer (if it hasn't already been triggered)
        timer.cancel()
        return val


if __name__ == "__main__":
    
    print(speech2Text("captured_audio/concat_output1.wav"))
    print(speech2Text("captured_audio/concat_output2.wav"))
    print(speech2Text("captured_audio/concat_output3.wav"))
    print(speech2Text("captured_audio/concat_output4.wav"))
    print(speech2Text("captured_audio/concat_output5.wav"))
    print(speech2Text("captured_audio/concat_output6.wav"))
    print(speech2Text("captured_audio/concat_output7.wav"))
    print(speech2Text("captured_audio/concat_output8.wav"))
    print(speech2Text("captured_audio/concat_output9.wav"))
    # print(speech2Text("india.wav"))