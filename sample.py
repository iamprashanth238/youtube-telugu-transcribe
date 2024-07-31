import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp as youtube_dl
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import tempfile
import shutil
import time

app = Flask(__name__)
CORS(app)

# Load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
model.config.forced_decoder_ids = None

#Getting request and return response
@app.get("/transcribe")
def transcribe():
    video_url = request.json['url']
    print(f"Received URL: {video_url}")
    audio_path, temp_dir = download_youtube_video(video_url)

    # Process the audio
    try:
        import soundfile as sf
        audio_input, sample_rate = sf.read(audio_path)
        input_features = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_features

        # Generate token ids
        predicted_ids = model.generate(input_features)
        # Decode token ids to text
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        return jsonify({"transcription": transcription}), 200
    
    except Exception as e:
        print(f"Error: {e}")
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
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    temp_audio_path_wav = temp_audio_path.replace('%(ext)s', 'wav')
    while not os.path.exists(temp_audio_path_wav):
        time.sleep(0.1)
    
    return temp_audio_path_wav, temp_dir