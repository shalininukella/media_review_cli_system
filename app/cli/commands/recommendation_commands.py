from app.services import recommendation_service

def get_top_rated_command(limit=5) -> dict:
    return recommendation_service.get_top_rated(limit)

def recommend_media_command(user_id: int, limit=5) -> dict:
    return recommendation_service.recommend_media(user_id, limit)
