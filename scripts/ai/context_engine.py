from pathlib import Path
import re

PROJECT_ROOT = Path(".")


def find_related_files(task_text):

    files = []

    matches = re.findall(r"([\w\/]+\.(py|js|ts|html|css))", task_text)

    for m in matches:

        path = PROJECT_ROOT / m[0]

        if path.exists():
            files.append(path)

    return files


def load_context(files, max_chars=20000):

    context = ""

    for f in files:

        try:

            text = f.read_text()

            context += f"\n\nFILE: {f}\n\n"
            context += text

        except Exception:
            continue

        if len(context) > max_chars:
            break

    return context


def build_context(task_text):

    files = find_related_files(task_text)

    return load_context(files)