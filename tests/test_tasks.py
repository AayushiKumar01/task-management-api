import pytest

def test_create_task(client):
    payload = {
        "title": "Learn pytest",
        "description": "Write automated API tests",
        "is_completed": False,
    }

    response = client.post("/api/v1/tasks", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["is_completed"] is False
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

    get_response = client.get(f"/api/v1/tasks/{data['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Learn pytest"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"description": "Missing title"},
        {"title": ""},
        {"title": "x" * 201},
    ],
)
def test_create_task_invalid_input(client, payload):
    response = client.post("/api/v1/tasks", json=payload)

    assert response.status_code == 422


def test_get_nonexistent_task(client):
    response = client.get("/api/v1/tasks/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task with ID 9999 not found"



def test_list_tasks_filtering_and_pagination(client):
    tasks = [
        {"title": "Task A", "is_completed": False},
        {"title": "Task B", "is_completed": True},
        {"title": "Task C", "is_completed": False},
        {"title": "Task D", "is_completed": True},
    ]

    for task in tasks:
        response = client.post("/api/v1/tasks", json=task)
        assert response.status_code == 201

    # Retrieve all tasks
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 4

    # Filter completed tasks
    response = client.get("/api/v1/tasks?is_completed=true")
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == [
        "Task B",
        "Task D",
    ]

    # Filter incomplete tasks
    response = client.get("/api/v1/tasks?is_completed=false")
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == [
        "Task A",
        "Task C",
    ]

    # Test pagination
    response = client.get("/api/v1/tasks?skip=1&limit=2")
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == [
        "Task B",
        "Task C",
    ]


def test_update_task(client):
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Original description",
            "is_completed": False,
        },
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Update only the completion status
    update_response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"is_completed": True},
    )

    assert update_response.status_code == 200

    updated_task = update_response.json()

    assert updated_task["is_completed"] is True
    assert updated_task["title"] == "Learn FastAPI"
    assert updated_task["description"] == "Original description"

    # Verify the update persisted
    get_response = client.get(f"/api/v1/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json()["is_completed"] is True


def test_delete_task(client):
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Temporary task"},
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Delete the task
    delete_response = client.delete(
        f"/api/v1/tasks/{task_id}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    # Verify the task no longer exists
    get_response = client.get(f"/api/v1/tasks/{task_id}")

    assert get_response.status_code == 404


def test_create_task_whitespace_title(client):
    response = client.post(
        "/api/v1/tasks",
        json={"title": "   "},
    )

    assert response.status_code == 422


def test_update_task_whitespace_title(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Valid title"},
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "   "},
    )

    assert response.status_code == 422


