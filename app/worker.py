# app/worker.py
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.db import get_session
from app.models import Reviews, User, Media
from datetime import datetime

lock = threading.Lock()

class ReviewWorker:
    """Handles concurrent review submissions safely."""

    def __init__(self, max_workers=5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit_review(self, user_id, media_id, rating, comment):
        """Submit a review in a separate thread."""
        return self.executor.submit(self._process_review, user_id, media_id, rating, comment)

    def _process_review(self, user_id, media_id, rating, comment):
        """Actual work done inside each thread."""
        session = get_session()
        try:
            user = session.get(User, user_id)
            media = session.get(Media, media_id)

            if not user or not media:
                return f"Invalid user ({user_id}) or media ({media_id})"

            with lock:  # prevent race conditions on same DB write
                review = Reviews(
                    user_id=user.id,
                    media_id=media.id,
                    rating=rating,
                    comment=comment,
                    created_at=datetime.utcnow()
                )
                session.add(review)
                session.commit()
                return f" Review added by {user.name} for '{media.title}'"
        except Exception as e:
            session.rollback()
            return f" Error: {e}"
        finally:
            session.close()

    def wait_for_all(self, futures):
        """Wait for all threads to complete."""
        for future in as_completed(futures):
            print(future.result())
