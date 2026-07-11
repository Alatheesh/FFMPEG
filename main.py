import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pyrogram import Client
from config import Config
from database import init_db
import uvicorn
import aiohttp

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
        
    # Delete webhook via Telegram Bot API directly using aiohttp to clear any active webhooks
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{Config.BOT_TOKEN}/deleteWebhook?drop_pending_updates=true"
            async with session.get(url) as response:
                resp_text = await response.text()
                logger.info(f"Telegram Webhook Delete Response: {resp_text}")
    except Exception as e:
        logger.warning(f"Failed to delete webhook via HTTP request: {e}")

    logger.info("Starting Pyrogram bot client...")
    try:
        await bot.start()
    except Exception as e:
        err_str = str(e)
        if "AuthKeyInvalid" in err_str or "401" in err_str or "Unauthorized" in err_str:
            logger.warning("Session file invalid or token revoked. Deleting session file and retrying...")
            import os
            session_file = "media_editor_bot.session"
            if os.path.exists(session_file):
                os.remove(session_file)
            await bot.start()
        else:
            raise e
        
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
