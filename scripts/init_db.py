from pathlib import Path
import logging
from app.core.db import init_db

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    init_db()
    logger.info("Database initialized at: %s", Path("data/media_review.db").resolve())

if __name__ == "__main__":
    main()
