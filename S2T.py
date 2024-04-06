# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

from vosk import KaldiRecognizer,Model
import wave
# model = Model(r"C:\Users\Sathvik Malgikar\Downloads\vosk-model-en-us-0.22\vosk-model-en-us-0.22")
model = Model(r"C:\Users\Sathvik Malgikar\Downloads\vosk-model-en-us-0.22\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model,16000)


def speech2Text(speechFile):
    # Open the WAV file for reading
    with wave.open(speechFile, 'rb') as wf:
        # Read audio data from the WAV file
        audio_data = wf.readframes(wf.getnframes())
        
        # Feed audio data to the recognizer
        recognizer.AcceptWaveform(audio_data)
        
        # Get the final recognition result
        result = recognizer.FinalResult()
        if result is  None:
            return ""
        return result[14:-3]


if __name__ == "__main__":
    
    print(speech2Text("concat_output.wav"))
    # print(speech2Text("india.wav"))