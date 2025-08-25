import os
from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CONFIG = {
    "groq_api_key": GROQ_API_KEY,
    "model_path": "severity_model/severity_predictor.pkl",
    "responder_model_path": "models/responder_model.pkl",
    "coordinator_model_path": "models/coordinator_model.pkl",
    "coordinator_instructions": "You are the Incident Response Coordinator...",
    "investigator_instructions": "You are the Incident Investigator...",
    "responder_instructions": "You are the Incident Responder...",
    "max_iterations": 5
}

