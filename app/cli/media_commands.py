from app.db import get_session
from app.models import Media
from app.media_factory import MediaFactory
from app.cache import cache_get, cache_set
import json


def list_media():
    session = get_session()
    medias = session.query(Media).all()
    for m in medias:
        print(f"[{m.id}] {m.title} ({m.type})")


def add_media(title, media_type):
    session = get_session()
    media_row = MediaFactory.create_media(title, media_type)
    session.add(media_row)
    session.commit()
    print(f"Added {media_type} '{title}' to database!")


def search_by_title(title):
    cache_key = f"reviews:{title.lower()}"

    # fetch from Redis
    cached = cache_get(cache_key)
    if cached:
        print(f"(from cache) Reviews for '{title}':")
        reviews = json.loads(cached)
        for r in reviews:
            print(f"{r['rating']} — {r['comment']}")
        return

    # If not cached, fetch from DB
    session = get_session()
    media_row = session.query(Media).filter_by(title=title).first()
    if not media_row:
        print(f"No media found with title '{title}'")
        return

    print(f"{media_row.title}, ({media_row.type})")

    if media_row.reviews:
        reviews = [
            {"rating": r.rating, "comment": r.comment} for r in media_row.reviews
        ]
        for r in reviews:
            print(f"{r['rating']} — {r['comment']}")
        # Store in Redis for next time
        cache_set(cache_key, json.dumps(reviews), ttl=120)  # 2 min cache
    else:
        print("No reviews yet.")
