import json

FILENAME = "tasks.json"
VALID_PRIORITIES = ("low", "medium", "high")


class Task:
    def __init__(self, text, done=False, priority="medium"):
        self.text = text
        self.done = done
        self.priority = priority

    def to_dict(self):
        return {"text": self.text, "done": self.done, "priority": self.priority}

    @classmethod
    def from_dict(cls, data):
        # .get() with a default handles tasks.json files saved before
        # priority existed, so old data doesn't crash on load.
        return cls(data["text"], data["done"], data.get("priority", "medium"))

    def __repr__(self):
        status = "✓" if self.done else "✗"
        return f"[{status}] ({self.priority}) {self.text}"


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

    def add_tasks(self, raw, priority="medium"):
        if priority not in VALID_PRIORITIES:
            print(
                f"Invalid priority '{priority}'. Must be one of: {', '.join(VALID_PRIORITIES)}.")
            return

        task_texts = [t.strip() for t in raw.split(",") if t.strip()]
        if not task_texts:
            print("Task can't be empty.")
            return

        existing_lower = {t.text.lower() for t in self.tasks}
        added = []
        skipped = []

        for text in task_texts:
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


def print_menu():
    print("\n--- To-Do List ---")
    print("1. View tasks")
    print("2. View tasks (sorted by priority)")
    print("3. Add task")
    print("4. Mark done")
    print("5. Delete task")
    print("6. Set priority")
    print("7. Exit")


def parse_numbers(raw):
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        return None
    numbers = []
    for p in parts:
        if not p.isdigit():
            return None
        numbers.append(int(p))
    return sorted(set(numbers))


def prompt_priority():
    raw = input(
        f"Priority ({'/'.join(VALID_PRIORITIES)}) [medium]: ").strip().lower()
    return raw if raw else "medium"


def main():
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            manager.view_tasks()
        elif choice == "2":
            manager.view_tasks(sort_by_priority=True)
        elif choice == "3":
            raw = input(
                "Enter task(s) (comma-separated for multiple): ").strip()
            priority = prompt_priority()
            manager.add_tasks(raw, priority=priority)
        elif choice == "4":
            manager.view_tasks()
            raw = input("Task number(s) to mark done (e.g. 1,3,5): ").strip()
            numbers = parse_numbers(raw)
            if numbers is None:
                print("Please enter valid number(s), comma-separated.")
            else:
                manager.mark_done(numbers)
        elif choice == "5":
            manager.view_tasks()
            raw = input("Task number(s) to delete (e.g. 1,3,5): ").strip()
            numbers = parse_numbers(raw)
            if numbers is None:
                print("Please enter valid number(s), comma-separated.")
            else:
                manager.delete_tasks(numbers)
        elif choice == "6":
            manager.view_tasks()
            raw = input(
                "Task number(s) to set priority for (e.g. 1,3,5): ").strip()
            numbers = parse_numbers(raw)
            if numbers is None:
                print("Please enter valid number(s), comma-separated.")
            else:
                priority = prompt_priority()
                manager.set_priority(numbers, priority)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
