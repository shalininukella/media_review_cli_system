import logging
from app.cli.commands.user_commands import add_user
from app.cli.commands.media_commands import add_media_command

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_dev_data():
    logger.info("Seeding development data...")

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
        add_media_command(title, media_type)

    logger.info("Development data seeded.")

def main():
    seed_dev_data()

if __name__ == "__main__":
    main()
