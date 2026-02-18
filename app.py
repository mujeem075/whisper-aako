import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import tempfile
import subprocess
import requests

app = Flask(__name__)

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'm4a', 'ogg', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transcribe_with_api(audio_path):
    """Use OpenAI Whisper API for transcription"""
    # This is a fallback - you can use OpenAI API or Groq API (free tier available)
    # For now, using a simple approach with AssemblyAI free tier
    
    # Convert audio to wav if needed
    wav_path = audio_path
    if not audio_path.endswith('.wav'):
        wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
        subprocess.run(['ffmpeg', '-i', audio_path, '-ar', '16000', '-ac', '1', wav_path], 
                      capture_output=True)
    
    # Read audio file
    with open(wav_path, 'rb') as f:
        audio_data = f.read()
    
    # Use Groq API (free and fast) - you'll need to add API key
    # For demo, returning a placeholder
    # In production, add: GROQ_API_KEY in Heroku config vars
    
    api_key = os.environ.get('GROQ_API_KEY', '')
    
    if api_key:
        # Use Groq Whisper API
        headers = {'Authorization': f'Bearer {api_key}'}
        files = {'file': ('audio.wav', audio_data, 'audio/wav')}
        data = {'model': 'whisper-large-v3'}
        
        response = requests.post(
            'https://api.groq.com/openai/v1/audio/transcriptions',
            headers=headers,
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('text', ''), result.get('language', 'unknown')
    
    # Fallback: Use Vosk for offline transcription
    return transcribe_with_vosk(wav_path)

def transcribe_with_vosk(audio_path):
    """Offline transcription using Vosk"""
    from vosk import Model, KaldiRecognizer
    import wave
    import json
    
    # Download model on first use
    model_path = "/tmp/vosk-model"
    if not os.path.exists(model_path):
        model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        import zipfile
        import urllib.request
        
        zip_path = "/tmp/model.zip"
        urllib.request.urlretrieve(model_url, zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("/tmp/")
        
        os.rename("/tmp/vosk-model-small-en-us-0.15", model_path)
    
    model = Model(model_path)
    
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    
    transcription = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcription.append(result.get('text', ''))
    
    final_result = json.loads(rec.FinalResult())
    transcription.append(final_result.get('text', ''))
    
    return ' '.join(transcription), 'en'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: mp3, wav, mp4, m4a, ogg, flac'}), 400
    
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        # Transcribe audio
        transcription, language = transcribe_with_api(temp_path)
        
        # Clean up temp file
        try:
            os.unlink(temp_path)
            wav_path = temp_path.rsplit('.', 1)[0] + '.wav'
            if os.path.exists(wav_path):
                os.unlink(wav_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'transcription': transcription.strip(),
            'language': language
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
