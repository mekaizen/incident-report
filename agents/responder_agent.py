# responder_agent.py
import joblib
import numpy as np

import pandas as pd

class ResponderAgent:
    def __init__(self, config):
        self.config = config
        self.classifier = joblib.load(config["responder_model_path"])


    def run(self, coordinator_output, investigator_report="", severity="", method="unknown", end_point="unknown"):
        input_text = f"Coordinator Decision: {coordinator_output}\n"
        if investigator_report:
            input_text += f"Investigator Findings: {investigator_report}\n"
        if severity:
            input_text += f"Severity: {severity}\n"

        row_df = pd.DataFrame([{
            "text": input_text,
            "method": method,
            "end_point": end_point,
            "severity": severity 
        }])

        label = self.classifier.predict(row_df)[0]
        return label



