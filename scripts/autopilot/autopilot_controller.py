import time
from pathlib import Path

from scripts.autopilot.task_execution_engine import run_next_task
from scripts.utils.logger import get_logger

ROOT = Path(__file__).resolve().parents[2]

STATE_FILE = ROOT / "runtime" / "autopilot_state.txt"
COMMAND_FILE = ROOT / "runtime" / "autopilot_command.txt"

logger = get_logger("autopilot")

state = "stopped"


def read_command():

    if not COMMAND_FILE.exists():
        return None

    cmd = COMMAND_FILE.read_text().strip()
    COMMAND_FILE.unlink(missing_ok=True)

    return cmd


def write_state(s):

    global state
    state = s

    STATE_FILE.parent.mkdir(exist_ok=True)

    with open(STATE_FILE, "w") as f:
        f.write(s)


def autopilot_loop():

    write_state("idle")

    while True:

        cmd = read_command()

        if cmd == "start":
            write_state("running")

        if cmd == "stop":
            write_state("stopped")

        if cmd == "pause":
            write_state("paused")

        if state == "running":

            try:
                run_next_task()
            except Exception as e:
                logger.error(f"autopilot error {e}")

        time.sleep(3)