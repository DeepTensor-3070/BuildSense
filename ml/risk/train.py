import pandas as pd
import numpy as np

def generate_risk_data(n=100000):

    data = []

    for _ in range(n):
        area = np.random.randint(500, 50000)
        floors = np.random.randint(1, 15)

        material = np.random.choice([0,1,2,3])
        location = np.random.choice([0,1])
        quality = np.random.choice([0,1])

        # feature engineering
        complexity = floors * 2 + area / 10000
        volatility = [0.2, 0.5, 0.4, 0.3][material]
        location_risk = [0.6, 0.3][location]
        quality_factor = [0.2, -0.1][quality]

        # risk formula
        risk = (
            complexity * 2 +
            volatility * 40 +
            location_risk * 30 +
            quality_factor * 20
        )

        # normalize
        risk = max(5, min(95, risk + np.random.uniform(-5, 5)))

        data.append([
            area, floors, material, location, quality,
            complexity, volatility, risk
        ])

    return pd.DataFrame(data, columns=[
        "area","floors","material","location","quality",
        "complexity","volatility","risk"
    ])

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

df = generate_risk_data()

X = df[[
    "area","floors","material","location","quality",
    "complexity","volatility"
]]

y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=8,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

joblib.dump(model, "risk_model.pkl")
print("✅ Risk model saved")