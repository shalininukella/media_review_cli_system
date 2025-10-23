import argparse
from app.cli.media_commands import list_media, add_media, search_by_title
from app.cli.review_commands import add_reviews, list_reviews
from app.cli.favourite_commands import add_favourite, remove_favourite, show_favourites
from app.cli.concurrency import concurrent_reviews
from app.cli.recommendation_commands import get_top_rated, recommend_media

def main():
    parser = argparse.ArgumentParser(description="Media Review CLI")
    parser.add_argument("--list", action="store_true", help="List all media")
    parser.add_argument("--review", nargs=3, metavar=("MEDIA_ID", "RATING", "COMMENT"), help="Add a review")
    parser.add_argument("--show-reviews", action="store_true", help="Show all reviews")
    parser.add_argument("--search", metavar=("TITLE"), help="Search by title")
    parser.add_argument("--add-media", nargs=2, metavar=("TITLE", "MEDIA_TYPE"), help="Add new media with type")
    parser.add_argument("--favourite", nargs=2, metavar=("MEDIA_ID", "USER_ID"), help="Favourite a particular media")
    parser.add_argument("--unfavourite", nargs=2, metavar=("MEDIA_ID", "USER_ID"), help="Unfavourite a particular media")
    parser.add_argument("--show-favourites", metavar="USER_ID", help="Show all the favourite media of a user")
    parser.add_argument("--concurrent", action="store_true", help="Simulate concurrent review submissions")
    parser.add_argument("--top-rated", action="store_true", help="Show top-rated media")
    parser.add_argument("--recommend", type=int, help="Recommend media for a user")

    args = parser.parse_args()

    if args.list:
        list_media()
    elif args.review:
        media_id, rating, comment = args.review
        add_reviews(int(media_id), float(rating), comment)
    elif args.show_reviews:
        list_reviews()
    elif args.search:
        search_by_title(args.search)
    elif args.add_media:
        title, media_type = args.add_media
        add_media(title, media_type)
    elif args.favourite:
        media_id, user_id = args.favourite
        add_favourite(media_id, user_id)
    elif args.unfavourite:
        media_id, user_id = args.unfavourite
        remove_favourite(media_id, user_id)
    elif args.show_favourites:
        show_favourites(args.show_favourites)
    elif args.concurrent:
        concurrent_reviews()
    elif args.top_rated:
        get_top_rated()
    elif args.recommend:
        recommend_media(args.recommend)
    else:
        parser.print_help()
