from fastapi import APIRouter, Request
from app.agents.exploration_aggregator import run_exploration_agent
from app.agents.intent_theme_inference import run_intent_agent
from app.agents.knowledge_graph_mapper import run_kg_agent
from app.agents.outcome_generator import run_outcome_agent
from app.agents.okr_generator import run_okr_agent

router = APIRouter()

@router.post("/aggregate")
async def aggregate_logs(request: Request):
    data = await request.json()
    return run_exploration_agent(data.get("logs", []))

@router.post("/infer-intent")
async def infer_intent(request: Request):
    data = await request.json()
    return run_intent_agent(data.get("input", []))

@router.post("/map-graph")
async def map_graph(request: Request):
    data = await request.json()
    return run_kg_agent(data.get("input", []))

@router.post("/generate-outcomes")
async def generate_outcomes(request: Request):
    data = await request.json()
    return run_outcome_agent(data.get("input", []))

@router.post("/generate-okr")
async def generate_okr(request: Request):
    data = await request.json()
    return run_okr_agent(data.get("input", []))
