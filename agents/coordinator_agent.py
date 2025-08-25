# coordinator_agent.py
import joblib
import numpy as np

import pandas as pd

class CoordinatorAgent:
    def __init__(self, config):
        self.config = config
        self.classifier = joblib.load(config["coordinator_model_path"])

        # def run(self, incident_description, investigator_report="", responder_report=""):
    def run(self, incident_description, investigator_report="", responder_report="", severity="", method="unknown", end_point="unknown"):    
        input_text = f"Incident: {incident_description}\n"
        if investigator_report:
            input_text += f"Investigator Report: {investigator_report}\n"
        if responder_report:
            input_text += f"Responder Report: {responder_report}\n"
        if severity:
            input_text += f"Severity: {severity}\n"    

        if severity.lower() == "high":
            return "block"
        elif severity.lower() == "medium":
            return "investigate"
        else:
            return "monitor"


