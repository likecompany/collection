from __future__ import annotations

from typing import List

from pydantic import AfterValidator, Field
from typing_extensions import Annotated, Final

from enums import Rank, Suit
from schema import ApplicationSchema

CARDS: Final[int] = len(Suit) * len(Rank)


class Collection(ApplicationSchema):
    file_id: str
    rank: Rank
    suit: Suit


class CollectionHelper(ApplicationSchema):
    rank: Rank
    suit: Suit

    def __hash__(self) -> int:
        return hash(self.rank) + hash(self.suit)


def validate_collection(collection: List[Collection]) -> List[Collection]:
    if {CollectionHelper(rank=rank, suit=suit) for rank in Rank for suit in Suit} != {
        CollectionHelper(rank=card.rank, suit=card.suit) for card in collection
    }:
        raise ValueError("NOT_ENOUGH_CARDS")

    return collection


class AddCollectionRequest(ApplicationSchema):
    access_token: str
    name: str
    collection: Annotated[List[Collection], AfterValidator(validate_collection)] = Field(
        min_length=CARDS,
        max_length=CARDS,
    )
