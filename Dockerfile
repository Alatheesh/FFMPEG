FROM python:3.10-slim

# Install system dependencies and FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for local temp storage
RUN mkdir -p /app/temp/downloads /app/temp/outputs && chmod -R 777 /app/temp

# Run the Telegram client application
CMD ["python", "main.py"]
