from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from genai import generate_whatif_insight
from insights import generate_smart_insights
from material import get_live_material_prices, calculate_material_index
from chatbot import handle_query
from copilot import find_best_scenario, generate_copilot_advice, copilot_engine

import sys
import os

sys.path.append(os.path.abspath("../models"))
from predict import predict_all

app = FastAPI(
    title="BuildSense AI API",
    description="AI-powered construction intelligence system",
    version="1.0",
)

# Allow the Streamlit frontend (any local origin) to reach the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INPUT SCHEMA 
class ProjectInput(BaseModel):
    area: float
    material_quality: int
    location_factor: float
    labor_cost: float
    project_type: int
    floors: int
    soil_type: int
    weather_index: float
    material_price_index: float
    contractor_experience: int
    equipment_availability: float
    project_complexity: int
    permits_delay: int
    transport_cost: float
    inflation_factor: float
    cost_per_sqft_est: float
    labor_intensity: float
    efficiency: float


# VALIDATION HELPER 
def validate_result(result):
    required = ["estimated_cost", "estimated_time", "dcs_score"]
    for key in required:
        if key not in result:
            raise ValueError(f"Invalid model output: missing '{key}'")


# ROUTES 

@app.get("/")
def home():
    return {"message": "🚀 BuildSense AI API is running"}


@app.get("/health")
def health():
    """Health-check endpoint used by the Streamlit UI."""
    return {"status": "ok", "message": "BuildSense AI API is healthy"}


# SINGLE PREDICTION 
@app.post("/predict")
def predict(data: ProjectInput):
    try:
        features = data.model_dump()

        result = predict_all(features)
        validate_result(result)

        insights = generate_smart_insights(features, result)
        prices = get_live_material_prices()
        material_index = calculate_material_index(prices)
        features["material_price_index"] = material_index

        try:
            explanation = generate_whatif_insight(result, result, {})
        except Exception:
            explanation = ""

        return {
            "status": "success",
            "data": result,
            "insights": insights,
            "explanation": explanation,
            "materials": prices,
            "material_index": material_index,
            "message": "",
        }

    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "insights": [],
            "explanation": "",
            "materials": {},
            "material_index": 0,
            "message": str(e),
        }


# MULTI WHAT-IF ENGINE 
@app.post("/multi-what-if")
def multi_what_if(data: dict):
    try:
        base_input = data.get("base")
        scenarios  = data.get("scenarios", [])

        if not base_input:
            raise HTTPException(status_code=400, detail="Missing 'base' input")

        base_result = predict_all(base_input)
        validate_result(base_result)

        results = []

        for scenario in scenarios:
            name    = scenario.get("name", "Scenario")
            changes = scenario.get("changes", {})

            try:
                modified_input = {**base_input, **changes}
                modified_result = predict_all(modified_input)
                validate_result(modified_result)

                impact = {
                    "cost_change": round(
                        modified_result["estimated_cost"] - base_result["estimated_cost"], 2
                    ),
                    "time_change": round(
                        modified_result["estimated_time"] - base_result["estimated_time"], 2
                    ),
                    "dcs_change": round(
                        modified_result["dcs_score"] - base_result["dcs_score"], 2
                    ),
                }

                try:
                    insight = generate_whatif_insight(base_result, modified_result, impact)
                except Exception:
                    insight = ""

                results.append({
                    "scenario": name,
                    "changes":  changes,
                    "result":   modified_result,
                    "impact":   impact,
                    "insight":  insight,
                })

            except Exception as scenario_error:
                results.append({
                    "scenario": name,
                    "error":    str(scenario_error),
                })

        return {
            "status": "success",
            "data": {
                "base":      base_result,
                "scenarios": results,
            },
            "message": "",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# CHAT 
@app.post("/chat")
def chat(data: dict):
    user_input = data.get("message", "")
    features   = data.get("features", {})

    if not user_input:
        raise HTTPException(status_code=400, detail="Missing 'message'")

    try:
        response = handle_query(user_input, features)
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "response": "", "message": str(e)}


# AI COPILOT 
@app.post("/copilot")
def copilot(data: dict):
    try:
        base      = data.get("base")
        scenarios = data.get("scenarios", [])
        goal      = data.get("goal", "balanced")

        if not base:
            raise HTTPException(status_code=400, detail="Missing 'base' input")

        base_result = predict_all(base)
        validate_result(base_result)

        scenario_results = []

        for s in scenarios:
            modified = {**base, **s.get("changes", {})}
            result   = predict_all(modified)

            impact = {
                "cost_change": round(result["estimated_cost"] - base_result["estimated_cost"], 2),
                "time_change": round(result["estimated_time"] - base_result["estimated_time"], 2),
                "dcs_change":  round(result["dcs_score"]      - base_result["dcs_score"],      2),
            }

            scenario_results.append({
                "scenario": s.get("name", "Scenario"),
                "result":   result,
                "impact":   impact,
            })

        output = copilot_engine(base_result, scenario_results, goal)

        return {
            "status":          "success",
            "best":            output["best"],
            "ranked":          output["ranked"],
            "suggestions":     output["suggestions"],
            "llm_explanation": output["llm_explanation"],
        }

    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}
