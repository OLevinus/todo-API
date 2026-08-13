from models import VALID_PRIORITIES
from task_manager import TaskManager


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
