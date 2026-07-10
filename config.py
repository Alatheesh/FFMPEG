import os

class Config:
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    MONGO_URI = os.environ.get("MONGO_URI", "")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "AutoMediaEditor")
    
    # Port for Hugging Face keep-alive webserver
    PORT = int(os.environ.get("PORT", "7860"))
    
    # Backblaze B2 Storage Settings
    B2_KEY_ID = os.environ.get("B2_KEY_ID", "")
    B2_APPLICATION_KEY = os.environ.get("B2_APPLICATION_KEY", "")
    B2_BUCKET_NAME = os.environ.get("B2_BUCKET_NAME", "")
    B2_ENABLED = bool(B2_KEY_ID and B2_APPLICATION_KEY and B2_BUCKET_NAME)

    # Local Temp Directories
    TEMP_DIR = os.path.join(os.getcwd(), "temp")
    DOWNLOADS_DIR = os.path.join(TEMP_DIR, "downloads")
    OUTPUTS_DIR = os.path.join(TEMP_DIR, "outputs")
    
    # Make sure temp directories exist
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
