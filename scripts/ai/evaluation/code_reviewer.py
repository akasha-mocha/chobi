from scripts.ai.ai_interface import call_ai
from scripts.utils.logger import log


def review_code(context):

    prompt = f"""
Review the code for bugs, architecture violations, and improvements.

Context:
{context}
"""

    result = call_ai(prompt)

    log("Review completed")

    return result