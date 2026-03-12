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