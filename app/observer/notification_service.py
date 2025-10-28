import logging
from sqlalchemy.orm import joinedload
from app.core.models import Favourites
from app.observer.base import Observer

logger = logging.getLogger(__name__)

class NotificationService(Observer):
    def update(self, media, review, session):
        try:
            # Eagerly load user relationship
            favourites = (
                session.query(Favourites)
                .options(joinedload(Favourites.user))
                .filter_by(media_id=media.id)
                .all()
            )

            if not favourites:
                logger.info(f"No favourites for '{media.title}'.")
                return

            logger.info(f"Sending notifications for '{media.title}' to {len(favourites)} users.")
            for fav in favourites:
                logger.info(f"Notifying {fav.user.name}: New review added (Rating: {review.rating})")

        except Exception as e:
            logger.exception(f"Notification error for '{media.title}': {e}")


# Example of an additional observer (optional)
# class AnalyticsService(Observer):
#     def update(self, media, review, session):
#         print(f"Updating analytics for '{media.title}' — New rating: {review.rating}")