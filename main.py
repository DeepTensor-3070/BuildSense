"""
BuildSense AI v4.0 — main.py
FastAPI backend with:
  • /analyze              — ML models (cost + timeline + risk + DCS)
  • /ai/analyze           — GPT-4o powered cost + timeline + risk prediction
  • /ai/insights          — GPT-4o proactive project insights (3 cards)
  • /ai/cost-explain      — GPT-4o cost breakdown explanation
  • /ai/risk-explain      — GPT-4o 6-dimension risk explanation
  • /ai/timeline-explain  — GPT-4o timeline phase explanation
  • /ai/chat              — GPT-4o multi-turn construction chatbot
  • /prices               — live-simulated material ticker
  • /health               — version + openai status
"""

import random, time, os, sys, json
from typing import List, Optional

_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)
_root = os.path.dirname(_here)
if _root not in sys.path:
    sys.path.insert(0, _root)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# OpenAI 
try:
    from openai import AsyncOpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False

_ENV_KEY = os.getenv("OPENAI_API_KEY", "")

def _get_client(request_key: str = ""):
    if not _OPENAI_AVAILABLE:
        raise HTTPException(500, "openai package not installed — run: pip install openai")
    key = (request_key or "").strip() or _ENV_KEY
    if not key:
        raise HTTPException(400, "OpenAI API key required. Set OPENAI_API_KEY env var or pass openai_key in request body.")
    return AsyncOpenAI(api_key=key)

#  ML service stubs (replaced by your real models if they exist) 
try:
    from backend.services.cost import predict_cost
    from backend.services.timeline import predict_timeline, generate_phases
    from backend.services.risk import predict_risk
    from backend.services.dcs import predict_dcs
except ModuleNotFoundError:
    try:
        from services.cost import predict_cost
        from services.timeline import predict_timeline, generate_phases
        from services.risk import predict_risk
        from services.dcs import predict_dcs
    except ModuleNotFoundError:
        def predict_cost(d):
            mat = {"concrete":1.0,"steel frame":1.22,"timber":0.78,"composite":1.35}
            loc = {"urban":1.15,"semi-urban":0.92}
            qual = {"standard":1.0,"premium":1.28}
            base = d["area"]*d["floors"]*3500 * mat.get(d["material"].lower(),1.0) * loc.get(d["location"].lower(),1.0) * qual.get(d["quality"].lower(),1.0)
            return {"total_cost":round(base),"material_cost":round(base*.48),"labor_cost":round(base*.30),"overhead":round(base*.14),"contingency":round(base*.08)}

        def predict_timeline(d):
            return float(max(10, round(d["floors"]*3 + d["area"]/3000)))

        def generate_phases(dur):
            names=["Site prep","Foundation","Structure","MEP","Finishing","Handover"]
            pcts=[0.08,0.18,0.30,0.20,0.17,0.07]
            phases,start=[],0
            for n,p in zip(names,pcts):
                l=max(1,round(dur*p)); phases.append({"phase":n,"start":start,"duration":l}); start+=l
            return phases

        def predict_risk(d):
            base=d["area"]/2000+d["floors"]*2
            if d["location"].lower()=="urban": base+=3
            if d["material"].lower()=="timber": base+=5
            return max(10,min(60,round(base)))

        def predict_dcs(d,total,risk):
            return max(55,min(95,100-risk+8))

