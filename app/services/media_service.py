import json
import logging
from app.core.db import get_session
from app.core.models import Media
from app.core.cache import cache_get, cache_set
from app.core.media_factory import MediaFactory

logger = logging.getLogger(__name__)

def list_media():
    """Fetch all media entries."""
    session = get_session()
    medias = session.query(Media).all()
    logger.info(f"Fetched {len(medias)} media entries.")
    return [{"id": m.id, "title": m.title, "type": m.type} for m in medias]


def add_media(title, media_type):
    """Add a new media item."""
    session = get_session()
    media_row = MediaFactory.create_media(title, media_type)
    session.add(media_row)
    session.commit()
    logger.info(f"Added new {media_type}: '{title}'.")
    return {"success": True, "message": f"Added {media_type} '{title}' to database!"}


def search_media_by_title(title):
    """Search for media and its reviews, using cache."""
    cache_key = f"reviews:{title.lower()}"
    cached = cache_get(cache_key)

    if cached:
        logger.info(f"Cache hit for '{title}'.")
        reviews = json.loads(cached)
        return {
            "cached": True,
            "title": title,
            "reviews": reviews,
        }

    session = get_session()
    media_row = session.query(Media).filter_by(title=title).first()

    if not media_row:
        logger.warning(f"No media found with title '{title}'.")
        return {"success": False, "message": f"No media found with title '{title}'"}

    reviews = [{"rating": r.rating, "comment": r.comment} for r in media_row.reviews]
    if reviews:
        cache_set(cache_key, json.dumps(reviews), ttl=120)
        logger.info(f"Cached reviews for '{title}'.")

    return {
        "success": True,
        "cached": False,
        "title": media_row.title,
        "type": media_row.type,
        "reviews": reviews,
    }
