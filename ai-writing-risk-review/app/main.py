from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .db import SessionLocal, init_db
from .models import Review
from .risk_engine import score_text


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="AI Writing Risk Review")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def read_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "result": None,
            "text": "",
        },
    )


@app.post("/review", response_class=HTMLResponse)
def review_text(
    request: Request,
    text: str = Form(...),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    result = score_text(text)
    review = Review(submitted_text=text, score=result["score"], level=result["level"])
    db.add(review)
    db.commit()
    db.refresh(review)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "result": result,
            "text": text,
            "review_id": review.id,
        },
    )
