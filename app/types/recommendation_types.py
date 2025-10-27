from typing import TypedDict, List

# One entry representing a media and its average rating
class MediaRating(TypedDict):
    title: str
    average_rating: float


# Response type for both functions
class RecommendationResult(TypedDict, total=False):
    success: bool
    message: str
    user_name: str
    data: List[MediaRating]
