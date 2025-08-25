#investigator_agent.py

import joblib
import pandas as pd

import joblib
import pandas as pd

class InvestigatorAgent:
    def __init__(self, severity_model_path="severity_model/severity_predictor.pkl"):
        self.severity_model = joblib.load(severity_model_path)

    def classify_incident(self, incident_description):
        desc = incident_description.lower()
        if "unauthorized" in desc or "forbidden" in desc:
            return "Access Violation"
        elif "error" in desc or "exception" in desc:
            return "Server Error"
        elif "timeout" in desc:
            return "Timeout"
        else:
            return "General Incident"

    def predict_severity(self, row):
        try:
            message = str(row.get("message", ""))
            input_field = str(row.get("input", ""))
            reason = str(row.get("reason", ""))
            url = str(row.get("url", ""))
            extra_info = str(row.get("extra_info", ""))
            status = str(row.get("status", "")).lower()
            method = str(row.get("method", "")).lower()
            end_point = str(row.get("end_point", "")).lower()

            text = f"{message} {input_field} {reason} {url} {extra_info}".strip()

            df = pd.DataFrame([{
                "text": text,
                "status": status,
                "method": method,
                "end_point": end_point
            }])

            prediction = self.severity_model.predict(df)[0]
            return prediction
        except Exception as e:
            print(f"⚠️ Severity prediction failed: {e}")
            return "unknown"

    def run(self, text, method="unknown", end_point="unknown", status="", reason=""):
        # 1. Run rule-based classification
        classification = self.classify_incident(text)

        # 2. Prepare row for severity prediction
        row = {
            "message": text,
            "input": "",  # Optional field, can be left blank
            "reason": reason,
            "url": "",  # Optional field, can be left blank
            "extra_info": "",  # Optional field, can be left blank
            "status": status,
            "method": method,
            "end_point": end_point
        }

        # 3. Predict severity
        severity = self.predict_severity(row)

        return classification, severity
