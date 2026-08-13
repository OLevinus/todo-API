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
