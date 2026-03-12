from fastapi import APIRouter

from dashboard.services.metrics_service import get_metrics
from dashboard.services.task_service import get_tasks
from dashboard.services.bug_service import get_bugs
from dashboard.services.cost_service import get_costs
from dashboard.services.system_service import get_system_status
from dashboard.services.log_service import get_logs
from dashboard.services.ai_control_service import (
    start_ai,
    stop_ai,
    pause_ai,
    get_ai_status
)

api = APIRouter()


@api.get("/logs")
def logs():
    return get_logs()


@api.get("/metrics")
def metrics():
    return get_metrics()


@api.get("/tasks")
def tasks():
    return get_tasks()


@api.get("/bugs")
def bugs():
    return get_bugs()


@api.get("/costs")
def costs():

    try:
        return get_costs()

    except Exception:

        return {
            "today": 0,
            "month": 0,
            "daily_budget": 0,
            "monthly_budget": 0,
            "remaining_today": 0,
            "remaining_month": 0
        }


@api.get("/system")
def system():
    return get_system_status()


@api.post("/ai/start")
def ai_start():
    return start_ai()


@api.post("/ai/stop")
def ai_stop():
    return stop_ai()


@api.post("/ai/pause")
def ai_pause():
    return pause_ai()


@api.get("/ai/status")
def ai_status():
    return get_ai_status()
    
    
==================================================
FILE PATH: C:\works\eco\test01\chobi\dashboard\api\dev_command_center_api.py
==================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pathlib import Path

from scripts.utils.logger import get_logger
from dashboard.api.api import api as api_router

logger = get_logger("dashboard_server")

# ---------------------------------------
# Path Resolve (environment independent)
# ---------------------------------------

ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = ROOT / "dashboard" / "static"


def create_app():

    app = FastAPI(
        title="AI Dev Command Center",
        version="1.0"
    )

    # ----------------------------
    # CORS
    # ----------------------------

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ----------------------------
    # API Routers
    # ----------------------------

    app.include_router(
        api_router,
        prefix="/api"
    )

    # ----------------------------
    # Static UI
    # ----------------------------

    app.mount(
        "/",
        StaticFiles(directory=str(STATIC_DIR), html=True),
        name="dashboard"
    )

    # ----------------------------
    # Startup
    # ----------------------------

    @app.on_event("startup")
    async def startup_event():

        logger.info("Dev Command Center started")

    # ----------------------------
    # Health Check
    # ----------------------------

    @app.get("/health")
    async def health():

        return {
            "status": "ok",
            "service": "ai-dev-dashboard"
        }

    return app


app = create_app()



==================================================
FILE PATH: C:\works\eco\test01\chobi\dashboard\services\bug_service.py
==================================================
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BUG_DIR = ROOT / "tickets/bugs"


def parse_bug_md(text: str):

    bug = {
        "id": "",
        "title": "",
        "status": "",
        "priority": ""
    }

    id_match = re.search(r"^ID:\s*(.*)", text, re.MULTILINE)
    if id_match:
        bug["id"] = id_match.group(1).strip()

    title_match = re.search(r"^Title:\s*(.*)", text, re.MULTILINE)
    if title_match:
        bug["title"] = title_match.group(1).strip()

    status_match = re.search(r"^Status:\s*(.*)", text, re.MULTILINE)
    if status_match:
        bug["status"] = status_match.group(1).strip()

    priority_match = re.search(r"^Priority:\s*(.*)", text, re.MULTILINE)
    if priority_match:
        bug["priority"] = priority_match.group(1).strip()

    return bug


def get_bugs():

    bugs = []

    if not BUG_DIR.exists():
        return bugs

    for f in BUG_DIR.glob("*.md"):

        try:

            with open(f, encoding="utf8") as fp:
                text = fp.read()

            bug = parse_bug_md(text)

            bugs.append(bug)

        except Exception:
            continue

    return bugs



==================================================
FILE PATH: C:\works\eco\test01\chobi\dashboard\services\cost_service.py
==================================================
import time
from threading import Lock

from scripts.metrics.cost_control_engine import CostControlEngine
from scripts.utils.logger import get_logger

logger = get_logger(__name__)

_engine = CostControlEngine()

CACHE_TTL = 3

_cache_time = 0
_cache_data = None

_lock = Lock()


def _refresh_cache():

    global _cache_time
    global _cache_data

    try:

        today = _engine.get_today_cost()
        month = _engine.get_month_cost()

        daily_budget = _engine.budget["daily_usd"]
        monthly_budget = _engine.budget["monthly_usd"]

        _cache_data = {
            "today": today,
            "month": month,
            "daily_budget": daily_budget,
            "monthly_budget": monthly_budget,
            "remaining_today": max(0, daily_budget - today),
            "remaining_month": max(0, monthly_budget - month)
        }

        _cache_time = time.time()

    except Exception as e:

        logger.error(f"Cost service error: {e}")

        _cache_data = {
            "today": 0,
            "month": 0,
            "daily_budget": 0,
            "monthly_budget": 0,
            "remaining_today": 0,
            "remaining_month": 0
        }


def get_costs():

    global _cache_time
    global _cache_data

    with _lock:

        if _cache_data is None or time.time() - _cache_time > CACHE_TTL:
            _refresh_cache()

        return _cache_data



