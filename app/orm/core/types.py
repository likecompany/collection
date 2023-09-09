from sqlalchemy import ForeignKey, types
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

BigInt = Annotated[int, mapped_column(types.BIGINT)]

String256 = Annotated[str, mapped_column(types.String(256))]
Text = Annotated[str, mapped_column(types.TEXT)]

Collection = Annotated[int, mapped_column(ForeignKey("collection.id"))]
