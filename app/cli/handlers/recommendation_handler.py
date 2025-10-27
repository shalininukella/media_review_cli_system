import logging
from app.cli.commands.recommendation_commands import get_top_rated_command, recommend_media_command

logger = logging.getLogger(__name__)

def handle(args):
    if args.top_rated:
        result = get_top_rated_command()
        if not result.get("success"):
            logger.info(result["message"])
        else:
            for title, avg in result["data"]:
                logger.info(f" - {title}: {avg:.1f}")

    elif args.recommend:
        result = recommend_media_command(args.recommend)
        if not result.get("success"):
            logger.info(result["message"])
        else:
            logger.info(f"Recommendations for {result['user_name']}:")
            if result["data"]:
                for title, avg in result["data"]:
                    logger.info(f" - {title} (avg rating: {avg:.1f})")
            else:
                logger.info("No recommendations available.")