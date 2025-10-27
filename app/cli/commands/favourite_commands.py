from app.services import favourite_service

def add_favourite_command(media_id: int, user_id: int) -> dict:
    return favourite_service.add_favourite(media_id, user_id)

def remove_favourite_command(media_id: int, user_id: int) -> dict:
    return favourite_service.remove_favourite(media_id, user_id)

def show_favourites_command(user_id: int) -> dict:
    return favourite_service.list_favourites(user_id)
