from app.db import get_session
from app.models import User
from app.worker import ReviewWorker

def concurrent_reviews():
    worker = ReviewWorker(max_workers=3)
    session = get_session()
    users = session.query(User).all()
    session.close()

    futures = []
    for i, user in enumerate(users[:3]):
        futures.append(
            worker.submit_review(
                user_id=user.id,
                media_id=1,
                rating=4.5 - i * 0.5,
                comment=f"Review from {user.name}",
            )
        )

    worker.wait_for_all(futures)
