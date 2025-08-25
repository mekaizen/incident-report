#test_prediction.py

from agents_model.investigator_agent_model import InvestigatorAgent
from agents_model.coordinator_agent_model import CoordinatorAgent
from agents_model.responder_agent_model import ResponderAgent
from configs.config import CONFIG

# Sample log entry (you can update this with any row content)
sample_row = {
    "input": "admin' OR '1'='1",
    "method": "POST",
    "end_point": "/login",
    "reason": "Suspicious input",
    "message": "Multiple failed login attempts",
    "extra_info": "User: admin",
    "status": "403"
}

# Generate incident description
def generate_description(row):
    parts = []
    for field, label in [
        ('input', "Input"), ('method', "Method"), ('end_point', "Endpoint"),
        ('reason', "Reason"), ('message', "Message"), ('extra_info', "Extra Info")
    ]:
        val = row.get(field)
        if val: parts.append(f"{label}: {val}")
    return ". ".join(parts)

if __name__ == "__main__":
    # Load agents
    investigator = InvestigatorAgent(
        severity_model_path="severity_model/severity_predictor.pkl",
        classifier_model_dir="models_new/binary_classifier"
    )
    coordinator = CoordinatorAgent(CONFIG)
    responder = ResponderAgent(CONFIG)

    incident_text = generate_description(sample_row)

    # Run investigator
    classification, category_type, subcategory, severity = investigator.run(
        incident_text,
        method=sample_row["method"],
        end_point=sample_row["end_point"],
        status=sample_row["status"],
        reason=sample_row["reason"]
    )

    # Run responder
    responder_action = responder.run(classification, severity)

    # Run coordinator
    coordinator_decision = coordinator.run(
        incident_text,
        investigator_report=classification,
        responder_report=responder_action,
        severity=severity,
        method=sample_row["method"],
        end_point=sample_row["end_point"]
    )

    # Output
    print("\n--- Final Prediction ---")
    print(f"Classification   : {classification}")
    print(f"Category Type    : {category_type}")
    print(f"Subcategory      : {subcategory}")
    print(f"Severity         : {severity}")
    print(f"Responder Action : {responder_action}")
    print(f"Coordinator      : {coordinator_decision}")
