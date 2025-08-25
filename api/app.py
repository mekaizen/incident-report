from fastapi import FastAPI
from pydantic import BaseModel

from configs.config import CONFIG
from agents.investigator_agent import InvestigatorAgent
from agents.coordinator_agent import CoordinatorAgent
from agents.responder_agent import ResponderAgent
from fastapi import UploadFile, File
import pandas as pd


app = FastAPI(title="Incident Response API")

# Load agents
investigator = InvestigatorAgent(CONFIG["model_path"])
coordinator = CoordinatorAgent(CONFIG)
responder = ResponderAgent(CONFIG)

# Input schema
class IncidentInput(BaseModel):
    message: str
    method: str = "unknown"
    end_point: str = "unknown"
    status: str = ""
    reason: str = ""

@app.get("/")
def read_root():
    return {"message": "Incident Response API is running!"}

@app.post("/predict")
def predict_incident(incident: IncidentInput):
    # 1. Classification + Severity
    classification, severity = investigator.run(
        text=incident.message,
        method=incident.method,
        end_point=incident.end_point,
        status=incident.status,
        reason=incident.reason
    )

    # 2. Coordinator decision
    coord_decision = coordinator.run(
        incident_description=incident.message,
        severity=severity,
        method=incident.method,
        end_point=incident.end_point
    )

    # 3. Responder action
    response = responder.run(
        coordinator_output=coord_decision,
        severity=severity
    )

    # Final report
    final_report = response

    return {
        "classification": classification,
        "severity": severity,
        "coordinator_decision": coord_decision,
        "responder_action": response,
        "final_report": final_report
    }

# Optional alias route
@app.post("/predict_incident")
def predict_incident_alias(incident: IncidentInput):
    return predict_incident(incident)


@app.post("/predict-bulk")
def predict_bulk(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    results = []

    for _, row in df.iterrows():
        incident_description = row.get("message", "")
        classification = investigator.classify_incident(incident_description)
        severity = investigator.predict_severity(row)
        results.append({
            "message": incident_description,
            "classification": classification,
            "severity": severity
        })

    return {"results": results}
