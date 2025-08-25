

import pandas as pd
from agents.coordinator_agent import CoordinatorAgent
from agents.investigator_agent import InvestigatorAgent
from agents.responder_agent import ResponderAgent
from configs.config import CONFIG

#  Set output path
OUTPUT_FILE = "data/processed_logs_final.csv"
INPUT_FILE = "unified_incident_logs.csv"  # or use "labeled_incident_logs.csv" for validation

def generate_incident_description(row):
    parts = []
    if pd.notna(row.get('input')) and row['input'] != 'N/A':
        parts.append(f"Input: {row['input']}")
    if pd.notna(row.get('method')) and row['method'] != 'N/A':
        parts.append(f"Method: {row['method']}")
    if pd.notna(row.get('end_point')) and row['end_point'] != 'N/A':
        parts.append(f"Endpoint: {row['end_point']}")
    if pd.notna(row.get('reason')) and row['reason'] != 'N/A':
        parts.append(f"Reason: {row['reason']}")
    if pd.notna(row.get('message')) and row['message'] != 'N/A':
        parts.append(f"Message: {row['message']}")
    if pd.notna(row.get('extra_info')) and row['extra_info'] != 'N/A':
        parts.append(f"Extra Info: {row['extra_info']}")
    return ". ".join(parts)

def main():
    try:
        # 🔹 Load incident data
        df = pd.read_csv(INPUT_FILE)
        df = df.head(10)  #  Limit to 10 rows for faster testing
        print(f" Loaded {len(df)} rows (for test run)")
        print(f" Loaded {len(df)} records from {INPUT_FILE}")
    except Exception as e:
        print(f" Error loading file: {e}")
        return

    #  Ensure required columns exist
    required_cols = {"input", "method", "end_point", "reason", "message", "extra_info"}
    missing = required_cols - set(df.columns)
    if missing:
        print(f" Missing columns in CSV: {missing}")
        return

    #  Initialize agents
    coordinator = CoordinatorAgent(CONFIG)
    investigator = InvestigatorAgent(CONFIG)
    responder = ResponderAgent(CONFIG)

    processed_logs = []

    for _, row in df.iterrows():
        try:
            incident_description = generate_incident_description(row)

            # Investigator: Classification (e.g. Category/Subcategory)
            classification = investigator.run(incident_description)

            investigator_output = investigator.run(incident_description, row)
            classification = "N/A"
            severity = "unknown"

            #  Split output
            for line in investigator_output.split("\n"):
                if "Classification:" in line:
                    classification = line.split(":", 1)[-1].strip()
                elif "Predicted Severity:" in line:
                    severity = line.split(":", 1)[-1].strip()

            #  Coordinator: Strategy
            coordination = coordinator.run(incident_description)

            # Responder: Action
            response = responder.run(coordination, classification)

            #  Final Summary
            final_report = coordinator.run(incident_description, classification, response)

            processed_logs.append({
            "method": row.get("method", "N/A"),
            "end_point": row.get("end_point", "N/A"),
            "reason": row.get("reason", "N/A"),
            "classification": classification,
            "severity": severity,
            "coordinator_decision": coordination,
            "responder_action": response,
            "final_report": final_report
        })

        except Exception as e:
            print(f" Error processing row: {e}")
            continue

    # Save results
    output_df = pd.DataFrame(processed_logs)
    output_df.to_csv(OUTPUT_FILE, index=False)
    print(f" Processed {len(output_df)} records. Output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

