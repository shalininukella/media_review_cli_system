from pathlib import Path
import sys

# Add root folder to path so we can import root.db
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db import init_db

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", Path("data/media_review.db").resolve())
    print("No seed data added. Use CLI commands to add users or media.")