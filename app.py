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
#model = pipeline("automatic-speech-recognition", model="openai/whisper-base")
#model.model.config.forced_decoder_ids = model.tokenizer.get_decoder_prompt_ids(language="te", task="transcribe")

# Getting request and return response
@app.route("/transcribe", methods=["GET"])
def transcribe():
    video_url = request.args.get('url')  # Use args to get query parameter
    if not video_url:
        return jsonify({"error": "URL parameter is missing"}), 400
    
    print(f"Received URL: {video_url}")
    audio_path, temp_dir = download_youtube_video(video_url)

    # transcribe the audio
    try:
        model_id = "openai/whisper-large-v3"
        # torch for cpu inference
        model = pipeline("automatic-speech-recognition", model=model_id)
        model.model.config.forced_decoder_ids = model.tokenizer.get_decoder_prompt_ids(language="te", task="transcribe")
        transcription = model(audio_path)['text']
        shutil.rmtree(temp_dir)
        return jsonify({"transcription": transcription}), 200

    except Exception as e:
        print(f"Error: {e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return jsonify({"error": str(e)}), 500

def download_youtube_video(video_url):
    temp_dir = tempfile.mkdtemp()
    temp_audio_path = os.path.join(temp_dir, 'temp_audio.%(ext)s')
    
    # Specifying the audio format and Post-processing to convert to WAV
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': temp_audio_path,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    temp_audio_path_wav = temp_audio_path.replace('%(ext)s', 'wav')
    while not os.path.exists(temp_audio_path_wav):
        time.sleep(0.1)
    
    return temp_audio_path_wav, temp_dir

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5000, debug=True)
