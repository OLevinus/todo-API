# To-Do API

A full-stack to-do list application with a **FastAPI** backend and a **Flask** frontend that talks to it over HTTP — mirroring how a real browser-based frontend communicates with a separate backend service in production.

## Features

- Create, view, update, and delete tasks
- Mark tasks as done / not done
- Assign a priority to each task
- Data persisted between sessions
- Clean separation between backend (API) and frontend (UI) — the Flask app has no direct access to the data, it only calls the API

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic
- **Frontend:** Python, Flask, Jinja2 templates
- **Communication:** REST over HTTP (`requests` library)

## Project Structure

```
todo-API/
├── backend/          # FastAPI app
│   ├── main.py
│   ├── models.py
│   ├── task_manager.py
│   └── requirements.txt
├── frontend/          # Flask app
│   ├── app.py
│   ├── templates/
│   ├── static/
│   └── requirements.txt
└── .gitignore
```

## Getting Started

### 1. Run the backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.
Interactive API docs are available at `http://127.0.0.1:8000/docs`.

### 2. Run the frontend (Flask)

In a **separate terminal**:

```bash
cd frontend
pip install -r requirements.txt
python app.py
```

The web app will be running at `http://127.0.0.1:5000`.

> The backend must be running before the frontend, or the frontend will show a "could not reach the API" message.

## API Endpoints

| Method | Endpoint          | Description              |
|--------|-------------------|---------------------------|
| GET    | `/tasks`          | List all tasks            |
| GET    | `/tasks/{id}`     | Get a single task         |
| POST   | `/tasks`          | Create a new task         |
| PUT    | `/tasks/{id}`     | Update a task's title, status, or priority |
| DELETE | `/tasks/{id}`     | Delete a task              |

## What I Learned

- Building a REST API with FastAPI, including request validation with Pydantic models
- Structuring a project with a decoupled backend/frontend, similar to real-world client-server architecture
- Using `requests` to consume an API from a server-rendered Flask app
- Git workflow: branching, staging, committing, and reorganizing a project's structure over time
