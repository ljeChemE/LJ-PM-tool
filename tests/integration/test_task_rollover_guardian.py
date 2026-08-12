"""Guardian suite for the daily-task rollover rule (Testing.md).

This is scheduling logic — the Playbook calls that out by name as needing a
guardian suite, because a silent wrong answer here (a task quietly dropped,
or one that never stops rolling) is expensive in a way a crash isn't.

Standing rule: change `list_todays_tasks`'s rollover behavior in
app/main.py, update this suite in the same change.
"""

from datetime import date

from app.clock import today
from app.main import app
from fastapi.testclient import TestClient


def _client_on(fake_today: date) -> TestClient:
    app.dependency_overrides[today] = lambda: fake_today
    return TestClient(app)


def _make_project(client: TestClient, name: str = "Errands") -> int:
    return client.post("/projects", json={"name": name}).json()["id"]


def test_incomplete_task_rolls_forward_to_todays_standup_until_done():
    day_one, day_two, day_three = date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3)

    try:
        client = _client_on(day_one)
        project_id = _make_project(client)
        task = client.post("/tasks", json={"title": "Buy milk", "project_id": project_id}).json()
        assert task["deadline"] == "2026-01-01"
        assert task["carried_over_count"] == 0

        client = _client_on(day_two)
        todays_tasks = client.get("/tasks/today").json()
        assert [t["id"] for t in todays_tasks] == [task["id"]]
        rolled = todays_tasks[0]
        assert rolled["deadline"] == "2026-01-02"
        assert rolled["carried_over_count"] == 1

        client.patch(f"/tasks/{task['id']}", json={"done": True})

        client = _client_on(day_three)
        assert client.get("/tasks/today").json() == []
    finally:
        app.dependency_overrides.pop(today, None)


def test_task_due_today_does_not_count_as_carried_over():
    """A task landing on today by design isn't the same as one that missed
    its day — carried_over_count must stay 0 either way it got there."""
    day_one = date(2026, 2, 1)

    try:
        client = _client_on(day_one)
        project_id = _make_project(client)
        task = client.post(
            "/tasks",
            json={"title": "Today's task", "project_id": project_id, "deadline": "2026-02-01"},
        ).json()

        todays_tasks = client.get("/tasks/today").json()
        assert [t["id"] for t in todays_tasks] == [task["id"]]
        assert todays_tasks[0]["carried_over_count"] == 0
    finally:
        app.dependency_overrides.pop(today, None)


def test_multiple_overdue_tasks_each_roll_forward_independently():
    day_one, day_two = date(2026, 3, 1), date(2026, 3, 4)

    try:
        client = _client_on(day_one)
        project_id = _make_project(client)
        first = client.post("/tasks", json={"title": "First", "project_id": project_id}).json()
        second = client.post("/tasks", json={"title": "Second", "project_id": project_id}).json()

        client = _client_on(day_two)
        todays_tasks = {t["id"]: t for t in client.get("/tasks/today").json()}
        assert set(todays_tasks) == {first["id"], second["id"]}
        assert all(t["deadline"] == "2026-03-04" for t in todays_tasks.values())
        assert all(t["carried_over_count"] == 1 for t in todays_tasks.values())
    finally:
        app.dependency_overrides.pop(today, None)


def test_future_task_does_not_appear_before_its_deadline():
    day_one, next_week = date(2026, 4, 1), date(2026, 4, 8)

    try:
        client = _client_on(day_one)
        project_id = _make_project(client)
        client.post(
            "/tasks",
            json={
                "title": "Plan trip",
                "project_id": project_id,
                "deadline": next_week.isoformat(),
            },
        )

        assert client.get("/tasks/today").json() == []
    finally:
        app.dependency_overrides.pop(today, None)


def test_done_task_on_a_past_day_never_rolls_forward_even_once():
    day_one, day_two = date(2026, 5, 1), date(2026, 5, 2)

    try:
        client = _client_on(day_one)
        project_id = _make_project(client)
        task = client.post(
            "/tasks", json={"title": "Done already", "project_id": project_id}
        ).json()
        client.patch(f"/tasks/{task['id']}", json={"done": True})

        client = _client_on(day_two)
        assert client.get("/tasks/today").json() == []
    finally:
        app.dependency_overrides.pop(today, None)
