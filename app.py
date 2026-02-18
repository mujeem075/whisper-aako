import os
import whisper
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'm4a', 'ogg', 'flac'}

# Model will be loaded on first request (lazy loading)
model = None

def get_model():
    global model
    if model is None:
        # Using tiny model - smallest and fastest
        model = whisper.load_model("tiny")
    return model

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        
        # Get model (lazy load)
        whisper_model = get_model()
        
        # Transcribe audio
        result = whisper_model.transcribe(temp_path)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return jsonify({
            'success': True,
            'transcription': result['text'].strip(),
            'language': result.get('language', 'unknown')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
