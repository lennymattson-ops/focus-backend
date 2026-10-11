rom fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Focus Application Backend is running!"}