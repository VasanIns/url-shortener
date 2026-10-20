import os
import secrets

import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

DATABASE_URL = os.environ["DATABASE_URL"]  # fail fast if not set

app = FastAPI()


class ShortenRequest(BaseModel):
    url: HttpUrl


@app.post("/shorten")
def shorten(req: ShortenRequest):
    code = secrets.token_urlsafe(4)
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(
            "INSERT INTO links (code, url) VALUES (%s, %s)",
            (code, str(req.url)),
        )
    return {"code": code, "short_url": f"/{code}"}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/{code}")
def redirect(code: str):
    with psycopg.connect(DATABASE_URL) as conn:
        row = conn.execute(
            "SELECT url FROM links WHERE code = %s", (code,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    return RedirectResponse(row[0], status_code=307)
