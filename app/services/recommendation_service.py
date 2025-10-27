import logging
from app.core.db import get_session
from app.core.models import User
from app.utils import get_media_with_avg_ratings
from app.types.recommendation_types import RecommendationResult

logger = logging.getLogger(__name__)

def get_top_rated(limit: int = 5) -> RecommendationResult:
    #Return top-rated media along with their average ratings."""
    session = get_session()
    try:
        with get_session() as session:
            rated = get_media_with_avg_ratings(session)
            top = rated[:limit]
            logger.info(f"Fetched top {limit} rated media.")
            return {"success": True, "data": [(m.title, avg) for m, avg in top]}
        
    except Exception as e:
        logger.exception(f"Error fetching top rated media: {e}")
        return {"success": False, "message": "Error fetching top-rated media."}

def recommend_media(user_id: int, limit: int = 5) -> RecommendationResult:
    #based on average ratings.
    
    try:
        with get_session() as session:
            user = session.query(User).get(user_id)
            if not user:
                return {"success": False, "message": "User not found."}

            fav_ids = {fav.media_id for fav in user.favourites}  
            rated = get_media_with_avg_ratings(session)

            recommended = [
                (m.title, avg)
                for m, avg in rated
                if m.id not in fav_ids
            ][:limit]

            logger.info(f"Generated {len(recommended)} recommendations for user {user_id}.")
            return {
                "success": True,
                "user_name": user.name,
                "data": recommended,
            }
        
    except Exception as e:
        logger.exception(f"Error generating recommendations: {e}")
        return {"success": False, "message": "Error generating recommendations."}