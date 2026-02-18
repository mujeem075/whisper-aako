# Audio Transcription API

Heroku par deployed audio transcription service using OpenAI Whisper model.

## Setup Instructions

### 1. Heroku Setup
```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Set dyno type to Standard-2x
heroku ps:type web=Standard-2X

# Optional: Add Groq API key for better accuracy (free tier available)
heroku config:set GROQ_API_KEY=your_groq_api_key

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### 2. Get Free Groq API Key (Recommended)
1. Visit: https://console.groq.com/
2. Sign up for free account
3. Get API key from dashboard
4. Add to Heroku: `heroku config:set GROQ_API_KEY=your_key`

Without API key, it will use Vosk (offline, less accurate but free).

### 2. API Usage

**Endpoint:** `POST /transcribe`

**Example using curl:**
```bash
curl -X POST -F "audio=@your-audio-file.mp3" https://your-app-name.herokuapp.com/transcribe
```

**Example using Python:**
```python
import requests

url = "https://your-app-name.herokuapp.com/transcribe"
files = {'audio': open('audio.mp3', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

**Response:**
```json
{
  "success": true,
  "transcription": "Your transcribed text here",
  "language": "en"
}
```

## Supported Audio Formats
- MP3
- WAV
- MP4
- M4A
- OGG
- FLAC

## Notes
- Standard-2x dyno recommended for better performance
- Timeout set to 300 seconds for large files
- Faster-Whisper tiny model used (4-5x faster than regular Whisper!)
- Model downloads on first request (takes ~20 seconds first time)
- For better accuracy, change "tiny" to "base" or "small" in app.py
- int8 quantization for faster CPU inference
