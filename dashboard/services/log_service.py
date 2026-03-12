from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LOG_FILE = ROOT / "runtime/logs/dev.log"


def tail_lines(path, n=200):

    if not path.exists():
        return []

    with open(path, encoding="utf8") as f:
        lines = f.readlines()

    return lines[-n:]


def get_logs():

    return {
        "lines": tail_lines(LOG_FILE, 200)
    }