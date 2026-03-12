# scripts/tasks/task_state_machine.py

class TaskStateMachine:

    STATES = [
        "PENDING",
        "READY",
        "RUNNING",
        "FAILED",
        "DONE",
        "BLOCKED"
    ]

    TRANSITIONS = {
        "PENDING": ["READY"],
        "READY": ["RUNNING", "BLOCKED"],
        "RUNNING": ["DONE", "FAILED"],
        "FAILED": ["READY"],
        "BLOCKED": ["READY"]
    }

    def can_transition(self, current, new):

        allowed = self.TRANSITIONS.get(current, [])

        return new in allowed

    def transition(self, task, new_state):

        current = task.get("state")

        if not self.can_transition(current, new_state):
            raise Exception(f"Invalid transition {current} -> {new_state}")

        task["state"] = new_state

        return task