from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import TEMPLATES_DIR
from app.db import get_db
from app.schemas import MonitorCreate
from app.services.monitor_service import create_monitor_record, run_monitor_check


router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.post("/monitors")
def create_monitor(
    request: Request,
    name: str = Form(...),
    url: str = Form(...),
    db: Session = Depends(get_db),
):
    form_data = {"name": name.strip(), "url": url.strip()}
    try:
        payload = MonitorCreate(**form_data)
    except Exception:
        return templates.TemplateResponse(
            request,
            "create_monitor.html",
            {"request": request, "error": "Enter a valid name and public URL.", "form": form_data},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    monitor = create_monitor_record(db, payload.name, str(payload.url))
    return RedirectResponse(url=f"/monitors/{monitor.id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/monitors/{monitor_id}/check")
def check_monitor(monitor_id: int, db: Session = Depends(get_db)):
    run_monitor_check(db, monitor_id)
    return RedirectResponse(url=f"/monitors/{monitor_id}", status_code=status.HTTP_303_SEE_OTHER)
