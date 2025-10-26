from app.services.concurrency_service import ReviewWorker

def concurrent_reviews_command(args_list):
    """
    args_list: list of strings from CLI, e.g.
    ["1", "2", "4.5", "Great movie", "2", "1", "3.0", "Not bad"]
    """
    # Convert args_list to chunks of 4 (user_id, media_id, rating, comment)
    if len(args_list) % 4 != 0:
        print("Error: Each review must have USER_ID MEDIA_ID RATING COMMENT")
        return

    reviews = []
    for i in range(0, len(args_list), 4):
        user_id = int(args_list[i])
        media_id = int(args_list[i+1])
        rating = float(args_list[i+2])
        comment = args_list[i+3]
        reviews.append((user_id, media_id, rating, comment))

    worker = ReviewWorker(max_workers=len(reviews))
    futures = [worker.submit_review(*r) for r in reviews]
    worker.wait_for_all(futures)
