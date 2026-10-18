from typing import Any

from fastapi.testclient import TestClient


def create_incident(client: TestClient, **fields: Any) -> dict[str, Any]:
    payload = {"title": "Login page down", "severity": "high"} | fields
    response = client.post("/incidents", json=payload)
    assert response.status_code == 201
    return response.json()


def test_healthz(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_incident_fills_in_defaults(client: TestClient) -> None:
    incident = create_incident(client)
    assert incident["id"] == 1
    assert incident["title"] == "Login page down"
    assert incident["description"] is None
    assert incident["status"] == "open"
    assert incident["created_at"] is not None
    assert incident["resolved_at"] is None


def test_create_rejects_invalid_severity(client: TestClient) -> None:
    response = client.post("/incidents", json={"title": "Test", "severity": "banana"})
    assert response.status_code == 422


def test_create_rejects_missing_title(client: TestClient) -> None:
    response = client.post("/incidents", json={"severity": "high"})
    assert response.status_code == 422


def test_create_rejects_empty_title(client: TestClient) -> None:
    response = client.post("/incidents", json={"title": "", "severity": "high"})
    assert response.status_code == 422


def test_list_incidents(client: TestClient) -> None:
    create_incident(client, title="First")
    create_incident(client, title="Second")
    response = client.get("/incidents")
    assert response.status_code == 200
    assert [incident["title"] for incident in response.json()] == ["First", "Second"]


def test_get_incident(client: TestClient) -> None:
    created = create_incident(client)
    response = client.get(f"/incidents/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_incident_returns_404(client: TestClient) -> None:
    response = client.get("/incidents/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Incident not found"}


def test_resolving_sets_resolved_at(client: TestClient) -> None:
    created = create_incident(client)
    response = client.patch(f"/incidents/{created['id']}", json={"status": "resolved"})
    assert response.status_code == 200
    assert response.json()["status"] == "resolved"
    assert response.json()["resolved_at"] is not None


def test_reopening_clears_resolved_at(client: TestClient) -> None:
    created = create_incident(client)
    client.patch(f"/incidents/{created['id']}", json={"status": "resolved"})
    response = client.patch(f"/incidents/{created['id']}", json={"status": "open"})
    assert response.status_code == 200
    assert response.json()["resolved_at"] is None


def test_partial_update_keeps_other_fields(client: TestClient) -> None:
    created = create_incident(client, title="Slow search", severity="low")
    response = client.patch(
        f"/incidents/{created['id']}", json={"severity": "critical"}
    )
    assert response.status_code == 200
    assert response.json()["severity"] == "critical"
    assert response.json()["title"] == "Slow search"


def test_delete_incident(client: TestClient) -> None:
    created = create_incident(client)
    response = client.delete(f"/incidents/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/incidents/{created['id']}").status_code == 404
