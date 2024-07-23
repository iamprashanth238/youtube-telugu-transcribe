from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import time
import tempfile
import shutil
import whisper

app = Flask(__name__)
CORS(app)

def download_youtube_video(video_url):
    temp_dir = tempfile.mkdtemp()
    temp_audio_path = os.path.join(temp_dir, 'temp_audio.%(ext)s')
    
    # Specify the audio format and post-process to convert to WAV
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

@app.route('/')
def index():
    return 'Welcome to the transcribe service'

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    video_url = request.json.get('url')
    print(f"Received URL: {video_url}")  # Debug print
    audio_path, temp_dir = download_youtube_video(video_url)
    
    print(f"Audio path: {audio_path}")  # Debug print

    # Load the Whisper model
    model = whisper.load_model("base")
    
    # Transcribe audio to Telugu text
    transcription_result = model.transcribe(audio_path, language="en")
    transcription_text = transcription_result.get("text", "")

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)
    
    # Return the transcription result
    return jsonify({'transcription': transcription_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
