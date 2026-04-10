# AI Change Monitor

Minimal local MVP for tracking text changes on public web pages with manual checks.

## Stack

- Python 3.9+ compatible
- FastAPI
- Jinja2
- SQLite
- SQLAlchemy
- pytest

## Features

- Dashboard of monitors
- Create monitor form
- Monitor detail page
- Manual "Check now" action
- Visible text extraction from HTML
- Text normalization and snapshot comparison
- Readable diff text
- Simple rule-based change summary

## Run locally

1. Create a local virtual environment:

   ```powershell
   py -3.12 -m venv .venv
   ```

   If Python 3.12 is not available on your machine, use any local Python 3.9+ interpreter instead:

   ```powershell
   py -3.9 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Start the app:

   ```powershell
   & .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Notes

- No authentication
- No billing
- No background jobs
- Manual checks only
- Uses Python standard library fetching and HTML parsing for simple public pages
