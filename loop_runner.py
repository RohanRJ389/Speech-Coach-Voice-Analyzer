import time

from features import calculate_intensity , calculate_pitch_variation #audio
from features import calculate_disfluency_rate , calculate_speech_rate #sentence

import wave
import numpy as  np

from assemblyAIS2T import speech2Text

from back import get_loop_status

if __name__=="__main__":
    

    prev_speech_rate = None
    complete_speech = ""
    


    while True:
        while not get_loop_status():
            
            time.sleep(3)
        
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
        
        print(str.upper("one iteration of metric updation complete !"))
        
            
            