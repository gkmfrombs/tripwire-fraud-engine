# TRIPWIRE: Real-Time Fraud Risk Engine

Local, cloud-free MLOps pipeline for transaction fraud detection. See `docs/TRIPWIRE_Blueprint.html`.

## Phase 1 quickstart (object store + Postgres + MLflow)

Requires Docker and Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # Windows: copy .env.example .env  (then edit the secrets)
docker compose up -d --build
docker compose ps                  # mlflow should become "healthy"
python scripts/smoke_test_infra.py # must print PASS
```

- MLflow UI: http://localhost:5000
- Object store S3 API: http://localhost:8333, status UI: http://localhost:9333
- Stop: `docker compose down` (keeps data) or `docker compose down -v` (wipes data)

Design decisions live in `docs/adr/`.
