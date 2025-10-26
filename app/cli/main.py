
import argparse
import logging
from app.logging_config import setup_logging

# CLI command wrappers (interact with services, not DB directly)
from app.cli.media_commands import (
    list_media_command,
    add_media_command,
    search_by_title_command,
)
from app.cli.review_commands import (
    add_review_command,
    list_reviews_command,
)
from app.cli.favourite_commands import (
    add_favourite_command,
    remove_favourite_command,
    show_favourites_command,
)
from app.cli.concurrency import concurrent_reviews_command
from app.cli.recommendation_commands import (
    get_top_rated_command,
    recommend_media_command,
)
from app.cli.user_commands import add_user, list_users

logger = logging.getLogger(__name__)


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="🎬 Media Review CLI")
    parser.add_argument("--list", action="store_true", help="List all media")
    parser.add_argument(
        "--review",
        nargs=3,
        metavar=("MEDIA_ID", "RATING", "COMMENT"),
        help="Add a review",
    )
    parser.add_argument("--show-reviews", action="store_true", help="Show all reviews")
    parser.add_argument("--search", metavar="TITLE", help="Search media by title")
    parser.add_argument(
        "--add-media", nargs=2, metavar=("TITLE", "MEDIA_TYPE"), help="Add new media"
    )
    parser.add_argument(
        "--favourite",
        nargs=2,
        metavar=("MEDIA_ID", "USER_ID"),
        help="Favourite a media",
    )
    parser.add_argument(
        "--unfavourite",
        nargs=2,
        metavar=("MEDIA_ID", "USER_ID"),
        help="Remove from favourites",
    )
    parser.add_argument(
        "--show-favourites", metavar="USER_ID", help="Show user’s favourite media"
    )
    parser.add_argument(
        "--concurrent",
        nargs="+",
        metavar="REVIEW",
        help="Submit multiple reviews concurrently. Format: USER_ID MEDIA_ID RATING COMMENT ...",
    )
    parser.add_argument("--top-rated", action="store_true", help="Show top-rated media")
    parser.add_argument(
        "--recommend", metavar="USER_ID", type=int, help="Recommend media for a user"
    )
    parser.add_argument("--add-user", metavar="NAME", help="Add a new user")
    parser.add_argument("--list-users", action="store_true", help="List all users")

    args = parser.parse_args()

    try:
        if args.list:
            list_media_command()
        elif args.review:
            media_id, rating, comment = args.review
            add_review_command(int(media_id), float(rating), comment)
        elif args.show_reviews:
            list_reviews_command()
        elif args.search:
            search_by_title_command(args.search)
        elif args.add_media:
            title, media_type = args.add_media
            add_media_command(title, media_type)
        elif args.favourite:
            media_id, user_id = args.favourite
            add_favourite_command(int(media_id), int(user_id))
        elif args.unfavourite:
            media_id, user_id = args.unfavourite
            remove_favourite_command(int(media_id), int(user_id))
        elif args.show_favourites:
            show_favourites_command(int(args.show_favourites))
        elif args.concurrent:
            concurrent_reviews_command(args.concurrent)
        elif args.top_rated:
            get_top_rated_command()
        elif args.recommend:
            recommend_media_command(args.recommend)
        elif args.add_user:
            add_user(args.add_user)
        elif args.list_users:
            list_users()
        else:
            parser.print_help()
    except Exception as e:
        logger.exception(f"Error executing command: {e}")
        print(f"Something went wrong: {e}")


if __name__ == "__main__":
    main()
