import logging
from app.core.db import get_session
from app.core.models import Favourites, Media, User

logger = logging.getLogger(__name__)

def add_favourite(media_id, user_id):
    """Add a media item to user's favourites."""
    session = get_session()

    user = session.query(User).get(user_id)
    media = session.query(Media).get(media_id)

    if not user:
        logger.warning(f"User ID {user_id} not found.")
        return {"success": False, "message": "User not found"}

    if not media:
        logger.warning(f"Media ID {media_id} not found.")
        return {"success": False, "message": "Media not found"}

    existing_fav = session.query(Favourites).filter_by(user_id=user.id, media_id=media.id).first()
    if existing_fav:
        logger.info(f"'{media.title}' already in favourites for user {user_id}.")
        return {"success": False, "message": f"'{media.title}' is already in your favourites."}

    fav = Favourites(user_id=user.id, media_id=media.id)
    session.add(fav)
    session.commit()
    logger.info(f"Added '{media.title}' to favourites for user {user_id}.")
    return {"success": True, "message": f"Added '{media.title}' to your favourites."}


def remove_favourite(media_id, user_id):
    """Remove a media item from user's favourites."""
    session = get_session()
    user = session.query(User).get(user_id)

    if not user:
        logger.warning(f"User ID {user_id} not found.")
        return {"success": False, "message": "User not found"}

    fav = session.query(Favourites).filter_by(user_id=user.id, media_id=media_id).first()
    if not fav:
        logger.info(f"Media ID {media_id} not found in favourites for user {user_id}.")
        return {"success": False, "message": "Media not found in favourites."}

    session.delete(fav)
    session.commit()
    logger.info(f"Removed media ID {media_id} from favourites for user {user_id}.")
    return {"success": True, "message": f"Removed media ID {media_id} from favourites."}


def list_favourites(user_id):
    """List all favourites for a given user."""
    session = get_session()
    user_favourites = session.query(Favourites).filter_by(user_id=user_id).all()

    if not user_favourites:
        logger.info(f"No favourites found for user ID {user_id}.")
        return {"success": True, "data": []}

    result = [{"media_id": f.media.id, "title": f.media.title} for f in user_favourites]
    logger.info(f"Fetched {len(result)} favourites for user ID {user_id}.")
    return {"success": True, "data": result}
