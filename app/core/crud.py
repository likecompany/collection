from __future__ import annotations

from corecrud import CRUD as CCRUD  # noqa
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from orm import CollectionElementModel, CollectionModel


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class CRUD:
    collections: CCRUD[CollectionModel] = CCRUD(CollectionModel)
    collection_elements: CCRUD[CollectionElementModel] = CCRUD(CollectionElementModel)


crud = CRUD()
