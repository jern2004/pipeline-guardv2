from fastapi import FastAPI

from app.database import Base, engine
from app.models import Incident

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PipelineGuard")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}