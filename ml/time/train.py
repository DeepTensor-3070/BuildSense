import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

def generate_timeline_data(n=100000):
    data = []

    for _ in range(n):
        area = np.random.randint(500, 50000)
        floors = np.random.randint(1, 15)

        material = np.random.choice([0,1,2,3])   # encoded
        location = np.random.choice([0,1])       # 0=urban delay, 1=normal

        # base duration
        base_duration = floors * 2 + area / 4000

        # material impact
        material_factor = [1.0, 0.8, 1.1, 0.9][material]

        # location delay
        location_factor = [1.2, 1.0][location]

        duration = base_duration * material_factor * location_factor

        # randomness
        duration *= np.random.uniform(0.9, 1.1)

        data.append([area, floors, material, location, duration])

    return pd.DataFrame(data, columns=[
        "area","floors","material","location","duration"
    ])


# Generate data
df = generate_timeline_data()

# Better feature engineering
df["complexity"] = (
    df["floors"] * 1.5 +
    df["area"] / 8000 +
    df["material"] * 0.5
)

# Features & target
X = df[["area","floors","material","location","complexity"]]
y = df["duration"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=8,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluation
score = model.score(X_test, y_test)
print(f"R2 Score: {score:.4f}")

# Save
joblib.dump(model, "timeline_model.pkl")
print("✅ Timeline model saved")
