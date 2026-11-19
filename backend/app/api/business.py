from fastapi import APIRouter, Query

from app.core.data_store import load_transactions
from app.services.copilot import copilot_answer
from app.services.optimization import menu_recommendations, pricing_scenario
from app.services.predictive import forecast_suitability

router = APIRouter(tags=["business"])


@router.get("/forecast/suitability")
def forecast_suitability_endpoint():
    return forecast_suitability(load_transactions())


@router.get("/optimization/menu")
def menu():
    return menu_recommendations(load_transactions())


@router.get("/optimization/pricing")
def pricing(
    product_detail: str = Query(...),
    price_change_percent: float = Query(default=0),
    quantity_assumption: str = Query(default="baseline"),
):
    return pricing_scenario(load_transactions(), product_detail, price_change_percent, quantity_assumption)


@router.post("/copilot")
def copilot(payload: dict):
    question = str(payload.get("question", "")).strip()
    if not question:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="question is required")
    return copilot_answer(question, load_transactions())
