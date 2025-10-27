import logging
from app.services import user_service

logger = logging.getLogger(__name__)

def add_user(name: str) -> dict:
    result = user_service.add_user(name)
    return result  # cli/handler/main will handle logging/display

def list_users() -> dict:
    result = user_service.list_users()
    return result 