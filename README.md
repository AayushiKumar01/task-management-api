# Task Management API

A RESTful task management service built with **Python, FastAPI, PostgreSQL, and SQLAlchemy**. The project demonstrates backend API development, relational database integration, schema migrations, request validation, and automated integration testing.

## Features

- Create, retrieve, update, and delete tasks
- Filter tasks by completion status
- Offset-based pagination
- Request and response validation using Pydantic
- PostgreSQL persistence with SQLAlchemy ORM
- Database schema migrations with Alembic
- Automated API integration tests using pytest
- Interactive API documentation using Swagger UI
- Docker Compose for local PostgreSQL setup

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.13 |
| Web Framework | FastAPI |
| Database | PostgreSQL 17 |
| ORM | SQLAlchemy 2 |
| Migrations | Alembic |
| Validation | Pydantic 2 |
| Testing | pytest, HTTPX |
| Infrastructure | Docker Compose |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/v1/tasks` | Create a task |
| GET | `/api/v1/tasks` | List tasks with pagination and filtering |
| GET | `/api/v1/tasks/{task_id}` | Retrieve a task |
| PATCH | `/api/v1/tasks/{task_id}` | Partially update a task |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task |

### Example: Create a Task

**Request**

`POST /api/v1/tasks`

```json
{
  "title": "Learn FastAPI",
  "description": "Build a REST API with PostgreSQL",
  "is_completed": false
}
```

**Response — 201 Created**

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Build a REST API with PostgreSQL",
  "is_completed": false,
  "created_at": "2026-11-03T20:00:00Z",
  "updated_at": "2026-11-03T20:00:00Z"
}
```

### Filtering and Pagination

Retrieve completed tasks:

`GET /api/v1/tasks?is_completed=true`

Retrieve the second page of 10 tasks:

`GET /api/v1/tasks?skip=10&limit=10`

Pagination supports a maximum page size of 100 records.

## Getting Started

### Prerequisites

- Python 3.13
- Docker Desktop with Docker Compose
- Git

### 1. Clone the Repository

```powershell
git clone <repository-url>
cd task-management-api
```

Replace `<repository-url>` with the GitHub repository URL.

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

```powershell
Copy-Item .env.example .env
```

The example configuration uses the local PostgreSQL credentials defined in `compose.yaml`. Change credentials for any non-local deployment.

### 5. Start PostgreSQL

```powershell
docker compose up -d
```

### 6. Apply Database Migrations

```powershell
python -m alembic upgrade head
```

### 7. Start the API

```powershell
python -m uvicorn app.main:app --reload
```

The API is available at:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI specification: http://127.0.0.1:8000/openapi.json

## Running Tests

Create a separate PostgreSQL test database:

```powershell
docker compose exec db psql -U taskuser -d taskdb -c "CREATE DATABASE taskdb_test;"
```

Run the automated tests:

```powershell
python -m pytest -v
```

The database-backed tests use `taskdb_test`, not the development database. The test fixture creates and drops test tables automatically.

**Warning:** The test fixture drops tables in the configured test database. Never point it at a database containing important data.

## Project Structure

```text
task-management-api/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   └── test_tasks.py
├── .env.example
├── .gitignore
├── alembic.ini
├── compose.yaml
├── requirements.txt
└── README.md
```

## Architecture

The application uses a simple layered design:

**HTTP Request → FastAPI Endpoint → Pydantic Validation → SQLAlchemy ORM → PostgreSQL**

FastAPI handles HTTP routing and dependency injection. Pydantic validates API input and output. SQLAlchemy manages database operations and transactions, while Alembic tracks schema changes.

The API uses a database session per request and returns appropriate HTTP status codes for successful operations, validation failures, and missing resources.

