# ADR 0001: SeaweedFS instead of MinIO as the local S3 store

- Status: accepted
- Date: 2026-10-08

## Context
The original design used MinIO. Research in Oct 2026 shows the MinIO community edition is no longer
viable for new work: the admin console was stripped (2025), official Docker images and binaries stopped
(Oct 2025), and the repositories were archived (server Apr 2026, `mc` client Jul 2026). Unpatched images
mean known CVEs cannot be fixed by pulling an update.

## Decision
Use SeaweedFS (Apache-2.0, actively released) as the S3-compatible store. Everything else talks plain S3
(MLflow via boto3, DVC via `dvc-s3`), so the store is replaceable by changing one endpoint URL.
Bucket creation uses the standard AWS CLI instead of the archived `mc`.

## Consequences
- No change to MLflow, DVC or Feast configuration beyond the endpoint and credentials.
- SeaweedFS `mini` mode is for development; a production deployment would run the distributed mode.
- MLflow runs with proxied artifact access: training and serving containers never hold storage keys.
