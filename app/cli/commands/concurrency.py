from app.services.concurrency_service import ReviewWorker
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def concurrent_reviews_command(args_list):
    if len(args_list) % 4 != 0:
        logger.error("Each review must have USER_ID MEDIA_ID RATING COMMENT")
        return

    reviews = []
    for i in range(0, len(args_list), 4):
        try:
            user_id = int(args_list[i])
            media_id = int(args_list[i + 1])
            rating = float(args_list[i + 2])
            comment = args_list[i + 3]
            reviews.append((user_id, media_id, rating, comment))
        except ValueError:
            logger.error("Invalid USER_ID or RATING format")
            return

    worker = ReviewWorker(max_workers=len(reviews))
    futures = [worker.submit_review(*r) for r in reviews]
    worker.wait_for_all(futures)
