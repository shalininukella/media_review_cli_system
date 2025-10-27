# app/types/review_types.py
from typing import TypedDict, List

class ReviewData(TypedDict):
    id: int
    user_id: int
    media_title: str
    rating: float
    comment: str

class ReviewResult(TypedDict, total=False):
    success: bool
    message: str
    data: List[ReviewData]
