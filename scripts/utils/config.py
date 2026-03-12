# AI Development System Configuration

from pathlib import Path

# --------------------------------
# Project Paths
# --------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCS_DIR = PROJECT_ROOT / "docs"
SRC_DIR = PROJECT_ROOT / "src"
TEST_DIR = PROJECT_ROOT / "tests"

TICKETS_DIR = PROJECT_ROOT / "tickets"
TASK_DIR = TICKETS_DIR / "tasks"
BUG_DIR = TICKETS_DIR / "bugs"

LOG_DIR = PROJECT_ROOT / "logs"

ANTIGRAVITY_DIR = PROJECT_ROOT / ".antigravity"
WORKFLOW_DIR = ANTIGRAVITY_DIR / "workflows"
PROMPT_DIR = ANTIGRAVITY_DIR / "prompts"

# --------------------------------
# AI Commands
# --------------------------------

# Claude Code CLI
CLAUDE_CMD = [
    "claude-code"
]

# OpenAI Codex CLI
CODEX_CMD = [
    "codex"
]

# Antigravity workflow runner
ANTIGRAVITY_CMD = [
    "antigravity"
]

# --------------------------------
# Workflow Names
# --------------------------------

TASK_GENERATOR_WORKFLOW = "task_generator"
BUG_GENERATOR_WORKFLOW = "bug_fix_generator"

# --------------------------------
# Build / Test Commands
# --------------------------------

BUILD_CMD = [
    "dotnet",
    "build"
]

TEST_CMD = [
    "dotnet",
    "test"
]

# --------------------------------
# Retry Configuration
# --------------------------------

MAX_FIX_RETRY = 3

# --------------------------------
# Log Files
# --------------------------------

BUILD_LOG = LOG_DIR / "build.log"
TEST_LOG = LOG_DIR / "test.log"
AI_LOG = LOG_DIR / "ai.log"

# --------------------------------
# Git Configuration
# --------------------------------

ENABLE_GIT_AUTO_COMMIT = True

GIT_COMMIT_PREFIX = "AI"

# --------------------------------
# Task Status
# --------------------------------

TASK_STATUS_OPEN = "Status: Open"
TASK_STATUS_DONE = "Status: Done"

BUG_STATUS_OPEN = "Status: Open"
BUG_STATUS_FIXED = "Status: Fixed"

# --------------------------------
# Utility
# --------------------------------

def ensure_directories():
    """Ensure required directories exist."""
    for d in [
        TASK_DIR,
        BUG_DIR,
        LOG_DIR
    ]:
        d.mkdir(parents=True, exist_ok=True)