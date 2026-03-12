import re


def _replace_status(text, new_status):

    return re.sub(
        r"Status:\s*\w+",
        f"Status: {new_status}",
        text
    )


def set_task_doing(task_file):

    text = task_file.read_text()

    text = _replace_status(text, "doing")

    task_file.write_text(text)


def set_task_done(task_file):

    text = task_file.read_text()

    text = _replace_status(text, "done")

    task_file.write_text(text)