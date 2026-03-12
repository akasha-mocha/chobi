import re
from pathlib import Path

from dashboard.services.cache_utils import TimedCache

ROOT = Path(__file__).resolve().parents[2]
BUG_DIR = ROOT / "tickets/bugs"

_cache = TimedCache(ttl=3)


def parse_bug_md(text: str):

    bug = {
        "id": "",
        "title": "",
        "status": "",
        "priority": ""
    }

    id_match = re.search(r"^ID:\s*(.*)", text, re.MULTILINE | re.IGNORECASE)
    if id_match:
        bug["id"] = id_match.group(1).strip()

    title_match = re.search(r"^Title:\s*(.*)", text, re.MULTILINE | re.IGNORECASE)
    if title_match:
        bug["title"] = title_match.group(1).strip()

    status_match = re.search(r"^Status:\s*(.*)", text, re.MULTILINE | re.IGNORECASE)
    if status_match:
        bug["status"] = status_match.group(1).strip()

    priority_match = re.search(r"^Priority:\s*(.*)", text, re.MULTILINE | re.IGNORECASE)
    if priority_match:
        bug["priority"] = priority_match.group(1).strip()

    return bug


def _load_bugs():

    bugs = []

    if not BUG_DIR.exists():
        return bugs

    for f in BUG_DIR.glob("*.md"):

        try:

            with open(f, encoding="utf8") as fp:
                text = fp.read()

            bug = parse_bug_md(text)

            bugs.append(bug)

        except Exception:
            continue

    return bugs


def get_bugs():
    return _cache.get(_load_bugs)