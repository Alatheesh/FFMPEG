import os
import logging

from config import DOWNLOAD_DIR, OUTPUT_DIR

# ---------------- Logging ---------------- #

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

# ------------- Create Folders ------------ #

def create_directories():
    folders = [
        DOWNLOAD_DIR,
        OUTPUT_DIR,
        "logs",
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

# ---------------- Main ------------------- #

def main():
    logger.info("========================================")
    logger.info(" Telegram Media Editor Bot")
    logger.info(" Initializing...")
    logger.info("========================================")

    create_directories()

    logger.info("✓ Required folders created.")
    logger.info("✓ Configuration loaded.")
    logger.info("✓ Ready for bot initialization.")

if __name__ == "__main__":
    main()
