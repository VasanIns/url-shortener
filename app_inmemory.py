import secrets
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI()
links: dict[str, str] = {}  # in-memory store: lost on restart (on purpose)

class ShortenRequest(BaseModel):
    url: HttpUrl

@app.post("/shorten")
def shorten(req: ShortenRequest):
    code = secrets.token_urlsafe(4)
    links[code] = str(req.url)
    return {"code": code, "short_url": f"/{code}"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/{code}")
def redirect(code: str):
    url = links.get(code)
    if url is None:
        raise HTTPException(status_code=404, detail="not found")
    return RedirectResponse(url, status_code=307)
