from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import SECRET_KEY

from routes import (
    cases,
    evidence,
    analysis,
    graph,
    dashboard,
    auth,
    entities,
    security,
    ai
)

app = FastAPI(title="Cyber Squad API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(cases.router)
app.include_router(evidence.router)
app.include_router(analysis.router)
app.include_router(graph.router)
app.include_router(dashboard.router)
app.include_router(auth.router)
app.include_router(entities.router)
app.include_router(security.router)
app.include_router(ai.router)

@app.get("/")
def home():
    return {"status": "Cyber Squad API running"}

from pathlib import Path

@app.get("/config-test")
def config_test():
    return {
        "secret": SECRET_KEY,
        "env_exists": (Path(__file__).parent / ".env").exists()
    }