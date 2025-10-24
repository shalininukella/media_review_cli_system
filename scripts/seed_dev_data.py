from pathlib import Path
import sys
from app.cli.user_commands import add_user
from app.cli.media_commands import add_media

# Add root to path so we can import app modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

def seed_dev_data():
    print("Seeding development data...")

    # Users
    users = ["Alice", "Bob", "Charlie"]
    for u in users:
        add_user(u)

    # Media
    media_list = [
        ("Inception", "movie"),
        ("Stranger Things", "show"),
        ("Shape of You", "song"),
    ]
    for title, media_type in media_list:
        add_media(title, media_type)

    print("Development data seeded.")


if __name__ == "__main__":
    seed_dev_data()
