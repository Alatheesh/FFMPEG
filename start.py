import logging
import os
import sys

from bot import load_handlers
from bot.client import app
from config import DOWNLOAD_DIR, OUTPUT_DIR

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


# ==================================================
# Directories
# ==================================================

def create_directories():

    for folder in (
        DOWNLOAD_DIR,
        OUTPUT_DIR,
        "logs",
    ):

        os.makedirs(
            folder,
            exist_ok=True
        )


# ==================================================
# Startup
# ==================================================

def startup():

    logger.info(
        "=" * 60
    )

    logger.info(
        "Starting Telegram Media Editor..."
    )

    create_directories()

    logger.info(
        "Directories checked."
    )

    load_handlers()

    logger.info(
        "Handlers loaded."
    )

    logger.info(
        "Bot started successfully."
    )

    logger.info(
        "=" * 60
    )


# ==================================================
# Main
# ==================================================

def main():

    try:

        startup()

        app.run()

    except KeyboardInterrupt:

        logger.info(
            "Bot stopped by user."
        )

    except Exception:

        logger.exception(
            "Fatal startup error:"
        )

        sys.exit(1)


if __name__ == "__main__":

    main()
