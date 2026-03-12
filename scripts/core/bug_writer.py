import json
from pathlib import Path
from datetime import datetime

TEMPLATE_PATH = Path(".antigravity/prompts/templates/bug_template.md")
BUG_DIR = Path("tickets/bugs")


def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def render_template(template, data):

    text = template

    text = text.replace("{{BUG_ID}}", data["id"])
    text = text.replace("{{TITLE}}", data["title"])
    text = text.replace("{{PRIORITY}}", data.get("priority", "medium"))
    text = text.replace("{{ERROR}}", data.get("error", ""))
    text = text.replace("{{CAUSE}}", data.get("cause", ""))
    text = text.replace("{{SUGGESTED_FIX}}", data.get("suggested_fix", ""))
    text = text.replace("{{FILE}}", data.get("file", ""))

    return text


def write_bug_ticket(bug_data):

    BUG_DIR.mkdir(parents=True, exist_ok=True)

    template = load_template()

    content = render_template(template, bug_data)

    filename = f"{bug_data['id']}.md"

    path = BUG_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Bug ticket created: {path}")


def main():

    input_path = Path("tmp/bug_ticket.json")

    if not input_path.exists():
        raise FileNotFoundError("tmp/bug_ticket.json not found")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    write_bug_ticket(data)


if __name__ == "__main__":
    main()