import joblib

risk_model = joblib.load("backend/models/risk_model.pkl")

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


def encode_quality(q):
    return {
        "Standard": 0,
        "Premium": 1
    }.get(q, 0)


def predict_risk(data):

    area = data["area"]
    floors = data["floors"]

    material = encode_material(data["material"])
    location = encode_location(data["location"])
    quality = encode_quality(data["quality"])

    complexity = floors * 2 + area / 10000
    volatility = [0.2, 0.5, 0.4, 0.3][material]

    X = [[
        area,
        floors,
        material,
        location,
        quality,
        complexity,
        volatility
    ]]

    risk = risk_model.predict(X)[0]

    return int(max(5, min(95, risk)))