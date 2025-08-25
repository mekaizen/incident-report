# train_agents.py

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

DATA_FILE = "data/processed_logs_final3.csv"

def train_agent_model(target_column, model_path):
    df = pd.read_csv(DATA_FILE)

    # ➕ Add heuristic responder_action values if missing/only one class
    if target_column == "responder_action" and df[target_column].nunique() <= 1:
        print("⚠️ Adding heuristic responder_action values based on severity...")
        df["responder_action"] = df["severity"].map({
            "low": "monitor",
            "medium": "investigate",
            "high": "isolate"
        }).fillna("investigate")

    # 🔍 Filter rows with valid target values
    df = df[df[target_column].notnull()]

    # 🚨 Skip if only one unique value
    if df[target_column].nunique() <= 1:
        print(f"❌ Skipping training for {target_column}: only one unique class present.")
        return

    # ✅ Generate combined text field
    df["text"] = (
        "Classification: " + df["classification"].astype(str) + "\n" +
        "Severity: " + df["severity"].astype(str) + "\n" +
        "Method: " + df["method"].astype(str) + "\n" +
        "Endpoint: " + df["end_point"].astype(str) + "\n" +
        "Reason: " + df["reason"].astype(str)
    )

    X = df[["text", "method", "end_point", "severity"]]
    y = df[target_column]

    # 🛠 Transformers
    text_transformer = TfidfVectorizer(max_features=300)
    cat_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(transformers=[
        ("text", text_transformer, "text"),
        ("method", cat_transformer, ["method"]),
        ("end_point", cat_transformer, ["end_point"]),
        ("severity", cat_transformer, ["severity"])
    ])

    # 🌲 Random Forest with class_weight
    pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("clf", RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42))
    ])

    print(df["coordinator_decision"].value_counts())
    print(df["responder_action"].value_counts())
    print(df["severity"].value_counts())

    # 🧠 Train model
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, model_path)
    print(f"✅ Trained and saved model for: {target_column} ➜ {model_path}")

if __name__ == "__main__":
    train_agent_model("coordinator_decision", "models/coordinator_model.pkl")
    train_agent_model("responder_action", "models/responder_model.pkl")
