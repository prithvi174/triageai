from fastapi import FastAPI, HTTPException
from core.schema import TicketRequest, TriageResult
from core.classifier import classify_ticket

app = FastAPI(
    title="TriageAI",
    description="LLM-powered IT support ticket classifier",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "TriageAI is running. Visit /docs for the API playground."}


@app.post("/triage", response_model=TriageResult)
def triage_ticket(request: TicketRequest):
    try:
        result = classify_ticket(request.ticket_text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"Classifier error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")