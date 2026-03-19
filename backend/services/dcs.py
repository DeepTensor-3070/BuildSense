import joblib
import os

dcs_model = None


def load_model():
    global dcs_model
    if dcs_model is None:
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "models", "dcs_model.pkl"
        )
        dcs_model = joblib.load(model_path)
    return dcs_model


def encode_material(mat):
    return {
        "Concrete": 0,
        "Steel frame": 1,
        "Timber": 2,
        "Composite": 3
    }.get(mat, 0)


def encode_location(loc):
    return {
        "Urban": 0,
        "Semi-urban": 1
    }.get(loc, 0)


def predict_dcs(data, predicted_cost, risk):

    model = load_model()   # ✅ load safely here

    area = data["area"]
    floors = data["floors"]

    material = encode_material(data["material"])
    location = encode_location(data["location"])

    # feature engineering (same as training)
    complexity = floors * 2 + area / 10000
    volatility_map = {0: 0.2, 1: 0.5, 2: 0.4, 3: 0.3}
    volatility = volatility_map[material]

    error_estimate = risk / 100

    X = [[
        area,
        floors,
        material,
        location,
        complexity,
        volatility,
        error_estimate
    ]]

    try:
        dcs = model.predict(X)[0]
        dcs = max(30, min(98, dcs))
        return int(dcs)
    except Exception as e:
        print("DCS prediction error:", e)
        return 70   # safe fallback