"""
Flask front-end for the to-do app.

This app has NO direct access to the task data — it only talks to your
FastAPI backend over HTTP, the same way a real browser-based frontend
would talk to a separate backend service in production.

Run your FastAPI backend first (assumed at http://127.0.0.1:8000),
then run this app:
    python app.py
Visit http://127.0.0.1:5000
"""

import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-this"  # needed for flash messages

# Change this if your FastAPI app runs on a different host/port
API_BASE_URL = "http://127.0.0.1:8000"


@app.route("/")
def index():
    try:
        response = requests.get(f"{API_BASE_URL}/tasks")
        response.raise_for_status()
        tasks = response.json()
    except requests.exceptions.RequestException:
        flash("Could not reach the API. Is the FastAPI server running?")
        tasks = []
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    if title:
        try:
            requests.post(f"{API_BASE_URL}/tasks", json={"title": title})
        except requests.exceptions.RequestException:
            flash("Could not reach the API. Is the FastAPI server running?")
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    try:
        # fetch current state so we know what to flip
        current = requests.get(f"{API_BASE_URL}/tasks/{task_id}").json()
        requests.put(
            f"{API_BASE_URL}/tasks/{task_id}",
            json={"done": not current.get("done", False)},
        )
    except requests.exceptions.RequestException:
        flash("Could not reach the API. Is the FastAPI server running?")
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    try:
        requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    except requests.exceptions.RequestException:
        flash("Could not reach the API. Is the FastAPI server running?")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
