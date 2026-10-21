# url-shortener

A minimal URL shortener I built to practice operating a service end to end:
deploy it, break it, write the postmortem, fix it, and verify the fix.

## Stack

- Python 3.13, FastAPI, uvicorn
- PostgreSQL 17 in Docker, with a named volume for persistence
- Runs on dev-01 in my Proxmox homelab; Docker installed via my
  [homelab-ansible](https://github.com/VasanIns/homelab-ansible) role

## Run it locally

    docker volume create shortener-pgdata
    docker run -d --name shortener-db \
      -e POSTGRES_USER=shortener -e POSTGRES_PASSWORD=devpassword \
      -e POSTGRES_DB=shortener \
      -v shortener-pgdata:/var/lib/postgresql/data \
      -p 127.0.0.1:5432:5432 --restart unless-stopped postgres:17
    docker exec -i shortener-db psql -U shortener -d shortener < schema.sql

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    export DATABASE_URL="postgresql://shortener:devpassword@127.0.0.1:5432/shortener"
    uvicorn app:app --host 0.0.0.0 --port 8000

## API

- `POST /shorten` with `{"url": "https://example.com"}` returns a short code
- `GET /{code}` redirects (307) to the original URL, or returns 404
- `GET /healthz` is a liveness check

## Incidents

- [001: Restart data loss](postmortems/001-restart-data-loss.md): the
  in-memory version lost every link on restart. Fixed by moving storage to
  Postgres; verified across app and database restarts.

## Roadmap

- Container image and deployment to my k3s cluster
- Prometheus metrics and an SLO on redirect success rate
- Readiness check that includes the database
- Connection pooling
