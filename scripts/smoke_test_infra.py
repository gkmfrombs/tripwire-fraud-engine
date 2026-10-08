"""Phase 1 acceptance test: proves tracking AND storage are wired together.

1. Logs a run + artifact through the MLflow server (the way training code will).
2. Reads the object store directly and confirms the artifact bytes are really there.
Run from the repo root:  python scripts/smoke_test_infra.py
"""
import os
import sys
import tempfile
from pathlib import Path

import boto3
import mlflow
from botocore.config import Config


def load_env(path: str = ".env") -> None:
    p = Path(path)
    if not p.exists():
        sys.exit("Missing .env. Run: cp .env.example .env  (then edit the secrets)")
    for line in p.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


load_env()
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment("smoke-test")

with mlflow.start_run(run_name="infra-check") as run:
    mlflow.log_param("check", "infra")
    mlflow.log_metric("ok", 1.0)
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "artifact.txt"
        f.write_text("stored via MLflow, kept in the object store")
        mlflow.log_artifact(str(f))

run_id = run.info.run_id
listed = [a.path for a in mlflow.MlflowClient().list_artifacts(run_id)]
assert "artifact.txt" in listed, f"MLflow does not list the artifact: {listed}"

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ.get("S3_ENDPOINT", "http://localhost:8333"),
    aws_access_key_id=os.environ["S3_ACCESS_KEY"],
    aws_secret_access_key=os.environ["S3_SECRET_KEY"],
    region_name="us-east-1",
    config=Config(s3={"addressing_style": "path"}),
)
objs = s3.list_objects_v2(Bucket="mlflow-artifacts", Prefix="").get("Contents", [])
keys = [o["Key"] for o in objs if run_id in o["Key"] and o["Key"].endswith("artifact.txt")]
assert keys, "Artifact not found in the mlflow-artifacts bucket"
print(f"PASS  run={run_id}\n      object store key: {keys[0]}")
