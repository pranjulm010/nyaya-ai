from core.config import (
    MAX_FREE_QUERIES,
    MAX_PUBLIC_QUERIES,
    MAX_LAWYER_QUERIES,
)


USER_PLANS = {
    "free": {
        "daily_queries": MAX_FREE_QUERIES,
        "monthly_queries": 100,
        "premium_allowed": False,
        "document_uploads": 3,
    },
    "public": {
        "daily_queries": MAX_PUBLIC_QUERIES,
        "monthly_queries": 1000,
        "premium_allowed": False,
        "document_uploads": 20,
    },
    "lawyer": {
        "daily_queries": MAX_LAWYER_QUERIES,
        "monthly_queries": 10000,
        "premium_allowed": True,
        "document_uploads": 200,
    },
}


def get_plan_limits(user_type: str = "free") -> dict:
    return USER_PLANS.get(
        user_type,
        USER_PLANS["free"]
    )