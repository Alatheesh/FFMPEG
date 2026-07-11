import logging
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
from engine.models import Workspace
logger = logging.getLogger(__name__)
db_client = None
db = None
workspaces_col = None
# In-memory database fallback to support local runs or environments without Mongo setup
memory_db = {}
async def init_db():
    global db_client, db, workspaces_col
    if not Config.MONGO_URI:
        logger.warning("MONGO_URI not set! Operating in MEMORY-ONLY mode. Workspace sessions will reset on restart.")
        return True
    try:
        db_client = AsyncIOMotorClient(Config.MONGO_URI, serverSelectionTimeoutMS=3000)
        db = db_client[Config.DATABASE_NAME]
        workspaces_col = db["workspaces"]
        # Try pinging database to test connection immediately
        await db_client.admin.command('ping')
        logger.info("MongoDB connection verified successfully for workspace sessions.")
        return True
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}. Falling back to in-memory mode.")
        return False
async def get_workspace(user_id: int) -> Workspace:
    user_key = str(user_id)
    if workspaces_col is not None:
        try:
            doc = await workspaces_col.find_one({"user_id": user_key})
            if doc:
                return Workspace.from_dict(user_id, doc)
        except Exception as e:
            logger.error(f"Error loading workspace from DB for user {user_id}: {e}")
            
    # Fallback to memory
    if user_key not in memory_db:
        memory_db[user_key] = Workspace(user_id)
    return memory_db[user_key]
async def save_workspace(workspace: Workspace):
    user_key = str(workspace.user_id)
    # Always update in-memory DB copy
    memory_db[user_key] = workspace
    
    if workspaces_col is not None:
        try:
            await workspaces_col.replace_one(
                {"user_id": user_key},
                workspace.to_dict(),
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error saving workspace to DB for user {workspace.user_id}: {e}")
            return False
    return True
async def delete_workspace(user_id: int):
    user_key = str(user_id)
    if user_key in memory_db:
        del memory_db[user_key]
        
    if workspaces_col is not None:
        try:
            await workspaces_col.delete_one({"user_id": user_key})
            return True
        except Exception as e:
            logger.error(f"Error deleting workspace from DB for user {user_id}: {e}")
            return False
    return True
