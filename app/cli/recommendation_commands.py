from app.db import get_session
from app.models import User
from app.utils import get_media_with_avg_ratings


def get_top_rated(limit=5):
    session = get_session()
    rated = get_media_with_avg_ratings(session)
    top = rated[:limit]

    print("Top Rated Media:")
    for media, avg in top:
        print(f" - {media.title}: {avg:.1f}")

    session.close()


def recommend_media(user_id, limit=5):
    session = get_session()
    user = session.query(User).get(user_id)
    if not user:
        print("User not found.")
        return

    fav_ids = {m.id for m in user.favourites}

    # Get sorted rated media and exclude favorites
    rated = get_media_with_avg_ratings(session)
    recommended = [(m, avg) for m, avg in rated if m.id not in fav_ids][:limit]

    print(f"Recommendations for {user.name}:")
    if recommended:
        for media, avg in recommended:
            print(f" - {media.title} (avg rating: {avg:.1f})")
    else:
        print("No recommendations available.")

    session.close()
