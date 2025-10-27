import logging
from app.core.db import get_session
from app.core.models import Favourites, Media, User
from app.types.favourite_types import FavouriteResult, FavouriteListResult

logger = logging.getLogger(__name__)


def add_favourite(media_id: int, user_id: int) -> FavouriteResult:
    try:
        with get_session() as session:
            user = session.get(User, user_id)
            media = session.get(Media, media_id)

            if not user:
                return {"success": False, "message": "User not found"}
            if not media:
                return {"success": False, "message": "Media not found"}

            existing_fav = (
                session.query(Favourites)
                .filter_by(user_id=user.id, media_id=media.id)
                .first()
            )
            if existing_fav:
                return {
                    "success": False,
                    "message": f"'{media.title}' is already in your favourites.",
                }

            fav = Favourites(user_id=user.id, media_id=media.id)
            session.add(fav)
            session.commit()
            return {
                "success": True,
                "message": f"Added '{media.title}' to your favourites.",
            }

    except Exception as e:
        logger.exception(
            f"Failed to add favourite for user {user_id}, media {media_id}"
        )
        return {
            "success": False,
            "message": "Failed to add favourite due to an internal error.",
        }


def remove_favourite(media_id: int, user_id: int) -> FavouriteResult:
    try:
        with get_session() as session:
            user = session.get(User, user_id)
            media = session.get(Media, media_id)

            if not user:
                return {"success": False, "message": "User not found"}
            if not media:
                return {"success": False, "message": "Media not found"}

            fav = (
                session.query(Favourites)
                .filter_by(user_id=user.id, media_id=media_id)
                .first()
            )

            if not fav:
                return {"success": False, "message": "Media not found in favourites."}

            media = session.get(Media, media_id)
            session.delete(fav)
            session.commit()
            return {
                "success": True,
                "message": f"Removed '{media.title}' from your favourites.",
            }

    except Exception as e:
        logger.exception(
            f"Failed to remove favourite for user {user_id}, media {media_id}"
        )
        return {
            "success": False,
            "message": "Failed to remove favourite due to an internal error.",
        }


def list_favourites(user_id: int) -> FavouriteListResult:
    try:
        with get_session() as session:
            user = session.get(User, user_id)
            if not user:
                return {"success": False, "message": "User not found"}

            favs = session.query(Favourites).filter_by(user_id=user_id).all()
            if not favs:
                return {"success": True, "data": []}

            result = [{"media_id": f.media.id, "title": f.media.title} for f in favs]
            return {"success": True, "data": result}

    except Exception as e:
        logger.exception(f"Failed to fetch favourites for user {user_id}")
        return {
            "success": False,
            "data": [],
            "message": "Failed to fetch favourites due to an internal error.",
        }
