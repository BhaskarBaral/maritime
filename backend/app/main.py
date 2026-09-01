from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import health, vessels, cargo, forecast, trade, anomaly, incentive, twin, copilot, pipeline, executive

app = FastAPI(
    title="YellowSense Maritime Intelligence API",
    description="AI-Powered Maritime Port Intelligence Platform — Cargo Projection & Predictability Core Engine",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,    tags=["Health"])
app.include_router(vessels.router,   prefix="/vessels",   tags=["Vessel Intelligence"])
app.include_router(cargo.router,     prefix="/cargo",     tags=["Cargo Forecasting"])
app.include_router(forecast.router,                        tags=["Intelligence Forecasting Engine"])
app.include_router(trade.router,     prefix="/trade",     tags=["Trade Intelligence"])
app.include_router(anomaly.router,   prefix="/anomaly",   tags=["Anomaly Detection"])
app.include_router(incentive.router, prefix="/incentive", tags=["Incentive Engine"])
app.include_router(twin.router,      prefix="/twin",      tags=["Digital Twin"])
app.include_router(copilot.router,   prefix="/copilot",   tags=["AI Copilot"])
app.include_router(pipeline.router,  prefix="/pipeline",  tags=["Data Pipeline"])
app.include_router(executive.router, prefix="/executive", tags=["Executive Dashboard"])

@app.get("/")
def root():
    return {"message": "YellowSense Maritime Intelligence API v3.0 — Data Grounded ML Engine Running", "modules": 8}
