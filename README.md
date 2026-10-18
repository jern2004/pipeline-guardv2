# PipelineGuard

PipelineGuard is a small FastAPI incident tracker with a production-style delivery pipeline. The app itself is deliberately simple; the pipeline around it is the point.

Every change goes through linting and tests, gets built into a container image, and is blocked if Trivy finds fixable HIGH or CRITICAL vulnerabilities. It then promotes through dev, staging, and prod on Azure, using Terraform for infrastructure and GitHub OIDC instead of stored secrets, so releases stay controlled and repeatable. A drift watchdog detects and reverts manual infrastructure changes, such as someone opening a network rule in the portal, so the environment stays consistent

**Why:** Writing an API is the easy part. The hard part of running one is everything around it: catching vulnerabilities, preventing drift, and keeping the pipeline reliable.


## Project Roadmap

| Phase | Name | Key Deliverables | Status |
|:-----:|------|------------------|:------:|
| 1 | FastAPI App | Incident CRUD API, SQLAlchemy + SQLite, Pydantic validation, `/healthz`, pytest suite, ruff | ✅ Done |
| 2 | Containerization | Multi-stage Dockerfile, non-root user, `.dockerignore` | 🟡 In progress |
| 3 | Terraform on Azure | Remote state backend, resource group, networking, ACR, dev/staging/prod tfvars | ⬜ Not started |
| 4 | CI/CD Pipeline | GitHub Actions: lint → test → build → Trivy image scan gate → push to ACR | ⬜ Not started |
| 5 | Multi-Environment Promotion | GitHub OIDC to Azure (no stored secrets), Key Vault for secrets, dev → staging → prod promotion | ⬜ Not started |
| 6 | Drift Watchdog | Scheduled drift detection, auto-revert of unauthorised network rule changes, alerting | ⬜ Not started |
| 7 | Kubernetes on AKS | AKS cluster via Terraform, Helm chart / manifests, probes and resource limits | ⬜ Not started |
| 8 | GitOps with Argo CD | Argo CD install, app-of-apps, auto-sync deployments from Git | ⬜ Not started |
| 9 | Observability | Metrics, logs and dashboards (e.g. Prometheus + Grafana), alerts | ⬜ Not started |
| 10 | Multi-Cloud with EKS | EKS cluster via Terraform on AWS, Argo CD deploying to both AKS and EKS | ⬜ Not started |

**Legend:** ⬜ Not started · 🟡 In progress · ✅ Done


## Run it locally

Requires [uv](https://docs.astral.sh/uv/).

```bash
cd app
uv sync
uv run uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs

