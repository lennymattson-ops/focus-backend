from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.Services.state_engine as state_engine
from app.Services.decision_engine import process_decision
from app.Services.outcome_engine import process_outcome
from app.Services.optimization_engine import optimize
from app.Services.loop_engine import closed_loop

# NEW: Behavioral Memory Store
from app.Services.history_store import append_record, load_history
from datetime import datetime

app = FastAPI()

# ---------------------------------------------------------
# CORS — allow your actual frontend origins
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Focus Application Backend is running!"}

# ---------------------------------------------------------
# State Engine
# ---------------------------------------------------------
@app.post("/state")
def receive_state(state: dict):
    return state_engine.process(state)

# ---------------------------------------------------------
# Decision Engine
# ---------------------------------------------------------
@app.post("/decision")
def decision_engine(data: dict):
    return process_decision(data)

# ---------------------------------------------------------
# Outcome Engine
# ---------------------------------------------------------
@app.post("/outcome")
def outcome_engine(data: dict):
    return process_outcome(data)

# ---------------------------------------------------------
# Optimization Engine
# ---------------------------------------------------------
@app.post("/optimize")
def optimization_endpoint(data: dict):
    interventions = data.get("interventions", [])
    effectiveness_history = data.get("effectiveness_history", {})
    return optimize(interventions, effectiveness_history)

# ---------------------------------------------------------
# Closed Loop Engine + Behavioral Memory Append
# ---------------------------------------------------------
@app.post("/loop")
def loop_endpoint(data: dict):
    previous_state = data.get("previous_state", {})
    current_state = data.get("current_state", {})
    interventions = data.get("interventions", [])
    effectiveness_history = data.get("effectiveness_history", {})
    completed = data.get("completed", False)

    # Run closed loop engine
    loop_result = closed_loop(
        previous_state,
        current_state,
        interventions,
        effectiveness_history,
        completed
    )

    # Build daily history record
    record = {
        "timestamp": datetime.now().isoformat(),
        "previous_state": previous_state,
        "current_state": current_state,
        "decision": data.get("decision"),
        "outcome": data.get("outcome"),
        "optimize": data.get("optimize"),
        "loop_result": loop_result
    }

    # Append to behavioral memory
    append_record(record)

    return loop_result

# ---------------------------------------------------------
# History Retrieval Endpoint
# ---------------------------------------------------------
@app.get("/history")
def get_history():
    return load_history()
