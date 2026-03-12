import os
import json


PROJECT_STRUCTURE = [

    "docs",
    "docs/specs",

    "tickets/tasks",
    "tickets/bugs",

    "knowledge",
    "memory",
    "metrics",
    "logs",

    "src",

    "scripts/core",
    "scripts/agents",
    "scripts/tasks",
    "scripts/ai",
    "scripts/safety",
    "scripts/memory",
    "scripts/metrics",
    "scripts/utils",

    ".antigravity/prompts",
    ".antigravity/workflows"
]


BASE_FILES = {

    "docs/architecture.md":
"""# Architecture

Describe system architecture here.
""",

    "docs/PROJECT_RULES.md":
"""# Project Rules

Coding rules
Architecture constraints
Test requirements
""",

    "knowledge/project_graph.json":
"""{}""",

    "memory/dev_memory.json":
"""[]"""
}


def create_structure(root):

    for path in PROJECT_STRUCTURE:

        full = os.path.join(root, path)

        os.makedirs(full, exist_ok=True)


def create_base_files(root):

    for path, content in BASE_FILES.items():

        full = os.path.join(root, path)

        os.makedirs(os.path.dirname(full), exist_ok=True)

        if not os.path.exists(full):

            with open(full, "w", encoding="utf-8") as f:
                f.write(content)


def bootstrap(project_name):

    root = os.path.abspath(project_name)

    print("Creating project:", root)

    create_structure(root)

    create_base_files(root)

    print("DevOS project created")


if __name__ == "__main__":

    name = input("Project name: ")

    bootstrap(name)