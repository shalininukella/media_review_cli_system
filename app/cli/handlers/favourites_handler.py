import logging
from app.cli.commands.favourite_commands import (
    add_favourite_command,
    remove_favourite_command,
    show_favourites_command,
)

logger = logging.getLogger(__name__)

def handle(args):
    if args.favourite:
        media_id, user_id = map(int, args.favourite)
        result = add_favourite_command(media_id, user_id)
        logger.info(result["message"])

    elif args.unfavourite:
        media_id, user_id = map(int, args.unfavourite)
        result = remove_favourite_command(media_id, user_id)
        logger.info(result["message"])

    elif args.show_favourites:
        user_id = int(args.show_favourites)
        result = show_favourites_command(user_id)
        if not result.get("success"):
            logger.info(result.get("message", "Something went wrong."))
        elif not result["data"]:
            logger.info("You haven’t favourited any media yet.")
        else:
            for fav in result["data"]:
                logger.info(f"  - {fav['title']} (ID: {fav['media_id']})")
