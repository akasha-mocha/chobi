from pathlib import Path

SRC_DIR = Path("src")
DOCS_DIR = Path("docs")

MAX_FILE_SIZE = 20000


def read_file_safe(path):
    try:
        text = path.read_text(encoding="utf-8")

        if len(text) > MAX_FILE_SIZE:
            text = text[:MAX_FILE_SIZE]

        return text

    except Exception:
        return ""


def collect_source_files():

    files = []

    if not SRC_DIR.exists():
        return files

    for f in SRC_DIR.rglob("*"):

        if f.suffix in [".ts", ".js", ".json", ".tsx"]:
            files.append(f)

    return files


def collect_docs():

    files = []

    if not DOCS_DIR.exists():
        return files

    for f in DOCS_DIR.glob("*.md"):
        files.append(f)

    return files


def build_context(task_file):

    context = []

    context.append("=== TASK ===\n")
    context.append(read_file_safe(task_file))

    context.append("\n=== ARCHITECTURE ===\n")

    arch = DOCS_DIR / "architecture.md"

    if arch.exists():
        context.append(read_file_safe(arch))

    context.append("\n=== SOURCE CODE ===\n")

    for src in collect_source_files():

        context.append(f"\n--- FILE: {src} ---\n")
        context.append(read_file_safe(src))

    return "\n".join(context)


def save_context(task_file):

    ctx = build_context(task_file)

    out = Path("tmp/context.txt")

    out.parent.mkdir(exist_ok=True)

    out.write_text(ctx, encoding="utf-8")

    return out