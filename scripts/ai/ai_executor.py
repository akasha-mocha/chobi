from pathlib import Path
import subprocess

from scripts.utils.logger import get_logger

logger = get_logger("ai_executor")


def run_ai_task(task_file):

    prompt = task_file.read_text()

    logger.info("execute ai task")

    # 例：Cursor CLI / Claude CLIなど
    subprocess.run(
        [
            "cursor",
            "--prompt",
            prompt
        ]
    )