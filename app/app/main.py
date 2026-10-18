from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Incident
from app.schemas import IncidentCreate, IncidentRead, IncidentUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PipelineGuard")


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


def get_incident_or_404(db: Session, incident_id: int) -> Incident:
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/incidents", response_model=IncidentRead, status_code=201)
def create_incident(payload: IncidentCreate, db: DbSession) -> Incident:
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@app.get("/incidents", response_model=list[IncidentRead])
def list_incidents(db: DbSession) -> list[Incident]:
    return list(db.scalars(select(Incident).order_by(Incident.id)).all())


@app.get("/incidents/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id: int, db: DbSession) -> Incident:
    return get_incident_or_404(db, incident_id)


@app.patch("/incidents/{incident_id}", response_model=IncidentRead)
def update_incident(
    incident_id: int, payload: IncidentUpdate, db: DbSession
) -> Incident:
    incident = get_incident_or_404(db, incident_id)
    changes = payload.model_dump(exclude_none=True)
    for field, value in changes.items():
        setattr(incident, field, value)

    if "status" in changes:
        if changes["status"] == "resolved" and incident.resolved_at is None:
            incident.resolved_at = datetime.now(UTC)
        elif changes["status"] != "resolved":
            incident.resolved_at = None

    db.commit()
    db.refresh(incident)
    return incident


@app.delete("/incidents/{incident_id}", status_code=204)
def delete_incident(incident_id: int, db: DbSession) -> None:
    incident = get_incident_or_404(db, incident_id)
    db.delete(incident)
    db.commit()
