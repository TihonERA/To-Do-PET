from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import text, String, UUID
from uuid import uuid4
from base import str_32, str_200, created_at, Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()")
    )
    login: Mapped[str_32] = mapped_column(unique=True, index=True)
    hash_pass: Mapped[str_200]
    created: Mapped[created_at]
    email: Mapped[str] = mapped_column(String(64), index=True)