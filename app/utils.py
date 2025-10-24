from app.db import get_session
from app.models import Media

def get_media_with_avg_ratings(session):
    """Return list of (media, avg_rating) tuples for all media that have reviews."""
    media_list = session.query(Media).all()
    rated = []

    for media in media_list:
        if media.reviews:
            avg_rating = sum(r.rating for r in media.reviews) / len(media.reviews)
            rated.append((media, avg_rating))

    # Sort descending by rating
    rated.sort(key=lambda x: x[1], reverse=True)
    return rated
