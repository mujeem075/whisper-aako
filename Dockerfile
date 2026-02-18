FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install whisper.cpp
RUN git clone https://github.com/ggerganov/whisper.cpp.git && \
    cd whisper.cpp && \
    make && \
    bash ./models/download-ggml-model.sh tiny.en

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300 --workers 2
