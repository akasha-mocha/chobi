import json
from pathlib import Path
from datetime import datetime


STATE_FILE = Path("state/dev_state.json")


class DevStateManager:

    def __init__(self):
        STATE_FILE.parent.mkdir(exist_ok=True)
        if not STATE_FILE.exists():
            self._init_state()

    # -----------------------------
    # 初期化
    # -----------------------------

    def _init_state(self):

        state = {
            "current_cycle": 0,
            "current_task": None,
            "completed_tasks": [],
            "failed_tasks": [],
            "last_build": None,
            "last_test": None,
            "last_bug": None,
            "updated_at": None
        }

        self._save(state)

    # -----------------------------
    # state load/save
    # -----------------------------

    def load(self):

        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, state):

        state["updated_at"] = datetime.utcnow().isoformat()

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    # -----------------------------
    # cycle
    # -----------------------------

    def next_cycle(self):

        state = self.load()
        state["current_cycle"] += 1
        self._save(state)

        return state["current_cycle"]

    # -----------------------------
    # task
    # -----------------------------

    def set_current_task(self, task_id):

        state = self.load()
        state["current_task"] = task_id
        self._save(state)

    def mark_task_complete(self, task_id):

        state = self.load()

        if task_id not in state["completed_tasks"]:
            state["completed_tasks"].append(task_id)

        state["current_task"] = None

        self._save(state)

    def mark_task_failed(self, task_id):

        state = self.load()

        if task_id not in state["failed_tasks"]:
            state["failed_tasks"].append(task_id)

        state["current_task"] = None

        self._save(state)

    # -----------------------------
    # build
    # -----------------------------

    def record_build(self, success, log_path=None):

        state = self.load()

        state["last_build"] = {
            "success": success,
            "log": log_path,
            "time": datetime.utcnow().isoformat()
        }

        self._save(state)

    # -----------------------------
    # test
    # -----------------------------

    def record_test(self, success, log_path=None):

        state = self.load()

        state["last_test"] = {
            "success": success,
            "log": log_path,
            "time": datetime.utcnow().isoformat()
        }

        self._save(state)

    # -----------------------------
    # bug
    # -----------------------------

    def record_bug(self, bug_id):

        state = self.load()

        state["last_bug"] = bug_id

        self._save(state)

    # -----------------------------
    # status
    # -----------------------------

    def summary(self):

        state = self.load()

        return {
            "cycle": state["current_cycle"],
            "current_task": state["current_task"],
            "completed": len(state["completed_tasks"]),
            "failed": len(state["failed_tasks"]),
            "last_build": state["last_build"],
            "last_test": state["last_test"]
        }