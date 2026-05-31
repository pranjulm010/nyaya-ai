from datetime import datetime
from typing import Dict, Any

from billing.limits import get_plan_limits


# MVP in-memory usage store.
# Later replace with PostgreSQL/Redis.
USAGE_DB = {}


def get_today_key() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def get_month_key() -> str:
    return datetime.utcnow().strftime("%Y-%m")


def get_user_usage(user_id: str) -> Dict[str, Any]:
    if user_id not in USAGE_DB:
        USAGE_DB[user_id] = {
            "daily": {},
            "monthly": {},
            "total_queries": 0,
            "last_used": None,
        }

    return USAGE_DB[user_id]


def can_user_continue(
    user_id: str,
    user_type: str = "free"
) -> Dict[str, Any]:

    limits = get_plan_limits(user_type)
    usage = get_user_usage(user_id)

    today = get_today_key()
    month = get_month_key()

    daily_count = usage["daily"].get(today, 0)
    monthly_count = usage["monthly"].get(month, 0)

    if daily_count >= limits["daily_queries"]:
        return {
            "allowed": False,
            "reason": "daily_limit_exceeded",
            "message": (
                f"Daily limit reached for {user_type} plan. "
                "Please try again tomorrow or upgrade."
            )
        }

    if monthly_count >= limits["monthly_queries"]:
        return {
            "allowed": False,
            "reason": "monthly_limit_exceeded",
            "message": (
                f"Monthly limit reached for {user_type} plan. "
                "Please upgrade your plan."
            )
        }

    return {
        "allowed": True,
        "reason": "ok",
        "daily_used": daily_count,
        "monthly_used": monthly_count,
        "daily_limit": limits["daily_queries"],
        "monthly_limit": limits["monthly_queries"],
    }


def track_usage(
    user_id: str,
    user_type: str = "free",
    intent: str = "simple_legal",
    sources_count: int = 0
) -> None:

    usage = get_user_usage(user_id)

    today = get_today_key()
    month = get_month_key()

    usage["daily"][today] = usage["daily"].get(today, 0) + 1
    usage["monthly"][month] = usage["monthly"].get(month, 0) + 1
    usage["total_queries"] += 1
    usage["last_used"] = datetime.utcnow().isoformat()

    usage["last_intent"] = intent
    usage["last_sources_count"] = sources_count


def get_usage_summary(user_id: str) -> Dict[str, Any]:
    usage = get_user_usage(user_id)

    today = get_today_key()
    month = get_month_key()

    return {
        "today": usage["daily"].get(today, 0),
        "this_month": usage["monthly"].get(month, 0),
        "total_queries": usage["total_queries"],
        "last_used": usage["last_used"],
        "last_intent": usage.get("last_intent"),
        "last_sources_count": usage.get("last_sources_count"),
    }