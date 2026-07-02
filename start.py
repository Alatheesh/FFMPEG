import os
import logging

from bot import load_handlers
from bot.client import app
from config import DOWNLOAD_DIR, OUTPUT_DIR

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def create_directories():
    for folder in [
        DOWNLOAD_DIR,
        OUTPUT_DIR,
        "logs",
    ]:
        os.makedirs(folder, exist_ok=True)


def main():

    logger.info("Starting Telegram Media Editor...")

    create_directories()

    load_handlers()

    logger.info("Handlers loaded.")

    app.run()


if __name__ == "__main__":
    main()
