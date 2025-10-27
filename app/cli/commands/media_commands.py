from app.services import media_service

def list_media_command() -> dict:
    medias = media_service.list_media()
    if not medias:
        return {"success": True, "data": [], "message": "No media found."}
    return {"success": True, "data": medias}


def add_media_command(title: str, media_type: str) -> dict:
    return media_service.add_media(title, media_type)


def search_by_title_command(title: str) -> dict:
    return media_service.search_media_by_title(title)
