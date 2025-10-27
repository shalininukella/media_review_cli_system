import argparse
import logging
from app.logging_config import setup_logging
from app.cli.handlers import (
    media_handler,
    review_handler,
    favourites_handler,
    user_handler,
    recommendation_handler,
    concurrency_handler,
)

logger = logging.getLogger(__name__)

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Media Review CLI")

    # define args
    # User commands
    parser.add_argument("--add-user", metavar="NAME")
    parser.add_argument("--list-users", action="store_true")

    # Media commands
    parser.add_argument("--list", action="store_true", help="List all media")
    parser.add_argument("--add-media", nargs=2, metavar=("TITLE", "MEDIA_TYPE"), help="Add new media")
    parser.add_argument("--search", metavar="TITLE", help="Search media by title")

    # Review commands 
    parser.add_argument("--review", nargs=3, metavar=("MEDIA_ID", "RATING", "COMMENT"), help="Add a review")
    parser.add_argument("--show-reviews", action="store_true", help="Show all reviews")
    
    # Favourite commands
    parser.add_argument("--favourite", nargs=2, metavar=("MEDIA_ID", "USER_ID"))
    parser.add_argument("--unfavourite", nargs=2, metavar=("MEDIA_ID", "USER_ID"))
    parser.add_argument("--show-favourites", metavar="USER_ID")

    # Recommendation commands
    parser.add_argument("--top-rated", action="store_true")
    parser.add_argument("--recommend", metavar="USER_ID", type=int)

    # Concurrency commands
    parser.add_argument("--concurrent", nargs="+", metavar="REVIEW")

    args = parser.parse_args()

    try:
        if args.list or args.add_media or args.search:
            media_handler.handle(args)
        elif args.review or args.show_reviews:
            review_handler.handle(args)
        elif args.favourite or args.unfavourite or args.show_favourites:
            favourites_handler.handle(args)
        elif args.top_rated or args.recommend:
            recommendation_handler.handle(args)
        elif args.add_user or args.list_users:
            user_handler.handle(args)
        elif args.concurrent:
            concurrency_handler.handle(args)
        else:
            parser.print_help()
    except Exception as e:
        logger.exception(f"Error executing command: {e}")

if __name__ == "__main__":
    main()
