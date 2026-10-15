from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decision_engine import process_decision
from services.outcome_engine import process_outcome
import state_engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Focus Application Backend is running!"}

@app.options("/state")
def options_state():
    return {}

@app.post("/state")
def receive_state(state: dict):
    behavioral_state = state_engine.process(state)
    return behavioral_state

@app.post("/decision")
def decision_engine(data: dict):
    decision = process_decision(data)
    return decision

@app.post("/outcome")
def outcome_engine(data: dict):
    return process_outcome(data)
