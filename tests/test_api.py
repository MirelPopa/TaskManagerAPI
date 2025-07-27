from fastapi.testclient import TestClient

from api.db import SessionLocal
from api.main import get_db, router


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router.dependency_overrides[get_db] = override_get_db

test_client = TestClient(router)


def test_create_task(db_session, clear_db):
    response = test_client.post(
        "/tasks", json={"title": "Test Task", "description": "Details"}
    )
    assert response.status_code == 200
    assert "id" in response.json()


def test_create_task_without_title(clear_db):
    response = test_client.post("/tasks", json={"description": "No title here"})
    assert response.status_code == 422


def test_duplicate_title(clear_db):
    task = {"title": "Unique Title", "description": "first"}
    test_client.post("/tasks", json=task)
    response2 = test_client.post("/tasks", json=task)
    assert response2.status_code != 200


def test_get_tasks_returns_list(clear_db):
    response = test_client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_tasks_insertion(clear_db):
    task_1 = {"title": "1", "description": "sample"}
    task_2 = {"title": "2", "description": "sample abc"}
    task_3 = {"title": "3"}
    task_4 = {"title": "4", "description": "sample 4"}
    task_5 = {"title": "5", "description": "sample 5"}
    test_client.post("/tasks", json=task_1)
    test_client.post("/tasks", json=task_2)
    test_client.post("/tasks", json=task_3)
    test_client.post("/tasks", json=task_4)
    test_client.post("/tasks", json=task_5)
    response = test_client.get("/tasks")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 5
