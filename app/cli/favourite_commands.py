from app.services import favourite_service

def add_favourite_command(media_id, user_id):
    result = favourite_service.add_favourite(media_id, user_id)
    print(result["message"])

def remove_favourite_command(media_id, user_id):
    result = favourite_service.remove_favourite(media_id, user_id)
    print(result["message"])

def show_favourites_command(user_id):
    result = favourite_service.list_favourites(user_id)

    if not result["data"]:
        print("You haven’t favourited any media yet.")
        return

    print("Your favourites:")
    for fav in result["data"]:
        print(f"  - {fav['title']} (ID: {fav['media_id']})")

