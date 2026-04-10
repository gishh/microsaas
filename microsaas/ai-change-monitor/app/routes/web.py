from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from app.config import TEMPLATES_DIR
from app.db import get_db
from app.models import Change, Monitor


router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    monitors = (
        db.query(Monitor)
        .options(joinedload(Monitor.snapshots), joinedload(Monitor.changes))
        .order_by(Monitor.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "request": request,
            "monitors": monitors,
        },
    )


@router.get("/monitors/new", response_class=HTMLResponse)
def create_monitor_page(request: Request):
    return templates.TemplateResponse(request, "create_monitor.html", {"request": request, "error": None, "form": {}})


@router.get("/monitors/{monitor_id}", response_class=HTMLResponse)
def monitor_detail(request: Request, monitor_id: int, db: Session = Depends(get_db)):
    monitor = (
        db.query(Monitor)
        .options(joinedload(Monitor.snapshots))
        .filter(Monitor.id == monitor_id)
        .first()
    )
    if monitor is None:
        raise HTTPException(status_code=404, detail="Monitor not found")

    changes = (
        db.query(Change)
        .filter(Change.monitor_id == monitor.id)
        .order_by(Change.created_at.desc())
        .all()
    )
    latest_snapshot = max(monitor.snapshots, key=lambda snapshot: snapshot.fetched_at) if monitor.snapshots else None
    return templates.TemplateResponse(
        request,
        "monitor_detail.html",
        {
            "request": request,
            "monitor": monitor,
            "changes": changes,
            "latest_snapshot": latest_snapshot,
        },
    )


@router.get("/changes/{change_id}", response_class=HTMLResponse)
def change_detail(request: Request, change_id: int, db: Session = Depends(get_db)):
    change = (
        db.query(Change)
        .options(joinedload(Change.previous_snapshot), joinedload(Change.current_snapshot), joinedload(Change.monitor))
        .filter(Change.id == change_id)
        .first()
    )
    if change is None:
        raise HTTPException(status_code=404, detail="Change not found")

    return templates.TemplateResponse(
        request,
        "change_detail.html",
        {
            "request": request,
            "change": change,
        },
    )
