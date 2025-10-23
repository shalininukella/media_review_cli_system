# app/cli/media_commands.py
from app.db import get_session
from app.models import Media, Reviews, User
from sqlalchemy import func

# Top-Rated
from app.db import get_session
from app.models import Media

def get_top_rated(limit=5):
    session = get_session()
    media_list = session.query(Media).all()
    rated = []

    for media in media_list:
        if media.reviews:
            avg_rating = sum(r.rating for r in media.reviews) / len(media.reviews)
            rated.append((media.title, avg_rating))

    # sort by average rating descending
    rated.sort(key=lambda x: x[1], reverse=True)
    top = rated[:limit]

    print("\nTop Rated Media:")
    for title, avg in top:
        print(f" - {title}: {avg:.1f}")

    session.close()


# Recommendations
from app.db import get_session
from app.models import User, Media

def recommend_media(user_id, limit=5):
    session = get_session()
    user = session.query(User).get(user_id)
    if not user:
        print("User not found.")
        return

    # IDs of media already favorited by the user
    fav_ids = {m.id for m in user.favorites}

    # Recommend any media not in user's favorites
    all_media = session.query(Media).all()
    recommended = [m.title for m in all_media if m.id not in fav_ids][:limit]

    print(f"\nRecommendations for {user.name}:")
    if recommended:
        for title in recommended:
            print(f" - {title}")
    else:
        print("No recommendations available.")

    session.close()
