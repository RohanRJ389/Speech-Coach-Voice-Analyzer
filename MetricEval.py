import time

from features import calculate_intensity , calculate_pitch_variation #audio
from features import calculate_disfluency_rate , calculate_speech_rate #sentence

import wave
import numpy as  np

from voskS2T import speech2Text

import json

prev_speech_rate = None
complete_speech = ""

json_file_path = "metrics.json"
cumulative_json_file_path = "c_metrics.txt"

def generate_tip(metrics):
    return "Your voice is too feeble !"

    
def one_iteration():  
    global prev_speech_rate, complete_speech  
    audio_file = "concat_output.wav"
    audio = wave.open(audio_file, 'rb')

    # Read audio data
    audio_data = np.frombuffer(audio.readframes(-1), dtype=np.int16)

    # Close audio file
    audio.close()

    intensity = calculate_intensity(audio_data)
    print("Intensity:", intensity)
    
    # Calculate pitch variation
    pitch_variation = calculate_pitch_variation(audio_file)
    print("Pitch Variation:", pitch_variation)
    
    text_transcript = speech2Text(audio_file)
    complete_speech+=text_transcript
    
    
    print("speech to text returned : " + text_transcript)
    
    # Calculate disfluency rate
    disfluency_rate = calculate_disfluency_rate(text_transcript)
    print("Disfluency Rate:", disfluency_rate)
    
    # Calculate speech rate (assuming speech duration is known)
    speech_rate, consistency_score = calculate_speech_rate(text_transcript, audio_file, prev_speech_rate)# TODO EWMA
    
    prev_speech_rate = speech_rate
    
    print("Speech Rate:", speech_rate)
    print("Consistency Score:", consistency_score)
    
    # File path to save the JSON file
   
    
    metrics = {
        "intensity" : intensity,
        "pitch_variation" : pitch_variation,
        "disfluency_rate"  : disfluency_rate,
        "speech_rate" : speech_rate,
        "consistency_score" : consistency_score,  
        "complete_speech" : complete_speech
    }
    tip = generate_tip(metrics)
    metrics["tip"] = tip

    # Write metrics to JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(metrics, json_file, indent=4)
    with open(cumulative_json_file_path, "a") as json_file:
        json.dump(metrics, json_file, indent=4)
        
    print(str.upper("one iteration of metric updation complete !"))
    

if __name__ =="__main__":
    with open(json_file_path, "w") as json_file:
        json_file.write("{}")
    with open(cumulative_json_file_path, "w") as json_file:
        json_file.write("{}")
    while True:
        
        one_iteration()
        
        

