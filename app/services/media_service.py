import json
import logging
from app.core.db import get_session
from app.core.models import Media
from app.cache import cache_get, cache_set
from app.core.media_factory import MediaFactory
from app.types.media_types import MediaListResult, MediaResult, MediaSearchResult

logger = logging.getLogger(__name__)

def list_media() -> MediaListResult:
    with get_session() as session:
        medias = session.query(Media).all()
        return [{"id": m.id, "title": m.title, "type": m.type} for m in medias]

def add_media(title: str, media_type: str) -> MediaResult:
    try:
        with get_session() as session:
            media_row = MediaFactory.create_media(title, media_type)
            session.add(media_row)
            session.commit()
            return {"success": True, "message": f"Added {media_type} '{title}' to database!"}
    except Exception as e:
        logger.exception(f"Failed to add media '{title}': {e}")
        return {"success": False, "message": "Failed to add media due to an internal error."}


def search_media_by_title(title: str) -> MediaSearchResult:
    #Search for media and its reviews, using cache
    cache_key = f"reviews:{title.lower()}"
    cached = cache_get(cache_key)

    if cached:
        reviews = json.loads(cached)
        return {"success": True, "cached": True, "title": title, "reviews": reviews}

    with get_session() as session:
        media_row = session.query(Media).filter_by(title=title).first()
        if not media_row:
            logger.warning(f"No media found with title '{title}'.")
            return {"success": False, "message": f"No media found with title '{title}'"}

        reviews = [{"rating": r.rating, "comment": r.comment} for r in media_row.reviews]
        if reviews:
            cache_set(cache_key, json.dumps(reviews), ttl=120)

        return {
            "success": True,
            "cached": False,
            "title": media_row.title,
            "type": media_row.type,
            "reviews": reviews,
        }
