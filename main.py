from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Engines
import app.Services.state_engine as state_engine
from app.Services.decision_engine import process_decision
from app.Services.outcome_engine import process_outcome
from app.Services.optimization_engine import optimize
from app.Services.loop_engine import closed_loop

# Intervention set (Phase 9 Step 6)
from app.Services.interventions import INTERVENTIONS

# Behavioral Memory Store
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
# Optimization Engine (Phase 9 Step 6)
# ---------------------------------------------------------
@app.post("/optimize")
def optimization_endpoint(data: dict):

    interventions = data.get(
        "interventions",
        INTERVENTIONS
    )

    effectiveness_history = data.get(
        "effectiveness_history",
        {}
    )

    full_history = load_history()

    result = optimize(
        interventions=interventions,
        effectiveness_history=effectiveness_history,
        full_history=full_history,
    )

    return result

# ---------------------------------------------------------
# Closed Loop Engine + Behavioral Memory Append
# ---------------------------------------------------------
@app.post("/loop")
def loop_endpoint(data: dict):
    previous_state = data.get("previous_state", {})
    current_state = data.get("current_state", {})
    decision = data.get("decision", {})
    outcome = data.get("outcome", {})
    interventions = data.get("interventions", [])
    effectiveness_history = data.get("effectiveness_history", {})
    selected_intervention = data.get("selected_intervention", {})
    completed = data.get("completed", False)

    # Run closed loop engine
    loop_result = closed_loop(
        previous_state,
        current_state,
        decision,
        outcome,
        interventions,
        effectiveness_history,
        selected_intervention,
        completed,
    )

    # Build daily history record
    record = {
        "timestamp": datetime.now().isoformat(),
        "previous_state": previous_state,
        "current_state": current_state,
        "decision": decision,
        "outcome": outcome,

        # Store intervention data directly
        "selected_intervention": selected_intervention,
        "updated_interventions": interventions,

        "effectiveness_history": effectiveness_history,

        "loop_result": loop_result,
    }

    append_record(record)

    return loop_result

# ---------------------------------------------------------
# History Retrieval Endpoint
# ---------------------------------------------------------
@app.get("/history")
def get_history():
    return load_history()
