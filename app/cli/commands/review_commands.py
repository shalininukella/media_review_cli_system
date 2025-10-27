from app.services import review_service

def add_review_command(user_id: int, media_id: int, rating: float, comment: str) -> dict:
    return review_service.add_review(user_id, media_id, rating, comment)

def list_reviews_command() -> dict:
    return review_service.list_reviews()
