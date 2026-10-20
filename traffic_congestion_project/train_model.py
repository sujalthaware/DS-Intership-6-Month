"""Train a time-aware classifier to predict the next observed congestion class.

Important: this predicts the class at the next *collected observation* for the
same road point, not a guaranteed 15-minute/one-hour forecast.
"""
import json
from collections import Counter

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, classification_report,
    confusion_matrix, f1_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

from config import MODEL_DIR, MODEL_PATH
from storage import load_observations

FEATURES = [
    "current_speed_kmph", "free_flow_speed_kmph", "speed_ratio",
    "congestion_index", "confidence", "hour", "day_of_week", "is_weekend",
    "road_closure", "functional_road_class", "location_id"
]
TARGET = "target_next_congestion"

def make_training_frame(df):
    if df.empty:
        return pd.DataFrame()
    data = df.copy()
    data = data.dropna(subset=["timestamp_utc", "congestion_class"])
    data = data.sort_values(["location_id", "timestamp_utc"])
    data["hour"] = data["timestamp_utc"].dt.hour
    data["day_of_week"] = data["timestamp_utc"].dt.dayofweek
    data["is_weekend"] = (data["day_of_week"] >= 5).astype(int)
    data["road_closure"] = data["road_closure"].fillna(0).astype(int)
    data["target_next_congestion"] = data.groupby("location_id")["congestion_class"].shift(-1)
    return data.dropna(subset=[TARGET]).copy()

def train_and_evaluate(df=None):
    if df is None:
        df = load_observations()
    data = make_training_frame(df)
    if len(data) < 30:
        return {
            "trained": False,
            "message": f"Need at least 30 sequential labeled transitions; currently have {len(data)}. Keep collecting observations.",
            "rows": len(data),
        }
    if data[TARGET].nunique() < 2:
        return {
            "trained": False,
            "message": "The next-observation target has only one class. Collect more varied traffic observations.",
            "rows": len(data),
        }

    data = data.sort_values("timestamp_utc")
    split_at = int(len(data) * 0.8)
    train = data.iloc[:split_at].copy()
    test = data.iloc[split_at:].copy()
    if train[TARGET].nunique() < 2 or test.empty:
        return {
            "trained": False,
            "message": "Not enough time-separated data/classes for a valid evaluation. Collect more observations.",
            "rows": len(data),
        }

    numeric_features = [
        "current_speed_kmph", "free_flow_speed_kmph", "speed_ratio",
        "congestion_index", "confidence", "hour", "day_of_week",
        "is_weekend", "road_closure"
    ]
    categorical_features = ["functional_road_class", "location_id"]

    preprocessor = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]), numeric_features),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical_features)
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=250,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42
        ))
    ])

    model.fit(train[FEATURES], train[TARGET])
    predictions = model.predict(test[FEATURES])
    labels = sorted(set(test[TARGET]) | set(predictions))
    report = classification_report(
        test[TARGET], predictions, labels=labels,
        output_dict=True, zero_division=0
    )
    metrics = {
        "accuracy": float(accuracy_score(test[TARGET], predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(test[TARGET], predictions)),
        "weighted_f1": float(f1_score(test[TARGET], predictions, average="weighted", zero_division=0)),
        "confusion_matrix": confusion_matrix(test[TARGET], predictions, labels=labels).tolist(),
        "labels": labels,
        "classification_report": report,
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "total_transitions": int(len(data)),
        "target_counts": dict(Counter(data[TARGET])),
        "evaluation": "Chronological holdout: earliest 80% train, latest 20% test",
        "target_definition": "Congestion class at the next collected observation for the same location",
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES, "metrics": metrics}, MODEL_PATH)
    with open(MODEL_DIR / "evaluation.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    return {"trained": True, "message": "Model trained and evaluated.", **metrics}

def predict_next(df=None):
    if df is None:
        df = load_observations()
    if not MODEL_PATH.exists():
        return None, "No trained model found. Collect history and train the model first."
    try:
        bundle = joblib.load(MODEL_PATH)
        model = bundle["model"]
        data = make_training_frame(df)
        if df.empty:
            return None, "No observations available."
        latest = df.sort_values("timestamp_utc").groupby("location_id").tail(1).copy()
        latest["hour"] = latest["timestamp_utc"].dt.hour
        latest["day_of_week"] = latest["timestamp_utc"].dt.dayofweek
        latest["is_weekend"] = (latest["day_of_week"] >= 5).astype(int)
        latest["road_closure"] = latest["road_closure"].fillna(0).astype(int)
        pred = model.predict(latest[FEATURES])
        output = latest[["timestamp_utc", "location_id", "location_name", "congestion_class"]].copy()
        output["predicted_next_congestion"] = pred
        output = output.rename(columns={"congestion_class": "current_rule_based_class"})
        return output, None
    except Exception as exc:
        return None, f"Prediction unavailable: {exc}"

if __name__ == "__main__":
    result = train_and_evaluate()
    print(result.get("message"))
    if result.get("trained"):
        print(f'Accuracy: {result["accuracy"]:.3f}')
        print(f'Balanced accuracy: {result["balanced_accuracy"]:.3f}')
        print(f'Weighted F1: {result["weighted_f1"]:.3f}')
        print(f'Model saved to {MODEL_PATH}')
