from fastapi import FastAPI
from pydantic import BaseModel
import json
from datetime import datetime
from pathlib import Path

app = FastAPI(title="DG Analyzer API", version="1.0.0")

OUTPUT_FILE = Path("latest_governance.json")

class GovernancePayload(BaseModel):
    dataset_name: str
    analysis: dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/governance/analyze")
def submit_governance(payload: GovernancePayload):
    data = {
        "dataset": payload.dataset_name,
        "analysis": payload.analysis,
        "timestamp": datetime.utcnow().isoformat()
    }
    OUTPUT_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"status": "ok"}

@app.get("/governance/latest")
def get_latest():
    if not OUTPUT_FILE.exists():
        return {"status": "empty", "message": "no analysis submitted yet"}
    return json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
