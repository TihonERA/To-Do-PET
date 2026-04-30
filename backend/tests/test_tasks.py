import pytest
from datetime import datetime, timezone, timedelta

def test_create_task(client, auth_headers):
    future_date = datetime.now() + timedelta(days=1)
    body = {
        "name": "Make tests",
        "description": "Make a lot of tests Make a lot of tests Make a lot of tests Make a lot of tests",
        "priority": 2,
        "due_date": future_date.isoformat()
    }
    response = client.post("/tasks/create_task", json=body, headers=auth_headers)
    assert response.status_code == 200

def test_get_tasks(client, auth_headers):
    body2 = {
        "name": "Make tests Make tests",
        "description": "Make a lot of tests Make a lot of tests Make a lot of tests Make a lot of tests",
        "priority": 2,
    }
    body3 = {
        "name": "Make tests Make tests Make tests",
        "description": "Make a lot of tests Make a lot of tests Make a lot of tests Make a lot of tests",
        "priority": 2,
    }
    client.post("/tasks/create_task", json=body2, headers=auth_headers)
    client.post("/tasks/create_task", json=body3, headers=auth_headers)
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_get_task(client, auth_headers):
    response = client.get(f"/tasks/{1}", headers=auth_headers)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.json()}")  # Увидите детали 422 ошибки
    assert response.status_code == 200

def test_update_description(client, auth_headers):
    future_date = datetime.now() + timedelta(days=1)
    body = {
        "new_name": "change_description_test",
        "new_description": "helloeverynyan helloeverynyan  helloeverynyan  helloeverynyan  helloeverynyan",
        "new_due_date": future_date.isoformat(),
        "set_completed": True,
        "switch_status": True
    }

    response = client.patch("/tasks/1/update_task", json=body, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "change_description_test"
    assert response.json()["description"] == "helloeverynyan helloeverynyan  helloeverynyan  helloeverynyan  helloeverynyan".strip()

def test_delete_task(client, auth_headers):
    response = client.delete(f"/tasks/{2}/delete", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Task deleted"
