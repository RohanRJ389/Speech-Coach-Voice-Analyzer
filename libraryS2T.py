# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import speech_recognition as sr

def speech2Text(speechFile):

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


if __name__ == "__main__":
    
    # print(speech2Text("concat_output.wav"))
    print(speech2Text("india.wav"))