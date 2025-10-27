import logging
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from app.services.review_service import add_review
from app.types.review_types import ReviewResult
from typing import List

logger = logging.getLogger(__name__)

class ReviewWorker:
    #Handles concurrent review submissions safely using add_review.

    def __init__(self, max_workers=5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit_review(
        self, user_id: int, media_id: int, rating: float, comment: str
    ) -> Future[ReviewResult]:
        #Submit a review asynchronously via add_review.
        return self.executor.submit(add_review, user_id, media_id, rating, comment)

    def wait_for_all(self, futures: List[Future[ReviewResult]]) -> None:
        #Wait for all submitted reviews to complete and log the results.
        for future in as_completed(futures):
            result = future.result()
            if result.get("success"):
                logger.info(result.get("message"))
            else:
                logger.warning(result.get("message"))

    def close(self) -> None:
        #Shutdown the executor cleanly.
        self.executor.shutdown(wait=True)
