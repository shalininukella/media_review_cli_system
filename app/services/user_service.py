import logging
from app.core.db import get_session
from app.core.models import User

logger = logging.getLogger(__name__)

def add_user(name: str):
    """Add a new user if not already present."""
    session = get_session()
    try:
        existing_user = session.query(User).filter_by(name=name).first()
        if existing_user:
            logger.info(f"User '{name}' already exists (id={existing_user.id}).")
            return {"success": False, "message": f"User '{name}' already exists."}

        user = User(name=name)
        session.add(user)
        session.commit()
        logger.info(f"User '{name}' added successfully (id={user.id}).")
        return {"success": True, "message": f"Added user '{name}' successfully.", "data": {"id": user.id, "name": name}}
    except Exception as e:
        logger.exception(f"Error adding user '{name}': {e}")
        session.rollback()
        return {"success": False, "message": "Error adding user."}
    finally:
        session.close()


def list_users():
    """Fetch and return all users."""
    session = get_session()
    try:
        users = session.query(User).all()
        if not users:
            logger.info("No users found.")
            return {"success": True, "data": []}

        user_data = [{"id": u.id, "name": u.name} for u in users]
        logger.info(f"Fetched {len(user_data)} users from database.")
        return {"success": True, "data": user_data}
    except Exception as e:
        logger.exception(f"Error listing users: {e}")
        return {"success": False, "message": "Error fetching users."}
    finally:
        session.close()
