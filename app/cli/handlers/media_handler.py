import logging
from app.cli.commands.media_commands import list_media_command, add_media_command, search_by_title_command

logger = logging.getLogger(__name__)

def handle(args):
    if args.list:
        result = list_media_command()
        if not result.get("data"):
            logger.info(result.get("message", "No media found."))
        else:
            for m in result["data"]:
                logger.info(f"[{m['id']}] {m['title']} ({m['type']})")

    elif args.add_media:
        title, media_type = args.add_media
        result = add_media_command(title, media_type)
        logger.info(result["message"])

    elif args.search:
        result = search_by_title_command(args.search)
        if not result.get("success", True):
            logger.info(result.get("message", "Something went wrong."))
        else:
            source = "(from cache)" if result.get("cached") else ""
            logger.info(f"{source} {result['title']} ({result.get('type', '')})")
            if result.get("reviews"):
                for r in result["reviews"]:
                    logger.info(f"  {r['rating']} — {r['comment']}")
            else:
                logger.info("No reviews yet.")
