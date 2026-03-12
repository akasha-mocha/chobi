import psutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AUTOPILOT_STATE_FILE = ROOT / "runtime" / "autopilot_state.txt"


def _read_ai_status():

    if not AUTOPILOT_STATE_FILE.exists():
        return "unknown"

    try:

        with open(AUTOPILOT_STATE_FILE, encoding="utf8") as f:
            status = f.read().strip()

        if status == "":
            return "unknown"

        return status

    except Exception:
        return "error"


def get_system_status():

    return {

        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "time": int(time.time()),
        "ai_status": _read_ai_status()

    }