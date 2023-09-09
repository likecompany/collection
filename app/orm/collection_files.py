from __future__ import annotations

from sqlalchemy.orm import Mapped

from .core import ORMModel, types


class CollectionFilesModel(ORMModel):
    rank: Mapped[types.Text]
    suit: Mapped[types.Text]

    file_id: Mapped[types.String256]

    collection_id: Mapped[types.Collection]
