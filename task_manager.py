import json

from models import Task, VALID_PRIORITIES

FILENAME = "tasks.json"


class TaskManager:
    def __init__(self, filename=FILENAME):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                raw = json.load(f)
                return [Task.from_dict(item) for item in raw]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(
                f"Warning: {self.filename} is empty or corrupted. Starting with an empty task list.")
            return []

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def add_tasks(self, raw, default_priority="medium"):
        task_texts = [t.strip() for t in raw.split(",") if t.strip()]
        if not task_texts:
            print("Task can't be empty.")
            return

        existing_lower = {t.text.lower() for t in self.tasks}
        added = []
        skipped = []
        invalid_priorities = []

        for entry in task_texts:
            if ":" in entry:
                text, _, prio_raw = entry.partition(":")
                text = text.strip()
                priority = prio_raw.strip().lower() or default_priority
            else:
                text = entry
                priority = default_priority
            if priority not in VALID_PRIORITIES:
                invalid_priorities.append(
                    f"{text} (invalid priority '{priority}')")
                continue

            if text.lower() in existing_lower:
                skipped.append(text)
                continue

            self.tasks.append(Task(text, priority=priority))
            existing_lower.add(text.lower())
            added.append(text)

        if added:
            self.save_tasks()
            print("Added: " + ", ".join(added))
        if skipped:
            print("Already on the list, skipped: " + ", ".join(skipped))
        if invalid_priorities:
            print("Skipped due to invalid priority: " +
                  ", ".join(invalid_priorities))

    def view_tasks(self, sort_by_priority=False):
        if not self.tasks:
            print("No tasks yet.")
            return

        # enumerate() over the ORIGINAL list order first so numbers stay
        # stable no matter how we choose to display things.
        indexed = list(enumerate(self.tasks, start=1))

        if sort_by_priority:
            order = {"high": 0, "medium": 1, "low": 2}
            indexed = sorted(
                indexed, key=lambda pair: order.get(pair[1].priority, 1))

        for i, task in indexed:
            print(f"{i}. {task}")

    def mark_done(self, task_numbers):
        marked = []
        invalid = []
        for num in task_numbers:
            if 1 <= num <= len(self.tasks):
                self.tasks[num - 1].done = True
                marked.append(self.tasks[num - 1].text)
            else:
                invalid.append(num)

        if marked:
            self.save_tasks()
            print("Marked done: " + ", ".join(marked))
        if invalid:
            print("Invalid task number(s): " + ", ".join(str(n)
                  for n in invalid))

    def delete_tasks(self, task_numbers):
        valid = [n for n in task_numbers if 1 <= n <= len(self.tasks)]
        invalid = [n for n in task_numbers if n not in valid]

        if not valid:
            if invalid:
                print("Invalid task number(s): " + ", ".join(str(n)
                      for n in invalid))
            return

        to_delete_texts = [self.tasks[n - 1].text for n in sorted(valid)]
        print("About to delete: " + ", ".join(to_delete_texts))
        confirm = input("Are you sure? (y/n): ").strip().lower()
        if confirm != "y":
            print("Delete cancelled.")
            return

        removed = []
        for num in sorted(valid, reverse=True):
            removed.append(self.tasks.pop(num - 1).text)

        self.save_tasks()
        print("Deleted: " + ", ".join(reversed(removed)))
        if invalid:
            print("Invalid task number(s): " + ", ".join(str(n)
                  for n in invalid))

    def set_priority(self, task_numbers, priority):
        if priority not in VALID_PRIORITIES:
            print(
                f"Invalid priority '{priority}'. Must be one of: {', '.join(VALID_PRIORITIES)}.")
            return

        updated = []
        invalid = []
        for num in task_numbers:
            if 1 <= num <= len(self.tasks):
                self.tasks[num - 1].priority = priority
                updated.append(self.tasks[num - 1].text)
            else:
                invalid.append(num)

        if updated:
            self.save_tasks()
            print(f"Set priority to '{priority}' for: " + ", ".join(updated))
        if invalid:
            print("Invalid task number(s): " + ", ".join(str(n)
                  for n in invalid))
