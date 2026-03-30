import joblib
import numpy as np
import json
import os

BASE_PATH = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_PATH, "saved")

# ---------------------------
# 🔹 Dynamic Model Loader
# ---------------------------
def load_model_bundle(model_name):
    model_path = os.path.join(MODEL_DIR, f"{model_name}.pkl")
    meta_path = os.path.join(MODEL_DIR, f"{model_name}_meta.json")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")

    if not os.path.exists(meta_path):
        raise FileNotFoundError(f"Metadata not found: {meta_path}")

    model = joblib.load(model_path)

    with open(meta_path) as f:
        metadata = json.load(f)

    return {
        "model": model,
        "features": metadata["features"]
    }


# ---------------------------
# 🔹 Load All Models
# ---------------------------
MODELS = {
    "cost": load_model_bundle("cost_model_v1"),
    "time": load_model_bundle("time_model_v1"),
    "risk": load_model_bundle("risk_model_v1")
}
# print("COST FEATURES:", MODELS["cost"]["features"])
# print("TIME FEATURES:", MODELS["time"]["features"])
# print("RISK FEATURES:", MODELS["risk"]["features"])

# ---------------------------
# 🔹 Input Validation
# ---------------------------
def validate_input(features, required_features):
    missing = [f for f in required_features if f not in features]

    if missing:
        raise ValueError(f"Missing features: {missing}")

    clean_features = {}

    for key in required_features:
        try:
            clean_features[key] = float(features[key])
        except:
            raise ValueError(f"Invalid value for {key}")

    return clean_features


# ---------------------------
# 🔹 Feature Preparation
# ---------------------------
def prepare_features(input_dict, feature_order):
    # 🔥 IMPORTANT: copy input to avoid mutation
    input_copy = input_dict.copy()

    # Remove unwanted keys
    input_copy.pop("risk_index", None)
    input_copy.pop("Unnamed: 0", None)

    # Keep only required features
    cleaned = {k: input_copy[k] for k in feature_order if k in input_copy}

    # Validate missing
    missing = [f for f in feature_order if f not in cleaned]
    if missing:
        raise ValueError(f"Missing features: {missing}")

    return np.array([[float(cleaned[f]) for f in feature_order]])


# ---------------------------
# 🔹 Core Prediction Engine
# ---------------------------
def predict_model(model_key, features):
    bundle = MODELS[model_key]
    model = bundle["model"]
    feature_order = bundle["features"]

    X = prepare_features(features, feature_order)

    pred = model.predict(X)[0]

    # Add probabilities if classifier
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        return pred, probs

    return pred, None


# ---------------------------
# 🔹 Utility Functions
# ---------------------------
def add_uncertainty(value, percent=0.1):
    return {
        "min": round(value * (1 - percent), 2),
        "max": round(value * (1 + percent), 2)
    }


def map_risk(pred):
    return {0: "Low", 1: "Medium", 2: "High"}[int(pred)]


def calculate_dcs(cost, time, risk):
    score = 100

    risk_penalty = {"Low": 0, "Medium": 15, "High": 30}
    score -= risk_penalty[risk]

    score -= min(cost / 200000, 20)
    score -= min(time / 20, 20)

    return max(int(score), 0)


# ---------------------------
# 🔹 Unified Prediction API
# ---------------------------
def predict_all(features: dict):
    # Cost Prediction
    features = features.copy()  # Avoid mutating original input
    cost_pred, _ = predict_model("cost", features)
    cost = float(cost_pred)
    # Time Prediction
    time_pred, _ = predict_model("time", features)
    time = float(time_pred)

    # Risk Prediction
    risk_pred, risk_probs = predict_model("risk", features)
    risk_label = map_risk(risk_pred)

    risk_output = {
        "label": risk_label
    }

    if risk_probs is not None:
        risk_output.update({
            "confidence": float(max(risk_probs)),
            "probabilities": {
                "Low": float(risk_probs[0]),
                "Medium": float(risk_probs[1]),
                "High": float(risk_probs[2])
            }
        })

    # Final Output
    result = {
        "estimated_cost": round(cost, 2),
        "cost_range": add_uncertainty(cost),

        "estimated_time": round(time, 2),
        "time_range": add_uncertainty(time),

        "risk": risk_output
    }

    # Add DCS Score
    result["dcs_score"] = calculate_dcs(cost, time, risk_label)

    return result

def predict_with_dcs(features: dict):
    return predict_all(features)
# ---------------------------
# 🔹 Test Run
# ---------------------------
if __name__ == "__main__":
    sample = {
        "area": 1500,
        "material_quality": 2,
        "location_factor": 1.3,
        "labor_cost": 60000,
        "project_type": 1,
        "floors": 2,
        "soil_type": 2,
        "weather_index": 0.4,
        "material_price_index": 1.2,
        "contractor_experience": 5,
        "equipment_availability": 0.8,
        "project_complexity": 2,
        "permits_delay": 5,
        "transport_cost": 20000,
        "inflation_factor": 1.1,
        "cost_per_sqft_est": 2.4,
        "labor_intensity": 40,
        "efficiency": 4.0
    }

    print(predict_all(sample))
