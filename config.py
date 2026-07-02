import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "")

# Backblaze B2 (Optional)
B2_KEY_ID = os.getenv("B2_KEY_ID", "")
B2_APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY", "")
B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME", "")

# Bot Settings
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Working Directories
DOWNLOAD_DIR = "temp/downloads"
OUTPUT_DIR = "temp/outputs"

# Maximum file size (GB)
MAX_FILE_SIZE = 20

# Progress update interval (seconds)
PROGRESS_UPDATE_TIME = 5

# FFmpeg
FFMPEG_BINARY = os.getenv("FFMPEG_BINARY", "ffmpeg")
FFPROBE_BINARY = os.getenv("FFPROBE_BINARY", "ffprobe")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Workspace
WORKSPACE_TIMEOUT = 3600

# Telegram
WORKERS = 20
SLEEP_THRESHOLD = 30
