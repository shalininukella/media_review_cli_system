import logging
from typing import TypedDict, List
from app.core.db import get_session
from app.core.models import User
from app.types.user_types import UserResult, UserData

logger = logging.getLogger(__name__)

def add_user(name: str) -> UserResult:
    try:
        with get_session() as session:
            existing_user = session.query(User).filter_by(name=name).first()
            if existing_user:
                # Only log as warning if this is unexpected or important for audit
                logger.warning(
                    f"Attempt to add existing user '{name}' (id={existing_user.id})."
                )
                return {"success": False, "message": f"User '{name}' already exists."}

            user = User(name=name)
            session.add(user)
            session.commit()
            return {
                "success": True,
                "message": f"Added user '{name}' successfully.",
                "data": [{"id": user.id, "name": name}],
            }
    except Exception as e:
        logger.exception(f"Error adding user '{name}': {e}")
        return {"success": False, "message": "Error adding user."}


def list_users() -> UserResult:
    try:
        with get_session() as session:
            users = session.query(User).all()
            user_data: List[UserData] = [{"id": u.id, "name": u.name} for u in users]
            return {"success": True, "data": user_data}
    except Exception as e:
        logger.exception(f"Error listing users: {e}")
        return {"success": False, "message": "Error fetching users."}
