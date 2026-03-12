import subprocess


def get_diff():

    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    )

    return result.stdout


def is_safe():

    diff = get_diff()

    lines = diff.splitlines()

    delete_count = sum(1 for l in lines if l.startswith("-"))

    if delete_count > 500:
        return False

    return True