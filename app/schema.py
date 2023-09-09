from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

PokerCollectionType = TypeVar("PokerCollectionType", bound=Any)


class ApplicationSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class ApplicationResponse(BaseModel, Generic[PokerCollectionType]):
    model_config = ConfigDict(populate_by_name=True)

    ok: bool
    result: Optional[PokerCollectionType] = None
    detail: Optional[str] = None
    error: Optional[str] = None
    error_code: Optional[int] = None
