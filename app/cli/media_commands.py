from app.services import media_service

def list_media_command():
    medias = media_service.list_media()
    if not medias:
        print("No media found.")
        return

    print("All Media:")
    for m in medias:
        print(f"[{m['id']}] {m['title']} ({m['type']})")


def add_media_command(title, media_type):
    result = media_service.add_media(title, media_type)
    print(result["message"])


def search_by_title_command(title):
    result = media_service.search_media_by_title(title)

    if not result.get("success", True) and "message" in result:
        print(result["message"])
        return

    source = "(from cache)" if result.get("cached") else ""
    print(f"{source} {result['title']} ({result.get('type', '')})")

    reviews = result.get("reviews", [])
    if reviews:
        print("Reviews:")
        for r in reviews:
            print(f"  {r['rating']} — {r['comment']}")
    else:
        print("No reviews yet.")
