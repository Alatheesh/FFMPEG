import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pyrogram import Client
from config import Config
from database import init_db
import uvicorn

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Validate credentials
if not Config.API_ID or not Config.API_HASH or not Config.BOT_TOKEN:
    logger.warning("Telegram keys (API_ID, API_HASH, BOT_TOKEN) are missing from env!")

# Initialize Pyrogram Bot Client
bot = Client(
    "media_editor_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing database connection...")
    db_success = await init_db()
    if not db_success:
        logger.error("Failed to connect database, starting in fallback memory-only mode.")
        
    logger.info("Starting Pyrogram bot client...")
    await bot.start()
    try:
        bot_info = await bot.get_me()
        logger.info(f"Bot @{bot_info.username} started successfully.")
    except Exception as e:
        logger.error(f"Error fetching bot info: {e}")
        
    yield
    
    # Shutdown actions
    logger.info("Stopping Pyrogram bot client...")
    await bot.stop()
    logger.info("Application shutdown complete.")

# Initialize FastAPI Keep-alive App
app = FastAPI(
    title="Auto Media Editor Dashboard",
    description="Active Keep-alive web-service endpoint for Hugging Face Spaces",
    lifespan=lifespan
)

@app.get("/")
async def root():
    from database import workspaces_col, memory_db
    try:
        if workspaces_col is not None:
            total_db_sessions = await workspaces_col.count_documents({})
        else:
            total_db_sessions = len(memory_db)
    except Exception:
        total_db_sessions = "Error"
        
    return {
        "status": "online",
        "app": "Auto Media Editor Backend Service",
        "database_mode": "MongoDB" if Config.MONGO_URI else "In-Memory Fallback",
        "active_workspaces": total_db_sessions,
        "backblaze_b2": "Enabled" if Config.B2_ENABLED else "Disabled"
    }

if __name__ == "__main__":
    logger.info(f"Launching webserver and bot on port {Config.PORT}...")
    uvicorn.run("main:app", host="0.0.0.0", port=Config.PORT, reload=False)
