import logging
from app.core.db import get_session
from app.core.models import Media, Reviews, User
from app.cache import cache
from app.observer.observer_manager import ReviewNotifier
from app.observer import NotificationService

logger = logging.getLogger(__name__)

def add_review(user_id: int, media_id: int, rating: int, comment: str):
    """Add a review, trigger notifications, and invalidate cache."""
    session = get_session()
    try:
        user = session.query(User).get(user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found.")
            return {"success": False, "message": "User not found."}

        media = session.query(Media).get(media_id)
        if not media:
            logger.warning(f"Media with ID {media_id} not found.")
            return {"success": False, "message": "Media not found."}

        review = Reviews(
            user_id=user_id,
            media_id=media_id,
            rating=rating,
            comment=comment
        )
        session.add(review)
        session.commit()
        logger.info(f"Review added for media_id={media_id} by user_id={user_id}")

        # Notify observers (notification services)
        notifier = ReviewNotifier()
        observer = NotificationService()
        notifier.attach(observer)
        notifier.notify(media, review, session)

        # Invalidate cache
        cache_key = f"reviews:{media.title.lower()}"
        cache.delete(cache_key)
        logger.info(f"Invalidated cache for key: {cache_key}")

        return {"success": True, "message": "Review added successfully!"}
    except Exception as e:
        logger.exception(f"Error adding review: {e}")
        session.rollback()
        return {"success": False, "message": "Failed to add review."}
    finally:
        session.close()


def list_reviews():
    """Return all reviews in structured format."""
    session = get_session()
    try:
        reviews = session.query(Reviews).all()
        if not reviews:
            return {"success": True, "data": []}

        data = [
            {
                "id": r.id,
                "user_id": r.user.id,
                "media_title": r.media.title,
                "rating": r.rating,
                "comment": r.comment
            }
            for r in reviews
        ]
        logger.info(f"Fetched {len(data)} reviews from database.")
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception(f"Error listing reviews: {e}")
        return {"success": False, "message": "Error fetching reviews."}
    finally:
        session.close()
