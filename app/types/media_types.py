from typing import TypedDict, List

class MediaData(TypedDict):
    id: int
    title: str
    type: str

class MediaListResult(TypedDict):
    success: bool
    data: List[MediaData]

class MediaResult(TypedDict):
    success: bool
    message: str

class ReviewSummary(TypedDict):
    rating: float
    comment: str

class MediaSearchResult(TypedDict, total=False):
    success: bool
    cached: bool
    title: str
    type: str
    message: str
    reviews: List[ReviewSummary]
