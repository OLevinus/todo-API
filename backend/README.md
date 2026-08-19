# To-Do API

A REST API version of the command-line to-do app, built with FastAPI.

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000/docs** — FastAPI auto-generates an
interactive page where you can try every endpoint from the browser.

## Endpoints

| Method | Path          | Description          |
|--------|---------------|-----------------------|
| GET    | /tasks        | List all tasks        |
| GET    | /tasks/{id}   | Get one task          |
| POST   | /tasks        | Create a task          |
| PUT    | /tasks/{id}   | Update a task          |
| DELETE | /tasks/{id}   | Delete a task          |

## Example requests

```bash
# create a task
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Buy milk"}'

# list tasks
curl http://127.0.0.1:8000/tasks

# mark task 1 done
curl -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d '{"done": true}'

# delete task 1
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## How it's structured

- `models.py` — Pydantic models (data shape + validation) for `Task`,
  `TaskCreate`, `TaskUpdate`.
- `task_manager.py` — same job as in the CLI version: create/read/update/delete
  tasks and persist them to `tasks.json`.
- `main.py` — the FastAPI app. Each route just calls into `TaskManager`.

## Next steps to try on your own

- Add a `PATCH` vs `PUT` distinction (PUT should really replace the whole
  resource; PATCH is for partial updates — right now this API blurs that).
- Add basic error handling for a missing/empty `title` on create.
- Swap `tasks.json` for SQLite once you're comfortable with the above.
