from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RUNTIME_DIR = ROOT / "runtime"

STATE_FILE = RUNTIME_DIR / "autopilot_state.txt"
COMMAND_FILE = RUNTIME_DIR / "autopilot_command.txt"


def _write_command(cmd: str):

    RUNTIME_DIR.mkdir(exist_ok=True)

    with open(COMMAND_FILE, "w", encoding="utf8") as f:
        f.write(cmd)


def start_ai():

    _write_command("start")

    return {
        "result": "ok",
        "command": "start"
    }


def stop_ai():

    _write_command("stop")

    return {
        "result": "ok",
        "command": "stop"
    }


def pause_ai():

    _write_command("pause")

    return {
        "result": "ok",
        "command": "pause"
    }


def get_ai_status():

    if not STATE_FILE.exists():
        return {"status": "unknown"}

    try:

        with open(STATE_FILE, encoding="utf8") as f:
            status = f.read().strip()

        if status == "":
            status = "unknown"

        return {"status": status}

    except Exception:

        return {"status": "error"}