import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.services.review_service import add_review

# Configure logging for this module
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

class ReviewWorker:
    """Handles concurrent review submissions safely using add_review."""

    def __init__(self, max_workers=5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit_review(self, user_id: int, media_id: int, rating: float, comment: str):
        """Submit a review asynchronously via add_review."""
        return self.executor.submit(add_review, user_id, media_id, rating, comment)

    def wait_for_all(self, futures):
        """Wait for all submitted reviews to complete and log the results."""
        for future in as_completed(futures):
            result = future.result()  # this is the dict returned by add_review
            if result.get("success"):
                logger.info(result.get("message"))
            else:
                logger.warning(result.get("message"))