==================================================
FILE PATH: C:\works\eco\test01\chobi\dashboard\services\metrics_service.py
==================================================
from dashboard.services.task_service import get_tasks
from dashboard.services.bug_service import get_bugs


def get_metrics():

    tasks = get_tasks()
    bugs = get_bugs()

    return {
        "tasks": len(tasks),
        "bugs": len(bugs)
    }



==================================================
FILE PATH: C:\works\eco\test01\chobi\dashboard\services\system_service.py
==================================================
import psutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AUTOPILOT_STATE_FILE = ROOT / "runtime" / "autopilot_state.txt"


def _read_ai_status():

    if not AUTOPILOT_STATE_FILE.exists():
        return "unknown"

    try:

        with open(AUTOPILOT_STATE_FILE, encoding="utf8") as f:
            status = f.read().strip()

        if status == "":
            return "unknown"

        return status

    except Exception:
        return "error"


def get_system_status():

    return {

        "cpu": psutil.cpu_percent(),

        "memory": psutil.virtual_memory().percent,

        "time": int(time.time()),

        "ai_status": _read_ai_status()

    }



==================================================
FILE PATH: C:\works\eco\test01\chobi\dashboard\services\task_service.py
==================================================
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TASK_DIR = ROOT / "tickets/tasks"


def parse_task_md(text: str):

    task = {
        "id": "",
        "title": "",
        "status": "",
        "priority": ""
    }

    id_match = re.search(r"^ID:\s*(.*)", text, re.MULTILINE)
    if id_match:
        task["id"] = id_match.group(1).strip()

    title_match = re.search(r"^Title:\s*(.*)", text, re.MULTILINE)

    if title_match:
        task["title"] = title_match.group(1).strip()

    status_match = re.search(r"^Status:\s*(.*)", text, re.MULTILINE)
    if status_match:
        task["status"] = status_match.group(1).strip()

    priority_match = re.search(r"^Priority:\s*(.*)", text, re.MULTILINE)
    if priority_match:
        task["priority"] = priority_match.group(1).strip()

    return task


def get_tasks():

    tasks = []

    if not TASK_DIR.exists():
        return tasks

    for f in TASK_DIR.glob("*.md"):

        try:

            with open(f, encoding="utf8") as fp:
                text = fp.read()

            task = parse_task_md(text)

            tasks.append(task)

        except Exception:
            continue

    return tasks



==================================================
FILE PATH: C:\works\eco\test01\chobi\dashboard\static\app.js
==================================================
async function loadMetrics() {

    try {

        const res = await fetch("/api/metrics")
        const data = await res.json()

        document.getElementById("tasks_count").innerText = data.tasks
        document.getElementById("bugs_count").innerText = data.bugs

    } catch (e) {

        console.log("metrics error", e)

    }
}


async function loadCosts() {

    try {

        const res = await fetch("/api/costs")
        const data = await res.json()

        document.getElementById("cost_today").innerText = data.today
        document.getElementById("cost_month").innerText = data.month

    } catch (e) {

        console.log("cost error", e)

    }
}


async function loadTasks() {

    try {

        const res = await fetch("/api/tasks")
        const tasks = await res.json()

        const list = document.getElementById("tasks")

        list.innerHTML = ""

        tasks.forEach(t => {

            const li = document.createElement("li")
            li.innerText = t.title + " [" + t.status + "]"

            list.appendChild(li)

        })

    } catch (e) {

        console.log("tasks error", e)

    }
}


async function loadBugs() {

    try {

        const res = await fetch("/api/bugs")
        const bugs = await res.json()

        const list = document.getElementById("bugs")

        list.innerHTML = ""

        bugs.forEach(b => {

            const li = document.createElement("li")
            li.innerText = b.title + " [" + b.status + "]"

            list.appendChild(li)

        })

    } catch (e) {

        console.log("bugs error", e)

    }
}


async function loadSystem() {

    try {

        const res = await fetch("/api/system")
        const data = await res.json()

        document.getElementById("status").innerText =
            "AI: " + data.ai_status +
            " | CPU: " + data.cpu + "%" +
            " | MEM: " + data.memory + "%"

    } catch (e) {

        console.log("system error", e)

    }
}


async function refresh() {

    await loadMetrics()
    await loadCosts()
    await loadTasks()
    await loadBugs()
    await loadSystem()

}


setInterval(refresh, 5000)

refresh()



==================================================
FILE PATH: C:\works\eco\test01\chobi\dashboard\static\index.html
==================================================
<!DOCTYPE html>
<html>
<head>

<title>AI DevOS Command Center</title>

<link rel="stylesheet" href="style.css">

</head>

<body>

<h1>AI Development Command Center</h1>

<div id="status">Loading...</div>

<h2>Tasks</h2>
<ul id="tasks"></ul>

<h2>Bugs</h2>
<ul id="bugs"></ul>

<h2>Metrics</h2>

Tasks: <span id="tasks_count"></span><br>
Bugs: <span id="bugs_count"></span><br>

Today Cost: <span id="cost_today"></span><br>
Month Cost: <span id="cost_month"></span>

<script src="app.js"></script>

</body>
</html>



==================================================
FILE PATH: C:\works\eco\test01\chobi\dashboard\static\style.css
==================================================
body{

font-family:Arial;
padding:40px;
background:#111;
color:#eee;

}



