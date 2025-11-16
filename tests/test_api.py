
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_crud_notes():
    r = client.post("/notes", json={"title": "Test", "content": "abc"})
    assert r.status_code == 201
    note = r.json()
    note_id = note["id"]

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200

    r = client.put(f"/notes/{note_id}", json={"title": "New", "content": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "New"

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204
