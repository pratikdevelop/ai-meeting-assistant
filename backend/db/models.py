from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    JSON
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        default="New Meeting",
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False,
    )

    # Relationship with Transcript
    transcripts: Mapped[list["Transcript"]] = relationship(
        "Transcript",
        back_populates="meeting",
        cascade="all, delete-orphan",
    )

    insight: Mapped["MeetingInsight | None"] = relationship(
        "MeetingInsight",
        back_populates="meeting",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Transcript(Base):
    __tablename__ = "transcripts"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    meeting_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "meetings.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    speaker: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationship with Meeting
    meeting: Mapped["Meeting"] = relationship(
        "Meeting",
        back_populates="transcripts",
    )

class MeetingInsight(Base):
    __tablename__ = "meeting_insights"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    meeting_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "meetings.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    key_points: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    action_items: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    decisions: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    meeting: Mapped["Meeting"] = relationship(
        "Meeting",
        back_populates="insight",
    )