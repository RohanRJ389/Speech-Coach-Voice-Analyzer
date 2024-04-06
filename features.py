import wave
import numpy as np
import re
import parselmouth

# Parameters for pitch normalization
min_pitch = 50  # Minimum pitch in Hz
max_pitch = 500  # Maximum pitch in Hz

# Function to calculate intensity
def calculate_intensity(audio_data):
    # Calculate root mean square (RMS) amplitude
    rms = np.sqrt(np.mean(np.square(audio_data)))
    # Normalize RMS amplitude to a range of 0 to 1
    intensity = rms / np.iinfo(audio_data.dtype).max
    return intensity*100

# Function to calculate pitch
def calculate_pitch(audio_file):
    # Load audio file
    snd = parselmouth.Sound(audio_file)
    # Extract pitch (fundamental frequency)
    pitch = snd.to_pitch()
    # Calculate mean pitch
    mean_pitch = np.nanmean(pitch.selected_array['frequency'])
    # Normalize pitch to a range of 0 to 1
    pitch_norm = (mean_pitch - min_pitch) / (max_pitch - min_pitch)
    return pitch_norm

# Function to calculate variation in pitch (intonation)
def calculate_pitch_variation(audio_file):
    # Load audio file
    snd = parselmouth.Sound(audio_file)
    # Extract pitch (fundamental frequency)
    pitch = snd.to_pitch()
    # Calculate standard deviation of pitch values
    pitch_std = np.nanstd(pitch.selected_array['frequency'])
    # Normalize pitch variation to a range of 0 to 1
    pitch_variation = pitch_std / (max_pitch - min_pitch)
    return pitch_variation

# Function to detect pauses
def detect_pauses(audio_data, threshold=0.05, min_pause_duration=0.1):
    # Convert audio data to mono and normalize
    audio_normalized = audio_data / np.max(np.abs(audio_data))
    # Detect pauses using threshold
    pauses = np.where(audio_normalized < threshold)[0]
    # Filter out short pauses
    pause_intervals = []
    current_pause_start = None
    for i in range(len(pauses) - 1):
        if current_pause_start is None:
            current_pause_start = pauses[i]
        if pauses[i + 1] - pauses[i] > min_pause_duration * len(audio_normalized):
            pause_intervals.append((current_pause_start, pauses[i]))
            current_pause_start = None
    # Calculate pause duration and frequency
    pause_durations = [end - start for start, end in pause_intervals]
    total_pause_duration = sum(pause_durations)
    pause_frequency = len(pause_durations) / len(audio_normalized)
    return total_pause_duration, pause_frequency

def calculate_disfluency_rate(sentence):
    # Define the regex pattern to capture disfluencies
    disfluency_pattern = r'\b(?:uh+h*|um+m*|err*|you\s+know|well|so|i\s+mean|basically|actually|kind\s+of|sort\s+of|anyway|right|okay)\b'
    
    # Count disfluencies
    disfluencies = re.findall(disfluency_pattern, sentence.lower())
    disfluency_count = len(disfluencies)
    
    # Calculate disfluency rate
    word_count = len(re.findall(r'\w+', sentence))
    disfluency_rate = (disfluency_count / word_count)  if word_count != 0 else 0
    
    return disfluency_rate


# Function to calculate speech rate
def calculate_speech_rate(transcript, file_name, prev_speech_rate=None):
    
    speech_duration = None
    #to find duration 
    

    with wave.open(file_name) as mywav:
        speech_duration = mywav.getnframes() // mywav.getframerate()
        print(f"Length of the WAV file: {speech_duration:.1f} s")
    
    # Count words
    word_count = len(re.findall(r'\w+', transcript))
    # Calculate speech rate
    speech_rate = word_count / speech_duration
    # Check consistency with previous speech rate
    if prev_speech_rate is not None and prev_speech_rate !=0 :
        consistency_score = 1 - abs(speech_rate - prev_speech_rate) / prev_speech_rate
    else:
        consistency_score = 1  # If no previous speech rate available or 0 , consider it consistent
    return speech_rate, consistency_score

# # Load audio file
# audio_file = "concat_output.wav"
# audio = wave.open(audio_file, 'rb')

# # Read audio data
# audio_data = np.frombuffer(audio.readframes(-1), dtype=np.int16)

# # Close audio file
# audio.close()

# Example sentence for filler words and speech rate calculation
# sentence = "Um, like, I uh think that,actually, err um, we should, you know, uh, do something."

# # Calculate disfluency rate
# disfluency_rate = calculate_disfluency_rate(sentence)
# print("Disfluency Rate:", disfluency_rate)

# # Calculate speech rate (assuming speech duration is known)
# speech_duration = 30  # Example speech duration in seconds
# speech_rate, consistency_score = calculate_speech_rate(sentence, speech_duration)
# print("Speech Rate:", speech_rate)
# print("Consistency Score:", consistency_score)


