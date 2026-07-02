FROM python:3.11-slim

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install FFmpeg and MediaInfo
RUN apt-get update && apt-get install -y \
    ffmpeg \
    mediainfo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better Docker caching)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create required folders
RUN mkdir -p temp/downloads temp/outputs logs

# Start the bot
CMD ["python", "start.py"]
