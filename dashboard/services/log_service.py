from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LOG_FILE = ROOT / "runtime" / "autopilot.log"


def get_logs():

    if not LOG_FILE.exists():
        return {"logs": []}

    try:

        with open(LOG_FILE, encoding="utf8") as f:
            lines = f.readlines()

        # last 50 rows
        lines = lines[-50:]

        return {
            "logs": [l.strip() for l in lines]
        }

    except Exception:

        return {"logs": []}