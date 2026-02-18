import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import tempfile
import subprocess
import json

app = Flask(__name__)

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'm4a', 'ogg', 'flac', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transcribe_with_whisper_cpp(audio_path):
    """Use whisper.cpp for transcription - lightweight and fast"""
    
    # Convert to WAV 16kHz if needed
    wav_path = audio_path
    if not audio_path.endswith('.wav'):
        wav_path = '/tmp/audio_converted.wav'
        try:
            # Use ffmpeg to convert
            subprocess.run([
                'ffmpeg', '-i', audio_path, 
                '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le',
                wav_path, '-y'
            ], capture_output=True, check=True, timeout=30)
        except Exception as e:
            # If conversion fails, try with original file
            wav_path = audio_path
    
    # Run whisper.cpp
    model_path = '/app/whisper.cpp/models/ggml-tiny.en.bin'
    whisper_bin = '/app/whisper.cpp/main'
    
    try:
        result = subprocess.run([
            whisper_bin,
            '-m', model_path,
            '-f', wav_path,
            '-nt',  # No timestamps
            '-l', 'auto',  # Auto detect language
            '-ojf',  # Output JSON full
        ], capture_output=True, text=True, timeout=120, check=True)
        
        # Parse output - whisper.cpp outputs to stdout
        output = result.stdout.strip()
        
        # Try to find JSON output
        json_file = wav_path + '.json'
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                transcription = data.get('transcription', [])
                if transcription:
                    text = ' '.join([t.get('text', '') for t in transcription])
                    return text.strip(), 'auto'
        
        # Fallback: parse from stdout
        lines = output.split('\n')
        text_lines = [line for line in lines if line.strip() and not line.startswith('[')]
        transcription = ' '.join(text_lines)
        
        return transcription.strip(), 'auto'
        
    except subprocess.TimeoutExpired:
        raise Exception("Transcription timeout - file too large")
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

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
        transcription, language = transcribe_with_whisper_cpp(temp_path)
        
        # Clean up temp files
        try:
            os.unlink(temp_path)
            if os.path.exists('/tmp/audio_converted.wav'):
                os.unlink('/tmp/audio_converted.wav')
            if os.path.exists('/tmp/audio_converted.wav.json'):
                os.unlink('/tmp/audio_converted.wav.json')
        except:
            pass
        
        return jsonify({
            'success': True,
            'transcription': transcription,
            'language': language
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
