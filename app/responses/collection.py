from __future__ import annotations

from typing import List, Optional

from likeinterface.types import User

from enums import Rank, Suit
from schema import ApplicationSchema


class CollectionElement(ApplicationSchema):
    file_id: str
    rank: Rank
    suit: Suit


class CollectionResponse(ApplicationSchema):
    id: int
    name: str
    user: Optional[User] = None
    collection_elements: List[CollectionElement]
