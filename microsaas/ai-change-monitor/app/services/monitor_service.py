import hashlib
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Change, Monitor, Snapshot
from app.services.differ import build_diff
from app.services.extractor import extract_visible_text, normalize_text
from app.services.fetcher import fetch_page
from app.services.summarizer import summarize_diff


def create_monitor_record(db: Session, name: str, url: str) -> Monitor:
    monitor = Monitor(name=name, url=url)
    db.add(monitor)
    db.commit()
    db.refresh(monitor)
    return monitor


def get_monitor(db: Session, monitor_id: int) -> Monitor:
    monitor = db.get(Monitor, monitor_id)
    if monitor is None:
        raise ValueError("Monitor not found")
    return monitor


def build_snapshot(monitor_id: int, raw_text: str, normalized_text: str, content_hash: str) -> Snapshot:
    return Snapshot(
        monitor_id=monitor_id,
        content_hash=content_hash,
        raw_text=raw_text,
        normalized_text=normalized_text,
    )


def run_monitor_check(db: Session, monitor_id: int) -> dict:
    monitor = get_monitor(db, monitor_id)

    html = fetch_page(monitor.url)
    raw_text = extract_visible_text(html)
    normalized_text = normalize_text(raw_text)
    content_hash = hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()

    latest_snapshot = (
        db.query(Snapshot)
        .filter(Snapshot.monitor_id == monitor.id)
        .order_by(Snapshot.fetched_at.desc(), Snapshot.id.desc())
        .first()
    )

    monitor.last_checked_at = datetime.utcnow()
    created_change = None

    if latest_snapshot is None:
        snapshot = build_snapshot(monitor.id, raw_text, normalized_text, content_hash)
        db.add(snapshot)
    elif latest_snapshot.content_hash != content_hash:
        snapshot = build_snapshot(monitor.id, raw_text, normalized_text, content_hash)
        db.add(snapshot)
        db.flush()

        diff_text = build_diff(latest_snapshot.normalized_text, normalized_text)
        created_change = Change(
            monitor_id=monitor.id,
            previous_snapshot_id=latest_snapshot.id,
            current_snapshot_id=snapshot.id,
            summary=summarize_diff(diff_text),
            diff_text=diff_text,
        )
        db.add(created_change)

    db.commit()

    if created_change is not None:
        db.refresh(created_change)

    return {
        "changed": created_change is not None,
        "change_id": created_change.id if created_change is not None else None,
    }
