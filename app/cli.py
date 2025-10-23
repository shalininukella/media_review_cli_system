"""
To handle  commands like --list, --review, --search, and --show-reviews
"""

import argparse
from app.db import get_session
from app.models import Media, Reviews, User


def list_media():
    session = get_session()
    medias = session.query(Media).all()
    for m in medias:
        print(f"[{m.id}] {m.title} ({m.type})")


def search_by_title(title):
    session = get_session()
    media_row = session.query(Media).filter_by(title=title).first()

    if not media_row:
        print(f"No media found with title '{title}'")
        return

    print(f"{media_row.title}, ({media_row.type})")

    if media_row.reviews:
        for r in media_row.reviews:
            print(f"⭐ {r.rating} — {r.comment}")
    else:
        print("No reviews yet.")


def add_reviews(media_id, rating, comment):
    session = get_session()

    user_id = int(input("Enter the user Id: "))
    user = session.query(User).get(user_id) 
    if not user:
        print("No user found.")
        return

    reviews = Reviews(
        user_id=user_id, media_id=media_id, rating=rating, comment=comment
    )
    session.add(reviews)
    session.commit()
    print("Review added successfully!")


def list_reviews():
    session = get_session()
    reviews = session.query(Reviews).all()
    if not reviews:
        print("No reviews yet.")
        return

    for r in reviews:
        print(f"[{r.id}] {r.user.id} ({r.media.title}), {r.rating}, {r.comment}")


from app.media_factory import MediaFactory


def add_media(title, media_type):
    session = get_session()
    media_row = MediaFactory.create_media(title, media_type)
    session.add(media_row)
    session.commit()
    print(f"Added {media_type} '{title}' to database!")


def main():
    parser = argparse.ArgumentParser(description="Media Review CLI")
    parser.add_argument("--list", action="store_true", help="List all media")
    parser.add_argument(
        "--review",
        nargs=3,
        metavar=("MEDIA_ID", "RATING", "COMMENT"),
        help="Add a review",
    )
    parser.add_argument("--show-reviews", action="store_true", help="Show all reviews")
    parser.add_argument("--search", metavar=("TITLE"), help="Search by title")
    parser.add_argument(
        "--add-media",
        nargs=2,
        metavar=("TITLE", "MEDIA_TYPE"),
        help="Add new media with type",
    )

    args = (
        parser.parse_args()
    )  # Reads from the command line, validates input, and stores values in a namespace.

    # to access the arguments -> print(args.list or args.review etc)

    if args.list:
        list_media()
    elif args.review:
        media_id, rating, comment = args.review
        add_reviews(int(media_id), float(rating), comment)
    elif args.show_reviews:
        list_reviews()
    elif args.search:
        title = args.search
        search_by_title(title)
    elif args.add_media:
        title, media_type = args.add_media
        add_media(title, media_type)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


# python app/media_review.py --list
# [1] Inception (movie)
# [2] Stranger Things (webshow)
# [3] Shape of You (song)

# python media_review.py --review 2 5 "good"
# Review added successfully!

# python media_review.py --show-reviews
# [[1] 1 (Stranger Things), 4.5, Amazing movie!
# [2] 1 (Stranger Things), 4.5, Amazing movie!
# [3] 1 (Shape of You), 4.5, Amazing movie!
# [4] 1 (Shape of You), 2, okok
# [5] 1 (Shape of You), 2, okok
# [6] 1 (Stranger Things), 5, good

# python media_review.py --search "Shape of You"
# Shape of You, (song)
# ⭐ 4.5 — Amazing movie!
# ⭐ 2 — okok
# ⭐ 2 — okok

# python media_review.py --add-media "Peaky Blinders" show
# Added show 'Peaky Blinders' to database!
