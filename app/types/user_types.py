from typing import TypedDict, List

class UserData(TypedDict):
    id: int
    name: str


class UserResult(TypedDict, total=False):
    success: bool
    message: str
    data: List[UserData]