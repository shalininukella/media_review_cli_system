from app.core.models import Media

def get_media_with_avg_ratings(session):
    """
    Returns a list of tuples (Media, avg_rating), sorted descending.
    Only media with at least one review are returned.
    """
    media_list = session.query(Media).all()
    rated = []

    for media in media_list:
        if media.reviews:
            avg_rating = sum(r.rating for r in media.reviews) / len(media.reviews)
            rated.append((media, avg_rating))

    rated.sort(key=lambda x: x[1], reverse=True)
    return rated
