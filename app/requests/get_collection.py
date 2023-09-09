from __future__ import annotations

from schema import ApplicationSchema


class GetCollectionRequest(ApplicationSchema):
    name: str
