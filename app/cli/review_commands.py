from app.db import get_session
from app.models import Media, Reviews, User
from app.observer import NotificationService
from app.observer.observer_manager import ReviewNotifier
from app.cache import cache


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

    #observer - notifications
    media = session.query(Media).get(media_id)
    notifier = ReviewNotifier()
    observer = NotificationService()
    notifier.attach(observer)
    notifier.notify(media, review, session)

    # invalidate cache for this media
    cache.delete(f"reviews:{media.title.lower()}")


def list_reviews():
    session = get_session()
    reviews = session.query(Reviews).all()
    if not reviews:
        print("No reviews yet.")
        return

    for r in reviews:
        print(f"[{r.id}] {r.user.id} ({r.media.title}), {r.rating}, {r.comment}")
