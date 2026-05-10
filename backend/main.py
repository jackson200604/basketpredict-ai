# ============================================================
# main.py — FastAPI Application principale
# ============================================================
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import MatchRequest, PredictionResponse
from data_ingestion import collect_match_data
from analytics_engine import run_analytics
from monte_carlo import run_full_simulation

# ── Initialisation ────────────────────────────────────────────
app = FastAPI(
    title       = "🏀 BasketPredictAI",
    description = "Prédiction de matchs basketball par IA",
    version     = "1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],
    allow_methods  = ["*"],
    allow_headers  = ["*"],
)


# =============================================================
# ROUTES
# =============================================================

@app.get("/")
def root():
    return {
        "app":     "BasketPredictAI",
        "version": "1.0.0",
        "status":  "online",
        "docs":    "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
async def predict(req: MatchRequest):
    """
    Endpoint principal de prédiction.
    Reçoit deux équipes et retourne l'analyse complète.
    """
    try:
        # ── 1. Collecte données ───────────────────────────────
        data = await collect_match_data(
            team_home  = req.team_home,
            team_away  = req.team_away,
            league     = req.league or "NBA",
            match_date = req.match_date,
        )

        # ──
