from typing import TypedDict, List

class FavouriteItem(TypedDict):
    media_id: int
    title: str

class FavouriteResult(TypedDict):
    success: bool
    message: str

class FavouriteListResult(TypedDict, total=False):
    success: bool
    data: List[FavouriteItem]
    message: str
