import random
import time
import os
import sys

# ── Fix imports regardless of where uvicorn is launched from ──
_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

_root = os.path.dirname(_here)
if _root not in sys.path:
    sys.path.insert(0, _root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Support both `uvicorn main:app` (from project root) and
# `uvicorn backend.main:app` (from parent of backend/)
try:
    from backend.services.cost import predict_cost
    from backend.services.timeline import predict_timeline, generate_phases
    from backend.services.risk import predict_risk
    from backend.services.dcs import predict_dcs
except ModuleNotFoundError:
    from services.cost import predict_cost
    from services.timeline import predict_timeline, generate_phases
    from services.risk import predict_risk
    from services.dcs import predict_dcs


# ─────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────

app = FastAPI(title="BuildSense AI API", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend/index.html at GET / if the folder exists
_frontend_dir = os.path.join(_root, "frontend")
if os.path.isdir(_frontend_dir):
    @app.get("/", include_in_schema=False)
    def serve_index():
        return FileResponse(os.path.join(_frontend_dir, "index.html"))


# ─────────────────────────────────────────────
# SCHEMA
# ─────────────────────────────────────────────

class ProjectInput(BaseModel):
    area: int
    floors: int
    material: str
    location: str
    quality: str


# ─────────────────────────────────────────────
# LIVE PRICE ENGINE
# ─────────────────────────────────────────────

_price_state = {
    "tmt":       {"label": "TMT Fe500D",     "value": 62400, "unit": "/MT"},
    "cement":    {"label": "Cement 50kg",    "value": 420,   "unit": "/bag"},
    "sand":      {"label": "River Sand",     "value": 1950,  "unit": "/m³"},
    "concrete":  {"label": "M25 Concrete",   "value": 5800,  "unit": "/m³"},
    "bricks":    {"label": "Bricks /1000",   "value": 8200,  "unit": "/1000"},
    "labour":    {"label": "Skilled Labour", "value": 850,   "unit": "/day"},
    "plywood":   {"label": "Plywood 18mm",   "value": 1650,  "unit": "/sh"},
    "aggregate": {"label": "Coarse Agg.",    "value": 1200,  "unit": "/m³"},
}

_last_price_tick = 0.0


def _fmt(value: int, unit: str) -> str:
    if value >= 1000:
        return f"₹{value:,}{unit}"
    return f"₹{value}{unit}"


@app.get("/prices")
def get_prices():
    """
    Returns live-simulated material prices.
    Frontend ticker reads: item.display, item.value, item.change_pct
    """
    global _last_price_tick

    if time.time() - _last_price_tick > 2.8:
        for v in _price_state.values():
            chg = (random.random() - 0.5) * 0.02
            v["value"]      = round(v["value"] * (1 + chg))
            v["change_pct"] = round(chg * 100, 2)
        _last_price_tick = time.time()

    return {
        key: {**item, "display": _fmt(item["value"], item["unit"])}
        for key, item in _price_state.items()
    }


# ─────────────────────────────────────────────
# HEALTH
# ─────────────────────────────────────────────

@app.get("/health")
def health():
    """
    Frontend reads: data.version
    Shows green banner when this returns 200.
    """
    return {
        "status":  "ok",
        "version": "4.0",
    }


# ─────────────────────────────────────────────
# ANALYZE  (the only ML endpoint the frontend uses)
# ─────────────────────────────────────────────

@app.post("/analyze")
def analyze(data: ProjectInput):
    """
    Frontend sends:
        { area, floors, material, location, quality }

    Frontend reads back:
        cost          → Total Cost card  (in Crores, e.g. 2.4)
        duration      → Duration card    (months)
        risk          → Risk Score card  (integer %)
        dcs           → DCS Score card   (0-100)
        material_cost → DCS panel + 3D chart sub-cost
        labor_cost    → DCS panel + 3D chart sub-cost
        overhead      → DCS panel + 3D chart sub-cost
        contingency   → DCS panel + 3D chart sub-cost
        phases        → Gantt chart      (list of {phase, start, duration})

    The What-if engine calls this endpoint a second time with an
    alternate material string to get the comparison column.
    """
    data_dict = data.dict()

    # ── Run ML models ──
    cost_data = predict_cost(data_dict)
    duration  = predict_timeline(data_dict)
    phases    = generate_phases(duration)
    risk      = predict_risk(data_dict)
    dcs       = predict_dcs(data_dict, cost_data["total_cost"], risk)

    total = cost_data["total_cost"]

    # ── Sub-costs ──
    # Use values from predict_cost if it returns them,
    # otherwise fall back to typical Indian construction ratios:
    # Materials 48% · Labour 30% · Overhead 14% · Contingency 8%
    mat_cost    = round(cost_data.get("material_cost", total * 0.48) / 1e7, 2)
    labour_cost = round(cost_data.get("labor_cost",    total * 0.30) / 1e7, 2)
    overhead    = round(cost_data.get("overhead",      total * 0.14) / 1e7, 2)
    contingency = round(cost_data.get("contingency",   total * 0.08) / 1e7, 2)

    return {
        # Health cards
        "cost":          round(total / 1e7, 2),
        "duration":      round(duration, 1),
        "risk":          risk,
        "dcs":           dcs,

        # Gantt
        "phases":        phases,

        # DCS panel + 3D chart + What-if
        "material_cost": mat_cost,
        "labor_cost":    labour_cost,
        "overhead":      overhead,
        "contingency":   contingency,
    }