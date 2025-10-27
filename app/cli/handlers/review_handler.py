import logging
from app.cli.commands.review_commands import add_review_command, list_reviews_command

logger = logging.getLogger(__name__)

def handle(args):
    if args.review:
        media_id, rating, comment = args.review
        try:
            user_id = int(input("Enter the user ID: "))
        except ValueError:
            logger.warning("Invalid user ID.")
            return
        result = add_review_command(user_id, int(media_id), float(rating), comment)
        logger.info(result["message"])

    elif args.show_reviews:
        result = list_reviews_command()
        if not result.get("success", True):
            logger.info(result.get("message"))
        else:
            reviews = result.get("data", [])
            if not reviews:
                logger.info("No reviews yet.")
            else:
                for r in reviews:
                    logger.info(f"[{r['id']}] User {r['user_id']} ({r['media_title']}), "
                                f"Rating: {r['rating']}, Comment: {r['comment']}")
