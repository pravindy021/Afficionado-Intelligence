from typing import Any

import pandas as pd


def forecast_suitability(frame: pd.DataFrame) -> dict[str, Any]:
    columns = set(frame.columns)
    has_year = "year" in columns
    has_time = "transaction_time" in columns
    return {
        "supported": False,
        "finest_supported_granularity": "hour-of-day" if has_time else "not supported",
        "available_history": {
            "year_values": sorted(frame["year"].dropna().unique().tolist()) if has_year else [],
            "calendar_dates": False,
            "hour_values": sorted(frame["hour"].dropna().unique().tolist()) if "hour" in columns else [],
        },
        "models": [],
        "reason": "The source has year and time-of-day fields but no calendar date or repeated-day history. Daily, weekly, 7-day, 14-day, and 30-day forecasts would invent time continuity.",
        "safe_alternative": "Hourly revenue and quantity summaries may describe observed source-time patterns, but they are not forecasts.",
    }
