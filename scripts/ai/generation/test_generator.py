import json

from scripts.ai.ai_context_engine import build_context
from scripts.ai.ai_interface import run
from scripts.utils.logger import log


def generate_tests(task):

    context = build_context(task)

    prompt = f"""
Generate unit tests for the following implementation task.

Task:
{json.dumps(task, indent=2)}

Context:
{context}

Requirements:
- Use appropriate testing framework
- Cover edge cases
- Do not modify production code
"""

    result = run(["codex", "generate-tests", prompt])

    log(result)

    return result