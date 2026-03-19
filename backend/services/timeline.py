import joblib

timeline_model = joblib.load("backend/models/timeline_model.pkl")


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


def predict_timeline(data):

    area = data["area"]
    floors = data["floors"]

    material = encode_material(data["material"])
    location = encode_location(data["location"])

    complexity = floors * 2 + area / 10000

    X = [[area, floors, material, location, complexity]]

    duration = timeline_model.predict(X)[0]

    return round(duration, 1)

def generate_phases(duration):

    return [
        {"phase": "Site prep", "start": 0, "duration": 0.10 * duration},
        {"phase": "Foundation", "start": 0.10 * duration, "duration": 0.15 * duration},
        {"phase": "Structure", "start": 0.25 * duration, "duration": 0.30 * duration},
        {"phase": "MEP", "start": 0.50 * duration, "duration": 0.20 * duration},
        {"phase": "Finishing", "start": 0.70 * duration, "duration": 0.20 * duration},
        {"phase": "Handover", "start": 0.90 * duration, "duration": 0.10 * duration},
    ]