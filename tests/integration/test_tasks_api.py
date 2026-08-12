from datetime import date

from app.clock import today
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_task_defaults_deadline_to_today():
    fixed_today = date(2026, 6, 15)
    app.dependency_overrides[today] = lambda: fixed_today
    try:
        project = client.post("/projects", json={"name": "Home"}).json()

        response = client.post(
            "/tasks", json={"title": "Water plants", "project_id": project["id"]}
        )

        assert response.status_code == 201
        body = response.json()
        assert body["deadline"] == "2026-06-15"
        assert body["status"] == "todo"
        assert body["carried_over_count"] == 0
    finally:
        app.dependency_overrides.pop(today, None)


def test_create_task_for_unknown_project_returns_404():
    response = client.post("/tasks", json={"title": "Orphan task", "project_id": 999999})

    assert response.status_code == 404


def test_patch_marks_task_done():
    project = client.post("/projects", json={"name": "Work"}).json()
    task = client.post(
        "/tasks",
        json={"title": "Write report", "project_id": project["id"], "deadline": "2026-07-01"},
    ).json()

    response = client.patch(f"/tasks/{task['id']}", json={"status": "done"})

    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_list_tasks_for_a_specific_day():
    project = client.post("/projects", json={"name": "Trip"}).json()
    client.post(
        "/tasks",
        json={"title": "Pack bags", "project_id": project["id"], "deadline": "2026-08-01"},
    )

    response = client.get("/tasks", params={"day": "2026-08-01"})

    assert response.status_code == 200
    titles = [t["title"] for t in response.json()]
    assert titles == ["Pack bags"]
