from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .core import ORMModel, types

if TYPE_CHECKING:
    from .collection_files import CollectionElementModel


class CollectionModel(ORMModel):
    name: Mapped[types.String256] = mapped_column(unique=True)
    user_id: Mapped[types.BigInt]
    collection_elements: Mapped[List[CollectionElementModel]] = relationship()
