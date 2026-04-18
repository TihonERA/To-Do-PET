from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, UUID, ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING
from base import intpk, created_at, Base

if TYPE_CHECKING:
    from .user import User 

class Tasks(Base):
    __tablename__ = "tasks"

    tasks_id: Mapped[intpk]
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    priority: Mapped[int] = mapped_column(default=0)
    created: Mapped[created_at]
    completed: Mapped[datetime | None] = mapped_column(nullable=True, default=None)
    status: Mapped[bool] = mapped_column(default=False)
    due_date: Mapped[datetime | None] = mapped_column(nullable=True, default=None)

    user: Mapped["User"] = relationship(back_populates="tasks")