import json
import wave
import numpy as np
from features import calculate_intensity, calculate_pitch_variation, calculate_disfluency_rate, calculate_speech_rate
from libraryS2T import speech2Text
#checking if this gets reflected
prev_speech_rate = None
complete_speech = ""

json_file_path = "frontend/src/metrics.json"
cumulative_json_file_path = "c_metrics.txt"

num =1

weights = {
    "intensity": 0.25,
    "pitch_variation": 0.25,
    "disfluency_rate": 0.3,
    "speech_rate": 0.2
}


def generate_tip(metric_name):
    """Generate a tip based on the specified metric."""
    tips = {
        "intensity": "Your voice seems a bit soft. Try projecting a bit more for better clarity.",
        "pitch_variation": "Consider varying your pitch a bit more to keep the audience engaged.",
        "disfluency_rate": "Try to reduce the number of filler words like 'um' and 'uh'.",
        "speech_rate": "You seem to be speaking a bit quickly. Slowing down slightly might improve your articulation."
    }
    return tips.get(metric_name, "I'm not sure what feedback to give at the moment.")



def one_iteration():
    global prev_speech_rate, complete_speech, num
    audio_file = f"captured_audio/concat_output{num}.wav"
    print(f"serial number {num}")
    num+=1
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
    complete_speech += text_transcript

    print("speech to text returned : " + text_transcript)

    # Calculate disfluency rate
    disfluency_rate = calculate_disfluency_rate(text_transcript)
    print("fluency Rate:", 1 - disfluency_rate)

    # Calculate speech rate (assuming speech duration is known)
    speech_rate, consistency_score = calculate_speech_rate(text_transcript, audio_file, prev_speech_rate)  # TODO EWMA

    prev_speech_rate = speech_rate

    print("Speech Rate:", speech_rate)
    print("Consistency Score:", consistency_score)

   # Calculate master score as weighted mean of metrics
    master_score = (weights["intensity"] * intensity +
                    weights["pitch_variation"] * pitch_variation +
                    weights["disfluency_rate"] * disfluency_rate +
                    weights["speech_rate"] * speech_rate)

    # Check for low master score and determine feedback
    threshold = 0.6  # Adjust the threshold as needed


    # metrics["tip"] = tip
    # File path to save the JSON file
    metrics = {
        "intensity": round(intensity,1),
        "pitch_variation": round(pitch_variation,1),
        "fluency_rate": 1 - round(disfluency_rate,1),
        "speech_rate": round(speech_rate,1),
        "consistency_score": round(consistency_score,1),
        "master_score": round(master_score,1),
        "complete_speech": complete_speech
    }
    if master_score < threshold:
        # Exclude 'complete_speech' from metrics for finding the lowest metric
        metrics_to_evaluate = {metric: value for metric, value in metrics.items() if metric != "master_score" and metric != "complete_speech"}
        if metrics_to_evaluate:
            # Find the lowest metric
            lowest_metric = min(metrics_to_evaluate, key=metrics_to_evaluate.get)
            # Generate tip based on the lowest metric
            tip = generate_tip(lowest_metric)
        else:
            # If there are no metrics to evaluate, provide a default tip
            tip = "Sounding good! Keep it up."
    else:
        # If the master score is above the threshold, provide positive feedback
        tip = "Sounding good! Keep it up."
    

    # tip = generate_tip(metrics)
    metrics["tip"] = tip

    # Write metrics to JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(metrics, json_file, indent=4)
    with open(cumulative_json_file_path, "a") as json_file:
        json.dump(metrics, json_file, indent=4)

    print(str.upper("one iteration of metric updation complete !"))


if __name__ == "__main__":
    with open(json_file_path, "w") as json_file:
        json_file.write("{}")
    with open(cumulative_json_file_path, "w") as json_file:
        json_file.write("{}")
    while True:
       one_iteration()