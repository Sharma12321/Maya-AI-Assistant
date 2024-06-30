class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        return f"Added '{task}' to your to-do list."

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            return f"Removed '{task}' from your to-do list."
        return f"'{task}' was not found in your to-do list."

    def list_tasks(self):
        if not self.tasks:
            return "Your to-do list is empty."
        return "Your to-do list:\n" + "\n".join(f"- {task}" for task in self.tasks)