from sqlalchemy.orm import mapped_column, DeclarativeBase
from sqlalchemy import text, String
from datetime import datetime, timezone
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', NOW())"),
    nullable=False
)]

updated_at = Annotated[
        datetime,
        mapped_column(
            server_default=text("TIMEZONE('utc', now())"),
            onupdate=datetime.now(timezone.utc)
        )
]

str_200 = Annotated[str, 200]
str_32 = Annotated[str, 32]
str_64 = Annotated[str, 64]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_200: String(200),
        str_32: String(32),
        str_64: String(64)
    }
    pass