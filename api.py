from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, Union
import json
from datetime import datetime
from pathlib import Path

app = FastAPI(title="DG Analyzer API", version="1.2.0")

OUTPUT_FILE = Path("latest_governance.json")


class GovernancePayload(BaseModel):
    dataset_name: str
    # Accept either:
    # - a normal JSON object (dict), or
    # - a JSON string (minified) to avoid GPT Actions runner parsing issues
    analysis: Union[Dict[str, Any], str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/governance/analyze")
def submit_governance(payload: GovernancePayload):
    analysis_obj = payload.analysis

    # If analysis comes as a string, parse it as JSON
    if isinstance(analysis_obj, str):
        try:
            analysis_obj = json.loads(analysis_obj)
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": "analysis must be a valid JSON string when provided as string",
                "details": str(e),
            }

    data = {
        "dataset": payload.dataset_name,
        "analysis": analysis_obj,
        "timestamp": datetime.utcnow().isoformat(),
    }

    OUTPUT_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"status": "ok"}


@app.get("/governance/latest")
def get_latest():
    if not OUTPUT_FILE.exists():
        return {"status": "empty", "message": "no analysis submitted yet"}
    return json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
