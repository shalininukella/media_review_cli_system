from app.models import Favourites
from app.observer.base import Observer


class NotificationService(Observer):

    def update(self, media, review, session):
        users_of_favourite_media = session.query(Favourites).filter_by(media_id=media.id).all()

        if not users_of_favourite_media:
            print(f"No users favorited '{media.title}', skip notification.")
            return

        print(f"Sending notifications for '{media.title}'...")
        for fav in users_of_favourite_media:
            print(f"Notifying {fav.user.name}: New review added (Rating: {review.rating})")


# Example of an additional observer (optional)
# class AnalyticsService(Observer):
#     def update(self, media, review, session):
#         print(f"Updating analytics for '{media.title}' — New rating: {review.rating}")
