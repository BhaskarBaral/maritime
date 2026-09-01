from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services import ml_models as ml

router = APIRouter()

class MonteCarloRequest(BaseModel):
    commodity: str = "IRON ORE"
    charge_delta: float = -5.0
    incentive_pct: float = 8.0

@router.get("/recommendations")
def get_recommendations():
    return {"recommendations": ml.generate_incentive_recommendations()}

@router.post("/monte-carlo")
def run_monte_carlo(req: MonteCarloRequest):
    return ml.run_incentive_monte_carlo(req.commodity, req.charge_delta, req.incentive_pct)
