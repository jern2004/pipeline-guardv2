# PipelineGuard

A small incident-tracker API, built as a DevOps portfolio project. The app is deliberately simple; the project's focus is the delivery pipeline, infrastructure as code and drift detection being built around it.

## Status

Phase 1 of 10, in progress: the FastAPI app, running locally against SQLite.

## What exists now

- FastAPI app with a `/healthz` health check
- `POST /incidents` to create an incident, with request validation (Pydantic)
- SQLAlchemy model for incidents, stored in SQLite locally
- Interactive API docs at `/docs`

## Run it locally

Requires [uv](https://docs.astral.sh/uv/).

```bash
cd app
uv sync
uv run uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs

## Tech

Python, FastAPI, SQLAlchemy, Pydantic, uv

## Roadmap

Planned, not yet built:

1. Docker image (multi-stage, non-root)
2. Terraform-managed Azure infrastructure
3. GitHub Actions CI/CD with Trivy image scanning
4. Multi-environment promotion with OIDC and Key Vault
5. Drift watchdog that detects and reverts unauthorised network rule changes
6. Kubernetes, GitOps with Argo CD, observability, AKS and EKS