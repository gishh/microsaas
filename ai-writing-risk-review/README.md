# AI Writing Risk Review

This MVP reviews persuasive writing for simple risk signals such as urgency, manipulative phrasing, and exaggerated guarantees. It uses FastAPI for the web app, Jinja2 for rendering, SQLite for storage, and SQLAlchemy for persistence.

## Features

- Submit writing through a small web form
- Score the text with a lightweight risk engine
- Store each review in SQLite
- Run a basic pytest test for the scoring logic

## Local setup

1. Create and activate a Python 3.12 virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the app from the `ai-writing-risk-review` directory:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Open `http://127.0.0.1:8000`.

## Project layout

- `app/main.py` exposes the FastAPI application and routes
- `app/risk_engine.py` contains the scoring logic
- `app/db.py` and `app/models.py` handle the SQLite setup
- `tests/test_review.py` includes a real pytest test

## Docker

Build and run with Docker:

```bash
docker build -t ai-writing-risk-review .
docker run --rm -p 8000:8000 ai-writing-risk-review
```
