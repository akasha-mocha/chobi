from pathlib import Path
import subprocess
import time

BUG_DIR = Path("tickets/bugs")

def find_open_bug():

    for f in BUG_DIR.glob("*.md"):

        text = f.read_text()

        if "Status: open" in text:
            return f, text

    return None, None


def mark_bug(file, status):

    text = file.read_text()

    text = text.replace("Status: open", f"Status: {status}")

    file.write_text(text)


def run_tests():

    result = subprocess.run(
        ["pytest"],
        capture_output=True
    )

    return result.returncode == 0


def fix_bug(bug_text):

    # ここでAI修正（例）
    print("AI fixing bug...")

    time.sleep(2)


def loop():

    while True:

        bug_file, bug_text = find_open_bug()

        if not bug_file:
            time.sleep(10)
            continue

        mark_bug(bug_file, "fixing")

        fix_bug(bug_text)

        if run_tests():

            mark_bug(bug_file, "closed")

        else:

            mark_bug(bug_file, "open")

        time.sleep(3)