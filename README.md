# Audio Transcription API 🎙️

Heroku par deployed audio transcription service using OpenAI Whisper model.

**Features:**
- 🌐 Web Interface - Browser mein audio upload karke test karo
- 🔌 REST API - Programmatic access ke liye
- 🎯 Multiple Audio Formats Support
- ⚡ Fast & Accurate Transcription

---

## 📋 Heroku par Manual Deployment (Dashboard se)

### Step 1: GitHub par Code Upload karo

1. **GitHub account mein login karo**: https://github.com
2. **New Repository banao**:
   - Click on "+" (top right) → "New repository"
   - Repository name do (jaise: `audio-transcription-api`)
   - Public ya Private select karo
   - "Create repository" click karo

3. **Code upload karo**:
   - Apne computer par is project folder mein jao
   - GitHub par jo commands dikha rahe hain, wo copy karo:
   ```bash
   git init
   git add .
   git commit -m "Audio transcription API"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```
   - Ya phir GitHub Desktop use kar sakte ho (easier hai)

---

### Step 2: Heroku Account Setup

1. **Heroku account banao** (agar nahi hai): https://signup.heroku.com/
2. **Login karo**: https://dashboard.heroku.com/

---

### Step 3: Heroku App Create karo

1. **Dashboard par jao**: https://dashboard.heroku.com/apps
2. **"New" button click karo** (top right corner)
3. **"Create new app" select karo**
4. **App details bharo**:
   - App name: koi unique name do (jaise: `my-audio-transcription`)
   - Region: United States ya Europe (jo paas ho)
5. **"Create app" button click karo**

---

### Step 4: GitHub se Connect karo

1. **"Deploy" tab par jao** (app dashboard mein)
2. **Deployment method mein "GitHub" select karo**
3. **"Connect to GitHub" button click karo**
4. **Authorize karo** (agar pehli baar hai)
5. **Repository search karo**:
   - Apne repository ka naam type karo
   - "Search" click karo
   - Jab mil jaye, "Connect" click karo

---

### Step 5: Deploy karo

1. **Manual Deploy section mein jao** (neeche scroll karo)
2. **Branch select karo**: `main`
3. **"Deploy Branch" button click karo**
4. **Wait karo** - Build process 5-10 minutes le sakta hai
5. **"View" button click karo** jab deployment complete ho jaye

---

### Step 6: Standard-2X Dyno Enable karo (Optional but Recommended)

1. **"Resources" tab par jao**
2. **"Change Dyno Type" click karo**
3. **"Standard-2X" select karo** (₹3,500-4,000/month approx)
4. **"Save" click karo**

**Note:** Free dyno bhi kaam karega but slow hoga aur 30 min baad sleep mode mein chala jayega.

---

### Step 7: App Test karo

**Web Interface se:**
1. Browser mein app URL kholo: `https://your-app-name.herokuapp.com`
2. Audio file upload karo (drag-drop ya click karke)
3. "Transcribe Audio" button click karo
4. Result dekho!

**API se test karo (Postman ya curl):**
```bash
curl -X POST -F "audio=@your-audio.mp3" https://your-app-name.herokuapp.com/transcribe
```

---

## 🔧 API Usage

### Endpoint
```
POST /transcribe
```

### Request
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Audio file with key `audio`

### Example (Python)
```python
import requests

url = "https://your-app-name.herokuapp.com/transcribe"
files = {'audio': open('audio.mp3', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

### Example (JavaScript)
```javascript
const formData = new FormData();
formData.append('audio', audioFile);

fetch('https://your-app-name.herokuapp.com/transcribe', {
    method: 'POST',
    body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

### Response
```json
{
  "success": true,
  "transcription": "Your transcribed text here",
  "language": "en"
}
```

---

## 📁 Supported Audio Formats
- MP3
- WAV
- MP4
- M4A
- OGG
- FLAC

---

## ⚙️ Configuration

### Files Overview
- `app.py` - Main Flask application
- `templates/index.html` - Web interface
- `requirements.txt` - Python dependencies
- `Procfile` - Heroku configuration
- `runtime.txt` - Python version

### Whisper Model
Default: `base` model (good balance of speed & accuracy)

**Change karna hai toh** `app.py` mein line 13 edit karo:
```python
# Options: tiny, base, small, medium, large
model = whisper.load_model("base")
```

---

## 🐛 Troubleshooting

### Build fail ho raha hai?
1. Heroku dashboard → "Activity" tab → Build logs check karo
2. "More" → "View build log" click karo

### App slow hai ya crash ho raha hai?
1. "Resources" tab → Standard-2X dyno enable karo
2. Ya `app.py` mein model change karo: `whisper.load_model("tiny")`

### Logs kaise dekhe?
1. Dashboard → "More" → "View logs"
2. Real-time logs dikhenge

### App restart karna hai?
1. Dashboard → "More" → "Restart all dynos"

---

## 💰 Cost Estimate

| Dyno Type | RAM | Cost | Best For |
|-----------|-----|------|----------|
| Free | 512MB | Free | Testing only (sleeps after 30 min) |
| Hobby | 512MB | $7/month | Light usage |
| Standard-2X | 1GB | $50/month | Production use |

---

## 📝 Notes
- Timeout set to 300 seconds for large files
- 2 workers configured for better performance
- Automatic cleanup of temporary files
- Drag-and-drop support in web interface

---

## 🚀 Next Steps

1. Custom domain add kar sakte ho (Settings → Domains)
2. Environment variables add kar sakte ho (Settings → Config Vars)
3. Automatic deploys enable kar sakte ho (Deploy → Enable Automatic Deploys)
4. Database add kar sakte ho (agar transcription history save karni ho)

Koi problem ho toh GitHub issue create karo! 🎉