# App 
app = FastAPI(title="BuildSense AI API", version="4.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

_frontend_dir = os.path.join(_root, "frontend")
if os.path.isdir(_frontend_dir):
    @app.get("/", include_in_schema=False)
    def serve_index():
        return FileResponse(os.path.join(_frontend_dir, "index.html"))


# Schemas 
class ProjectInput(BaseModel):
    area: int; floors: int; material: str; location: str; quality: str

class AIProjectInput(BaseModel):
    area: int; floors: int; material: str; location: str; quality: str
    cost: float = 0.0; duration: float = 0.0; risk: int = 0; dcs: int = 0
    material_cost: float = 0.0; labor_cost: float = 0.0
    overhead: float = 0.0; contingency: float = 0.0
    openai_key: Optional[str] = ""

class ChatMessage(BaseModel):
    role: str; content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    area: int = 8000; floors: int = 4; material: str = "Concrete"
    location: str = "Urban"; quality: str = "Standard"
    cost: float = 2.4; duration: float = 18.0; risk: int = 22; dcs: int = 78
    openai_key: Optional[str] = ""


# Shared helpers 
BASE_SYS = """You are BuildSense AI, an expert construction intelligence assistant for Indian projects.
Standards: IS 456:2000 (RCC), IS 800 (Steel), IS 875 (Loads), IS 1786 (TMT), CPWD DSR 2023-24 (North India).
Market rates: TMT Fe500D ₹62,400/MT · M25 concrete ₹5,800/m³ · Cement ₹420/bag · River Sand ₹1,950/m³ · Skilled labour ₹850/day · Bricks ₹8,200/1000.
Regional: North Indian alluvial soil · Monsoon Jun-Sep · Seismic zones II-III.
Always cite IS clauses, DSR rates, ₹ figures. Be concise and expert."""

def _ctx(d):
    return (f"Project: {d.get('area',0):,} sqft | {d.get('floors',0)} floors | {d.get('material','?')} | "
            f"{d.get('location','?')} India | {d.get('quality','?')}\n"
            f"Estimates: ₹{d.get('cost',0)} Cr | {d.get('duration',0)} mo | Risk {d.get('risk',0)}% | DCS {d.get('dcs',0)}/100\n"
            f"Costs: Mat ₹{d.get('material_cost',0)}Cr | Lab ₹{d.get('labor_cost',0)}Cr | OH ₹{d.get('overhead',0)}Cr | Cont ₹{d.get('contingency',0)}Cr")

async def _gpt_json(client, msgs, max_tokens=800):
    r = await client.chat.completions.create(model="gpt-4o", max_tokens=max_tokens, temperature=0.3,
        response_format={"type":"json_object"}, messages=msgs)
    try: return json.loads(r.choices[0].message.content or "{}")
    except: return {"raw": r.choices[0].message.content}

async def _gpt_text(client, msgs, max_tokens=600):
    r = await client.chat.completions.create(model="gpt-4o", max_tokens=max_tokens, temperature=0.4, messages=msgs)
    return r.choices[0].message.content or ""



# /analyze  — ML models (contract unchanged)

@app.post("/analyze")
def analyze(data: ProjectInput):
    d = data.dict()
    cd = predict_cost(d)
    dur = predict_timeline(d)
    phases = generate_phases(dur)
    risk = predict_risk(d)
    dcs = predict_dcs(d, cd["total_cost"], risk)
    total = cd["total_cost"]
    return {
        "cost":          round(total/1e7, 2),
        "duration":      round(dur, 1),
        "risk":          risk,
        "dcs":           dcs,
        "phases":        phases,
        "material_cost": round(cd.get("material_cost", total*.48)/1e7, 2),
        "labor_cost":    round(cd.get("labor_cost",    total*.30)/1e7, 2),
        "overhead":      round(cd.get("overhead",      total*.14)/1e7, 2),
        "contingency":   round(cd.get("contingency",   total*.08)/1e7, 2),
    }



# /ai/analyze  — GPT-4o predicts cost + timeline + risk in one call
@app.post("/ai/analyze")
async def ai_analyze(data: AIProjectInput):
    """GPT-4o replaces all three ML models. Returns same shape as /analyze plus ai_narrative."""
    client = _get_client(data.openai_key)
    d = data.dict()
    result = await _gpt_json(client, [
        {"role":"system","content": BASE_SYS + "\nRespond ONLY with valid JSON, no markdown."},
        {"role":"user","content": f"""You are the AI prediction engine for a construction cost estimator.
Input: {d['area']:,} sqft | {d['floors']} floors | {d['material']} | {d['location']} India | {d['quality']} grade

Return this exact JSON (all numeric fields must be valid numbers):
{{
  "cost": <total cost in Crores float 2dp>,
  "duration": <months float 1dp>,
  "risk": <overrun risk % integer 10-65>,
  "dcs": <Decision Confidence Score integer 55-95>,
  "material_cost": <Crores float>,
  "labor_cost": <Crores float>,
  "overhead": <Crores float>,
  "contingency": <Crores float>,
  "phases": [
    {{"phase":"Site prep",  "start":0,  "duration":<months int>}},
    {{"phase":"Foundation", "start":<n>,"duration":<months int>}},
    {{"phase":"Structure",  "start":<n>,"duration":<months int>}},
    {{"phase":"MEP",        "start":<n>,"duration":<months int>}},
    {{"phase":"Finishing",  "start":<n>,"duration":<months int>}},
    {{"phase":"Handover",   "start":<n>,"duration":<months int>}}
  ],
  "ai_narrative": "<2-3 sentence expert justification citing DSR 2023-24 rates>"
}}
Use CPWD DSR 2023-24 North India. Ensure material_cost+labor_cost+overhead+contingency equals cost."""}
    ], max_tokens=900)
    for f,v in [("cost",2.4),("duration",18.0),("risk",22),("dcs",75),("material_cost",1.15),("labor_cost",0.72),("overhead",0.34),("contingency",0.19)]:
        if f not in result: result[f]=v
    if "phases" not in result: result["phases"] = generate_phases(float(result["duration"]))
    return result



# /ai/cost-explain  — GPT-4o explains cost breakdown

@app.post("/ai/cost-explain")
async def ai_cost_explain(data: AIProjectInput):
    client = _get_client(data.openai_key)
    result = await _gpt_json(client, [
        {"role":"system","content": BASE_SYS + "\nRespond ONLY with valid JSON."},
        {"role":"user","content": f"""{_ctx(data.dict())}

Analyse this cost estimate. Return JSON:
{{
  "summary": "2-3 sentence expert verdict on ₹{data.cost} Cr, citing DSR 2023-24",
  "breakdown": "Insight on whether {data.material_cost}/{data.labor_cost}/{data.overhead} Cr material/labour/overhead split is typical for {data.material} in {data.location} India",
  "savings": ["Specific tip 1 with ₹ saving amount","Tip 2 with % reduction","Tip 3 procurement strategy"],
  "red_flags": ["Cost risk 1 specific to this project","Risk 2"],
  "confidence": "One sentence on estimate confidence given DCS {data.dcs}/100"
}}"""}
    ], max_tokens=700)
    return result



# /ai/risk-explain  — GPT-4o explains 6 risk dimensions

@app.post("/ai/risk-explain")
async def ai_risk_explain(data: AIProjectInput):
    client = _get_client(data.openai_key)
    result = await _gpt_json(client, [
        {"role":"system","content": BASE_SYS + "\nRespond ONLY with valid JSON."},
        {"role":"user","content": f"""{_ctx(data.dict())}

Perform 6-dimension risk analysis. Return JSON:
{{
  "summary": "2 sentences on overall {data.risk}% overrun risk for this project",
  "dimensions": [
    {{"name":"Budget",    "score":<0-100>,"reason":"specific cause","mitigation":"action with ₹ figure"}},
    {{"name":"Timeline",  "score":<0-100>,"reason":"specific cause","mitigation":"action"}},
    {{"name":"Materials", "score":<0-100>,"reason":"reference current market rates","mitigation":"procurement strategy"}},
    {{"name":"Labour",    "score":<0-100>,"reason":"at ₹850/day context","mitigation":"action"}},
    {{"name":"Weather",   "score":<0-100>,"reason":"monsoon Jun-Sep impact on {data.material}","mitigation":"specific action"}},
    {{"name":"Regulatory","score":<0-100>,"reason":"IS code compliance for {data.floors}-floor {data.material}","mitigation":"action"}}
  ],
  "strategy": "Top 2 risk mitigation priorities specific to this project"
}}"""}
    ], max_tokens=800)
    return result



# /ai/timeline-explain  — GPT-4o explains the project schedule

@app.post("/ai/timeline-explain")
async def ai_timeline_explain(data: AIProjectInput):
    client = _get_client(data.openai_key)
    result = await _gpt_json(client, [
        {"role":"system","content": BASE_SYS + "\nRespond ONLY with valid JSON."},
        {"role":"user","content": f"""{_ctx(data.dict())}

Analyse the {data.duration}-month schedule for this project. Return JSON:
{{
  "summary": "Expert assessment of {data.duration} months for {data.area:,} sqft {data.floors}-floor {data.material} in {data.location} India",
  "phases": [
    {{"phase":"Site prep",  "typical_duration":"2-3 weeks","ai_note":"key note","risk_flag":"delay risk or empty string"}},
    {{"phase":"Foundation", "typical_duration":"4-6 weeks","ai_note":"IS 456:2000 compliance note","risk_flag":"soil/monsoon risk or empty"}},
    {{"phase":"Structure",  "typical_duration":"X months", "ai_note":"{data.material}-specific note","risk_flag":"key risk or empty"}},
    {{"phase":"MEP",        "typical_duration":"X weeks",  "ai_note":"coordination note","risk_flag":"risk or empty"}},
    {{"phase":"Finishing",  "typical_duration":"X weeks",  "ai_note":"{data.quality} grade note","risk_flag":"risk or empty"}},
    {{"phase":"Handover",   "typical_duration":"2-3 weeks","ai_note":"statutory completion","risk_flag":"snag risk or empty"}}
  ],
  "critical_path": "Phase most likely to cause delay and specific reason",
  "monsoon_advice": "Specific Jun-Sep strategy for this {data.material} project",
  "acceleration_tips": ["Tip 1 to reduce duration","Tip 2 to reduce duration"]
}}"""}
    ], max_tokens=800)
    return result



# /ai/insights  — GPT-4o proactive insights (3 cards)

@app.post("/ai/insights")
async def ai_insights(data: AIProjectInput):
    client = _get_client(data.openai_key)
    result = await _gpt_json(client, [
        {"role":"system","content": BASE_SYS + "\nRespond ONLY with valid JSON."},
        {"role":"user","content": f"""{_ctx(data.dict())}

Generate exactly 3 proactive insights — one warning, one opportunity, one tip. Return JSON:
{{
  "insights": [
    {{"type":"warning",     "title":"5-7 word title","body":"2-3 sentences with ₹ figures and IS code refs","action":"One concrete action"}},
    {{"type":"opportunity", "title":"5-7 word title","body":"2-3 sentences with savings in ₹ or %","action":"One concrete action"}},
    {{"type":"tip",         "title":"5-7 word title","body":"2-3 sentences practical construction guidance","action":"One concrete action"}}
  ]
}}"""}
    ], max_tokens=700)
    return result



# /ai/chat  — GPT-4o multi-turn chatbot

@app.post("/ai/chat")
async def ai_chat(req: ChatRequest):
    client = _get_client(req.openai_key)
    system = (BASE_SYS +
        f"\n\nLIVE PROJECT: {req.area:,} sqft | {req.floors} floors | {req.material} | {req.location} India | {req.quality}"
        f"\nCost ₹{req.cost}Cr | Duration {req.duration}mo | Risk {req.risk}% | DCS {req.dcs}/100"
        "\n\nAnswer questions about this project. Max 200 words. Use line breaks. Cite IS codes. Include ₹ figures.")
    msgs = [{"role":"system","content":system}] + [{"role":m.role,"content":m.content} for m in req.messages]
    reply = await _gpt_text(client, msgs, max_tokens=600)
    return {"reply": reply}



# /prices  — live-simulated material ticker (unchanged)

_price_state = {
    "tmt":       {"label":"TMT Fe500D",    "value":62400,"unit":"/MT"},
    "cement":    {"label":"Cement 50kg",   "value":420,  "unit":"/bag"},
    "sand":      {"label":"River Sand",    "value":1950, "unit":"/m³"},
    "concrete":  {"label":"M25 Concrete",  "value":5800, "unit":"/m³"},
    "bricks":    {"label":"Bricks /1000",  "value":8200, "unit":"/1000"},
    "labour":    {"label":"Skilled Labour","value":850,  "unit":"/day"},
    "plywood":   {"label":"Plywood 18mm",  "value":1650, "unit":"/sh"},
    "aggregate": {"label":"Coarse Agg.",   "value":1200, "unit":"/m³"},
}
_last_price_tick = 0.0

def _fmt(v,u): return f"₹{v:,}{u}" if v>=1000 else f"₹{v}{u}"

@app.get("/prices")
def get_prices():
    global _last_price_tick
    if time.time()-_last_price_tick>2.8:
        for v in _price_state.values():
            chg=(random.random()-0.5)*0.02; v["value"]=round(v["value"]*(1+chg)); v["change_pct"]=round(chg*100,2)
        _last_price_tick=time.time()
    return {k:{**item,"display":_fmt(item["value"],item["unit"])} for k,item in _price_state.items()}


# /health
@app.get("/health")
def health():
    return {"status":"ok","version":"4.0","openai_ready": _OPENAI_AVAILABLE and bool(_ENV_KEY)}
