"""
handles commands like --list, --review, --search, --show-reviews
"""

import argparse
from app.db import get_session
from app.models import Media, Reviews, User, Favourites
from app.observer import NotificationService
from app.observer_manager import ReviewNotifier


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

    review = Reviews(user_id=user_id, media_id=media_id, rating=rating, comment=comment)
    session.add(review)
    session.commit()
    print("Review added successfully!")

    # notify the observers
    media = session.query(Media).filter_by(id=media_id).first()

    notifier = ReviewNotifier()
    observer = NotificationService()
    notifier.attach(observer)
    notifier.notify(media, review, session)


def list_reviews():
    session = get_session()
    reviews = session.query(Reviews).all()
    if not reviews:
        print("No reviews yet.")
        return

    for r in reviews:
        print(f"[{r.id}] {r.user.id} ({r.media.title}), {r.rating}, {r.comment}")


# for factory
from app.media_factory import MediaFactory


def add_media(title, media_type):
    session = get_session()
    media_row = MediaFactory.create_media(title, media_type)
    session.add(media_row)
    session.commit()
    print(f"Added {media_type} '{title}' to database!")


# for observer
def add_favourite(media_id, user_id):
    session = get_session()
    user = session.query(User).get(user_id)
    media = session.query(Media).get(media_id)

    if not user:
        print("user not found")
        return

    elif not media:
        print("media not found")
        return

    # when both user and media exists
    existing_fav = (
        session.query(Favourites).filter_by(user_id=user.id, media_id=media.id).first()
    )
    if existing_fav:
        print(f"'{media.title}' is already in your favorites.")
        return

    fav = Favourites(user_id=user.id, media_id=media.id)
    session.add(fav)
    session.commit()
    print(f"Added '{media.title}' to your favorites.")


def remove_favourite(media_id, user_id):
    session = get_session()
    user = session.query(User).get(user_id)

    if not user:
        print("no user found")
        return

    fav = (
        session.query(Favourites).filter_by(user_id=user.id, media_id=media_id).first()
    )

    if not fav:
        print("Media not found in favorites.")
        return

    session.delete(fav)
    session.commit()
    print(f"Removed media ID {media_id} from favorites.")


def show_favourites(user_id):
    session = get_session()
    user_favourites = session.query(Favourites).filter_by(user_id=user_id).all()

    if not user_favourites:
        print("You haven’t favorited any media yet.")
        return

    print("Your favourites:")
    for fav in user_favourites:
        print(f"  - {fav.media.title} (ID: {fav.media.id})")


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

    # New favorite related commands
    parser.add_argument(
        "--favourite",
        nargs=2,
        metavar=("MEDIA_ID", "USER_ID"),
        help="Favourite a particular media",
    )
    parser.add_argument(
        "--unfavourite",
        nargs=2,
        metavar=("MEDIA_ID", "USER_ID"),
        help="Unfavourite a particular media",
    )
    parser.add_argument(
        "--show-favourites",
        metavar="USER_ID",
        help="Show all the favourite media of a user",
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
    elif args.favourite:
        media_id, user_id = args.favourite
        add_favourite(media_id, user_id)
    elif args.unfavourite:
        media_id, user_id = args.unfavourite
        remove_favourite(media_id, user_id)
    elif args.show_favourites:
        user_id = args.show_favourites
        show_favourites(user_id)
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
