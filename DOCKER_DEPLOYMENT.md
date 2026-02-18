# Docker Deployment Guide - Heroku

Yeh method use karke tum **unlimited transcriptions** kar sakte ho without API limits!

## Features
- ✅ Self-hosted Whisper model (no API needed)
- ✅ Unlimited transcriptions
- ✅ Fast processing with whisper.cpp
- ✅ No external dependencies
- ✅ Works on Heroku Standard-2x dyno

## Deployment Steps

### 1. Heroku Dashboard se Deploy

1. **Heroku Dashboard** open karo: https://dashboard.heroku.com/
2. **New** → **Create new app** click karo
3. App name do aur create karo

### 2. GitHub se Connect karo

1. App dashboard mein **Deploy** tab par jao
2. **Deployment method** mein **GitHub** select karo
3. Apna repository search karke connect karo
4. **Enable Automatic Deploys** (optional)

### 3. Stack Set karo (IMPORTANT!)

Heroku dashboard mein:
1. **Settings** tab par jao
2. **Add buildpack** section mein kuch mat karo (Docker use kar rahe hain)
3. Terminal se (agar access hai):
   ```bash
   heroku stack:set container -a your-app-name
   ```

Ya manually:
1. Settings → App Information
2. Stack: **container** hona chahiye

### 4. Deploy karo

**Option A: GitHub se (Recommended)**
1. Code ko GitHub par push karo:
   ```bash
   git add .
   git commit -m "Docker deployment with whisper.cpp"
   git push origin main
   ```
2. Heroku dashboard → Deploy tab → **Deploy Branch** click karo

**Option B: Heroku CLI se**
```bash
heroku login
heroku git:remote -a your-app-name
git push heroku main
```

### 5. Dyno Type Set karo

1. **Resources** tab par jao
2. **Change Dyno Type** click karo
3. **Standard-2X** select karo ($50/month)
   - 1GB RAM (model ke liye zaruri)
   - No sleep
   - Better performance

### 6. Test karo

App URL open karo: `https://your-app-name.herokuapp.com`

## Important Notes

### First Request
- Pehli baar 2-3 minutes lag sakte hain (model load ho raha hai)
- Uske baad fast rahega

### Model Size
- Tiny.en model use kar rahe hain (~75MB)
- English ke liye optimized
- Agar multilingual chahiye toh Dockerfile mein `tiny.en` ko `tiny` se replace karo

### Better Accuracy ke liye
Dockerfile mein model change karo:
```dockerfile
# Tiny model (current) - Fast, 70-75% accuracy
bash ./models/download-ggml-model.sh tiny.en

# Base model - Better accuracy, slower
bash ./models/download-ggml-model.sh base.en

# Small model - Best balance
bash ./models/download-ggml-model.sh small.en
```

### Cost
- **Free Dyno:** Works but sleeps after 30 min, limited hours
- **Standard-2X:** $50/month, 1GB RAM, no sleep (Recommended)
- **Performance-M:** $250/month, 2.5GB RAM (for larger models)

## Troubleshooting

### Build timeout?
- Heroku free tier mein build time limit hai
- Standard-2X dyno use karo

### Out of memory?
- Standard-2X dyno use karo (1GB RAM)
- Ya tiny model use karo (already using)

### Slow transcription?
- Standard-2X dyno upgrade karo
- Workers increase karo Dockerfile mein: `--workers 4`

## Logs Check karna

Dashboard se:
1. **More** → **View logs**

Ya CLI se:
```bash
heroku logs --tail -a your-app-name
```

---

Yeh solution **completely self-hosted** hai - no API limits, unlimited transcriptions! 🚀
