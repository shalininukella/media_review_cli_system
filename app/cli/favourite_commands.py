from app.db import get_session
from app.models import Favourites, Media, User

def add_favourite(media_id, user_id):
    session = get_session()
    user = session.query(User).get(user_id)
    media = session.query(Media).get(media_id)

    if not user:
        print("user not found")
        return
    elif not media:
        print("media not found")
        return

    existing_fav = session.query(Favourites).filter_by(user_id=user.id, media_id=media.id).first()
    if existing_fav:
        print(f"'{media.title}' is already in your favorites.")
        return

    fav = Favourites(user_id=user.id, media_id=media.id)
    session.add(fav)
    session.commit()
    print(f"Added '{media.title}' to your favorites.")

def remove_favourite(media_id, user_id):
    session = get_session()
    user = session.query(User).get(user_id)
    if not user:
        print("no user found")
        return

    fav = session.query(Favourites).filter_by(user_id=user.id, media_id=media_id).first()
    if not fav:
        print("Media not found in favorites.")
        return

    session.delete(fav)
    session.commit()
    print(f"Removed media ID {media_id} from favorites.")

def show_favourites(user_id):
    session = get_session()
    user_favourites = session.query(Favourites).filter_by(user_id=user_id).all()

    if not user_favourites:
        print("You haven’t favorited any media yet.")
        return

    print("Your favourites:")
    for fav in user_favourites:
        print(f"  - {fav.media.title} (ID: {fav.media.id})")
