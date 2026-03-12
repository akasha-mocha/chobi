from scripts.ai.ai_interface import call_ai
from scripts.utils.logger import log


def generate_code(task, context):

    prompt = f"""
You are a senior developer.

Implement the following task.

Task
{task}

Project context
{context}

Return only code.
"""

    result = call_ai(prompt)

    log("AI code generated")

    return result


def generate_file(task, context):

    code = generate_code(task, context)

    file_path = task.get("target_file")

    if not file_path:
        return

    with open(file_path, "w", encoding="utf-8") as f:

        f.write(code)

    log(f"File written {file_path}")