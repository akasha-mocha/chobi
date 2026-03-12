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