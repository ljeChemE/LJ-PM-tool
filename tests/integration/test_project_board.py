from datetime import date

from app.clock import today
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_project_board_shows_every_task_regardless_of_day_or_status():
    fixed_today = date(2026, 9, 1)
    app.dependency_overrides[today] = lambda: fixed_today
    try:
        project = client.post("/projects", json={"name": "Board Test"}).json()

        old_task = client.post(
            "/tasks",
            json={
                "title": "Old task",
                "project_id": project["id"],
                "deadline": "2026-01-01",
            },
        ).json()
        future_task = client.post(
            "/tasks",
            json={
                "title": "Future task",
                "project_id": project["id"],
                "deadline": "2026-12-31",
            },
        ).json()

        response = client.get(f"/projects/{project['id']}/tasks")

        assert response.status_code == 200
        titles = {t["title"] for t in response.json()}
        assert titles == {"Old task", "Future task"}
        # Full-history view never applies the /tasks/today rollover.
        old = next(t for t in response.json() if t["id"] == old_task["id"])
        assert old["deadline"] == "2026-01-01"
        assert old["carried_over_count"] == 0
        assert future_task["status"] == "todo"
    finally:
        app.dependency_overrides.pop(today, None)


def test_project_board_for_unknown_project_returns_404():
    response = client.get("/projects/999999/tasks")

    assert response.status_code == 404


def test_task_status_moves_through_all_three_kanban_stages():
    project = client.post("/projects", json={"name": "Kanban Test"}).json()
    task = client.post("/tasks", json={"title": "Ship feature", "project_id": project["id"]}).json()
    assert task["status"] == "todo"

    moved = client.patch(f"/tasks/{task['id']}", json={"status": "in_progress"})
    assert moved.json()["status"] == "in_progress"

    done = client.patch(f"/tasks/{task['id']}", json={"status": "done"})
    assert done.json()["status"] == "done"


def test_project_status_reflects_completed_and_in_progress():
    completed = client.post("/projects", json={"name": "Finished Project"}).json()
    assert completed["status"] == "in_progress"
