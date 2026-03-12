import json
from pathlib import Path

from scripts.ai.ai_interface import call_ai
from scripts.utils.logger import get_logger

logger = get_logger(__name__)

ROOT = Path(__file__).resolve().parents[2]

BUG_DIR = ROOT / "tickets/bugs"


class ResearchAgent:

    def __init__(self):
        pass

    # -----------------------------------------

    def load_bug(self, bug_id):

        path = BUG_DIR / f"{bug_id}.json"

        if not path.exists():
            return None

        with open(path, encoding="utf8") as f:
            return json.load(f)

    # -----------------------------------------

    def extract_error(self, bug):

        if not bug:
            return ""

        return bug.get("error", "")

    # -----------------------------------------

    def build_prompt(self, error):

        return f"""
You are a senior software engineer.

Analyze this error and propose possible fixes.

Error:
{error}

Output:
- root cause
- fix strategy
- example code fix
"""

    # -----------------------------------------

    def research(self, bug_id):

        bug = self.load_bug(bug_id)

        if not bug:
            return None

        error = self.extract_error(bug)

        prompt = self.build_prompt(error)

        logger.info("Researching bug")

        result = call_ai(prompt)

        return {
            "bug": bug_id,
            "analysis": result
        }