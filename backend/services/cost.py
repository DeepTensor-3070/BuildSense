import joblib
import numpy as np

# Load models and encoder at module level for efficiency
material_model = joblib.load("backend/models/material_model.pkl")
labor_model = joblib.load("backend/models/labor_model.pkl")
encoder = joblib.load("backend/models/encoders.pkl")


import pandas as pd

def predict_cost(data):

    df = pd.DataFrame([data])

    # Encode categorical columns properly
    for col in ["material", "location", "quality"]:
        df[col] = encoder[col].transform(df[col])

    # Ensure column order matches training
    df = df[["area", "floors", "material", "location", "quality"]]

    # Predict
    material_cost = material_model.predict(df)[0]
    labor_cost = labor_model.predict(df)[0]

    overhead = 0.15 * (material_cost + labor_cost)
    contingency = 0.08 * (material_cost + labor_cost)

    total_cost = material_cost + labor_cost + overhead + contingency

    return {
        "material_cost": material_cost,
        "labor_cost": labor_cost,
        "overhead": overhead,
        "contingency": contingency,
        "total_cost": total_cost
    }