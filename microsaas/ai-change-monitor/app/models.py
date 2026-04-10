from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Monitor(Base):
    __tablename__ = "monitors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    snapshots: Mapped[list["Snapshot"]] = relationship(
        "Snapshot", back_populates="monitor", cascade="all, delete-orphan", foreign_keys="Snapshot.monitor_id"
    )
    changes: Mapped[list["Change"]] = relationship(
        "Change", back_populates="monitor", cascade="all, delete-orphan", foreign_keys="Change.monitor_id"
    )


class Snapshot(Base):
    __tablename__ = "snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    monitor_id: Mapped[int] = mapped_column(ForeignKey("monitors.id"), nullable=False, index=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_text: Mapped[str] = mapped_column(Text, nullable=False)

    monitor: Mapped["Monitor"] = relationship("Monitor", back_populates="snapshots", foreign_keys=[monitor_id])


class Change(Base):
    __tablename__ = "changes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    monitor_id: Mapped[int] = mapped_column(ForeignKey("monitors.id"), nullable=False, index=True)
    previous_snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshots.id"), nullable=False)
    current_snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshots.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    diff_text: Mapped[str] = mapped_column(Text, nullable=False)

    monitor: Mapped["Monitor"] = relationship("Monitor", back_populates="changes", foreign_keys=[monitor_id])
    previous_snapshot: Mapped["Snapshot"] = relationship("Snapshot", foreign_keys=[previous_snapshot_id])
    current_snapshot: Mapped["Snapshot"] = relationship("Snapshot", foreign_keys=[current_snapshot_id])
