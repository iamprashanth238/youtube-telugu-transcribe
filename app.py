import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp as youtube_dl
import torch
from transformers import pipeline
import tempfile
import shutil
import time

app = Flask(__name__)
CORS(app)

# Load model and processor
model = pipeline("automatic-speech-recognition", model="kattojuprashanth238/whisper-small-te-v3")
model.model.config.forced_decoder_ids = model.tokenizer.get_decoder_prompt_ids(language="te", task="transcribe")

# Getting request and return response
@app.route("/transcribe", methods=["GET"])
def transcribe():
    video_url = request.args.get('url')  # Use args to get query parameter
    if not video_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        # Download video
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, 'audio.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            audio_file = os.path.join(temp_dir, 'audio.mp3')

            # Transcribe audio
            result = model(audio_file)

            # Return transcription
            return jsonify({"transcription": result['text']})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)