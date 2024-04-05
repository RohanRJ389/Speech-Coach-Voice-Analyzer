# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "021075eedad54bf08bd8b600a2fee888"
transcriber = aai.Transcriber()

# transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")

# will wait for 2-5 seconds at max for getting text
def speech2Text(speechFile):
    transcript = transcriber.transcribe("./"+speechFile)
    print ( transcript.text)
    return (transcript.text)