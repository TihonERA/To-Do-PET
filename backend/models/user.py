from sqlalchemy.orm import mapped_column, Mapped, relationship
import uuid
from sqlalchemy import text, String
from uuid import uuid4
from backend.models.base import str_32, str_200, created_at, Base
from .task import Tasks

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()")
    )
    login: Mapped[str_32] = mapped_column(unique=True, index=True)
    hash_pass: Mapped[str_200]
    created: Mapped[created_at]
    email: Mapped[str] = mapped_column(String(64), index=True)

    tasks: Mapped[list["Tasks"]] = relationship(back_populates="user")