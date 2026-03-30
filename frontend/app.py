import streamlit as st
import requests
import pandas as pd
import json
import time


# CONFIG
API_BASE   = "http://127.0.0.1:8000"
API_PREDICT = f"{API_BASE}/predict"
API_MULTI   = f"{API_BASE}/multi-what-if"
API_CHAT    = f"{API_BASE}/chat"
API_COPILOT = f"{API_BASE}/copilot"


# PAGE CONFIG
st.set_page_config(
    page_title="BuildSense AI",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏗️",
)

# GLOBAL CSS  — dark industrial + neon accent
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Rajdhani:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --bg0:    #0a0c10;
  --bg1:    #0f1218;
  --bg2:    #151a22;
  --bg3:    #1c2330;
  --border: #1e2d40;
  --accent: #00d4ff;
  --accent2:#ff6b35;
  --accent3:#7fff6e;
  --text0:  #e8edf5;
  --text1:  #8fa3bc;
  --text2:  #4a6080;
  --danger: #ff3c5a;
  --warn:   #ffb020;
  --ok:     #00e576;
}

html, body, [data-testid="stApp"] {
  background-color: var(--bg0) !important;
  font-family: 'DM Sans', sans-serif;
  color: var(--text0);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(160deg, #0d1117 0%, #0f1822 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text0) !important; }
[data-testid="stSidebar"] .stSlider > div > div > div { background: var(--accent) !important; }

/* ── Headings ── */
h1, h2, h3 { font-family: 'Rajdhani', sans-serif !important; letter-spacing: 0.04em; }
h1 { font-size: 2.4rem !important; font-weight: 700 !important; color: var(--text0) !important; }
h2 { color: var(--accent) !important; font-size: 1.5rem !important; }
h3 { color: var(--text0) !important; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  padding: 1rem 1.2rem !important;
}
[data-testid="metric-container"] label { color: var(--text1) !important; font-family: 'Space Mono', monospace !important; font-size: 0.7rem !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--accent) !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1.8rem !important; font-weight: 700 !important; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-family: 'Space Mono', monospace !important; font-size: 0.72rem !important; }

/* ── Buttons ── */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--accent) !important;
  color: var(--accent) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.08em !important;
  border-radius: 6px !important;
  padding: 0.5rem 1.4rem !important;
  transition: all 0.2s ease !important;
}
.stButton > button:hover {
  background: var(--accent) !important;
  color: var(--bg0) !important;
  box-shadow: 0 0 18px rgba(0,212,255,0.4) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
  gap: 4px;
  border-bottom: 1px solid var(--border) !important;
  background: transparent !important;
}
[data-testid="stTabs"] button[role="tab"] {
  font-family: 'Space Mono', monospace !important;
  font-size: 0.72rem !important;
  color: var(--text1) !important;
  border-radius: 6px 6px 0 0 !important;
  padding: 0.5rem 1.2rem !important;
  background: var(--bg1) !important;
  border: 1px solid var(--border) !important;
  border-bottom: none !important;
  letter-spacing: 0.06em;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
  color: var(--accent) !important;
  background: var(--bg2) !important;
  border-color: var(--accent) !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 8px !important; border-left-width: 3px !important; }
div[data-baseweb="notification"] { background: var(--bg2) !important; border-color: var(--accent) !important; }

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stSelectbox select {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text0) !important;
  border-radius: 6px !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 8px rgba(0,212,255,0.25) !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text0) !important;
  font-family: 'Rajdhani', sans-serif !important;
}

/* ── Dataframes ── */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Custom card ── */
.bs-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 0.8rem;
}
.bs-card-accent { border-left: 3px solid var(--accent); }
.bs-card-warn   { border-left: 3px solid var(--warn); }
.bs-card-ok     { border-left: 3px solid var(--ok); }
.bs-card-danger { border-left: 3px solid var(--danger); }

.bs-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.68rem;
  font-family: 'Space Mono', monospace;
  letter-spacing: 0.06em;
}
.bs-badge-ok     { background: rgba(0,229,118,0.12); color: var(--ok); border: 1px solid var(--ok); }
.bs-badge-warn   { background: rgba(255,176,32,0.12); color: var(--warn); border: 1px solid var(--warn); }
.bs-badge-danger { background: rgba(255,60,90,0.12);  color: var(--danger); border: 1px solid var(--danger); }

.section-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text1);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 0.8rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.4rem;
}

.mono { font-family: 'Space Mono', monospace; font-size: 0.82rem; }
.label-sm { font-size: 0.7rem; color: var(--text1); font-family: 'Space Mono', monospace; letter-spacing: 0.06em; text-transform: uppercase; }

/* insight pill */
.insight-pill {
  background: rgba(255,176,32,0.08);
  border: 1px solid rgba(255,176,32,0.3);
  border-radius: 8px;
  padding: 0.5rem 0.9rem;
  margin: 0.35rem 0;
  font-size: 0.83rem;
  color: #f0c060;
}

/* chat bubbles */
.chat-user {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 12px 12px 2px 12px;
  padding: 0.6rem 1rem;
  margin: 0.4rem 0;
  font-size: 0.87rem;
  max-width: 80%;
  margin-left: auto;
}
.chat-ai {
  background: rgba(0,212,255,0.06);
  border: 1px solid rgba(0,212,255,0.18);
  border-radius: 12px 12px 12px 2px;
  padding: 0.6rem 1rem;
  margin: 0.4rem 0;
  font-size: 0.87rem;
  max-width: 80%;
  color: var(--text0);
}

/* rank item */
.rank-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.6rem 1rem;
  margin: 0.3rem 0;
}
.rank-num {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text2);
  min-width: 28px;
}
.rank-num.gold   { color: #ffd700; }
.rank-num.silver { color: #b0b8c8; }
.rank-num.bronze { color: #cd7f32; }

/* material price bar */
.mat-bar-outer {
  background: var(--bg3);
  border-radius: 4px;
  height: 8px;
  width: 100%;
  overflow: hidden;
  margin-top: 4px;
}
.mat-bar-inner {
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
}

/* status dot */
.dot-ok     { width:8px; height:8px; border-radius:50%; background:var(--ok);     display:inline-block; box-shadow: 0 0 6px var(--ok); }
.dot-warn   { width:8px; height:8px; border-radius:50%; background:var(--warn);   display:inline-block; box-shadow: 0 0 6px var(--warn); }
.dot-danger { width:8px; height:8px; border-radius:50%; background:var(--danger); display:inline-block; box-shadow: 0 0 6px var(--danger); }

/* progress track */
.progress-track {
  background: var(--bg3);
  border-radius: 20px;
  height: 10px;
  width: 100%;
  overflow: hidden;
  margin: 4px 0 10px 0;
}
.progress-fill {
  height: 10px;
  border-radius: 20px;
  transition: width 0.5s ease;
}
.progress-fill.ok     { background: linear-gradient(90deg, #00e576, #00b4d8); }
.progress-fill.warn   { background: linear-gradient(90deg, #ffb020, #ff6b35); }
.progress-fill.danger { background: linear-gradient(90deg, #ff3c5a, #ff6b35); }

.header-logo {
  font-family: 'Rajdhani', sans-serif;
  font-size: 2.2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #00d4ff 0%, #7fff6e 60%, #ff6b35 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.04em;
}
.header-sub {
  font-family: 'Space Mono', monospace;
  font-size: 0.72rem;
  color: var(--text2);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-top: -6px;
}

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg1); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* hide streamlit chrome */
#MainMenu { display:none; }
footer    { display:none; }
header    { display:none; }
</style>
""", unsafe_allow_html=True)

# HELPERS
def api_post(url, payload, timeout=15):
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "⚠️ Cannot connect to BuildSense API. Make sure the FastAPI server is running on port 8000."
    except requests.exceptions.Timeout:
        return None, "⏱️ API request timed out."
    except Exception as e:
        return None, f"API Error: {str(e)}"

def health_check():
    try:
        r = requests.get(API_BASE + "/", timeout=3)
        return r.status_code == 200
    except:
        return False

def fmt_inr(val):
    if val >= 1_00_00_000:
        return f"₹{val/1_00_00_000:.2f} Cr"
    elif val >= 1_00_000:
        return f"₹{val/1_00_000:.2f} L"
    return f"₹{val:,.0f}"

def risk_color(label):
    l = str(label).lower()
    if "low"  in l: return "ok"
    if "high" in l: return "danger"
    return "warn"

def dcs_color(score):
    if score >= 80: return "ok"
    if score >= 50: return "warn"
    return "danger"

def simple_bar_html(val, max_val, cls):
    pct = min(100, int(val / max_val * 100))
    return f"""
<div class="progress-track">
  <div class="progress-fill {cls}" style="width:{pct}%"></div>
</div>"""

# SESSION STATE
defaults = {
    "result": None,
    "result_full": None,
    "scenario_results": None,
    "copilot_data": None,
    "chat_history": [],
    "prediction_history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# SIDEBAR
with st.sidebar:
    # Logo
    st.markdown('<div class="header-logo">⬡ BuildSense</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub">Construction Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    # API status
    api_ok = health_check()
    status_html = (
        '<span class="dot-ok"></span> &nbsp;API Online'
        if api_ok else
        '<span class="dot-danger"></span> &nbsp;API Offline'
    )
    st.markdown(f'<div class="bs-card mono" style="padding:0.6rem 1rem">{status_html}</div>', unsafe_allow_html=True)
    st.markdown("")

    st.markdown('<div class="section-title">📥 Project Inputs</div>', unsafe_allow_html=True)

    area                 = st.number_input("Area (sq ft)",           value=1500,   step=100)
    material_quality     = st.selectbox("Material Quality",          [1, 2, 3], index=1,
                                         format_func=lambda x: {1:"Economy",2:"Standard",3:"Premium"}[x])
    location_factor      = st.slider("Location Factor",              0.5, 2.0, 1.3, 0.05)
    labor_cost           = st.number_input("Labor Cost (₹)",         value=60000,  step=5000)
    project_type         = st.selectbox("Project Type",              [1, 2, 3], index=0,
                                         format_func=lambda x: {1:"Residential",2:"Commercial",3:"Industrial"}[x])
    floors               = st.number_input("Floors",                 value=2,      min_value=1)
    soil_type            = st.selectbox("Soil Type",                 [1, 2, 3], index=0,
                                         format_func=lambda x: {1:"Good",2:"Average",3:"Poor"}[x])
    weather_index        = st.slider("Weather Risk Index",           0.0, 1.0, 0.4, 0.05)
    material_price_index = st.slider("Material Price Index",         0.5, 2.0, 1.2, 0.05)
    contractor_experience= st.number_input("Contractor Exp. (yrs)", value=5,      min_value=0)
    equipment_availability=st.slider("Equipment Availability",       0.0, 1.0, 0.8, 0.05)
    project_complexity   = st.selectbox("Project Complexity",        [1, 2, 3], index=1,
                                         format_func=lambda x: {1:"Simple",2:"Moderate",3:"Complex"}[x])
    permits_delay        = st.number_input("Permit Delays (days)",   value=5,      min_value=0)
    transport_cost       = st.number_input("Transport Cost (₹)",     value=20000,  step=1000)
    inflation_factor     = st.slider("Inflation Factor",             0.5, 2.0, 1.1, 0.05)
    cost_per_sqft_est    = st.number_input("Cost / sq ft (₹)",      value=2.4,    step=0.1, format="%.1f")
    labor_intensity      = st.number_input("Labor Intensity",        value=40,     min_value=0)
    efficiency           = st.slider("Contractor Efficiency",        0.0, 5.0, 4.0, 0.1)

base_payload = {
    "area": area, "material_quality": material_quality,
    "location_factor": location_factor, "labor_cost": labor_cost,
    "project_type": project_type, "floors": floors, "soil_type": soil_type,
    "weather_index": weather_index, "material_price_index": material_price_index,
    "contractor_experience": contractor_experience,
    "equipment_availability": equipment_availability,
    "project_complexity": project_complexity, "permits_delay": permits_delay,
    "transport_cost": transport_cost, "inflation_factor": inflation_factor,
    "cost_per_sqft_est": cost_per_sqft_est, "labor_intensity": labor_intensity,
    "efficiency": efficiency,
}

# HEADER
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<div class="header-logo" style="font-size:2.6rem">⬡ BuildSense AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub" style="font-size:0.68rem">AI-Powered Construction Decision Intelligence · v1.0</div>', unsafe_allow_html=True)
with col_h2:
    if not api_ok:
        st.warning("API Offline", icon="⚠️")
    else:
        st.success("API Ready", icon="✅")

st.markdown("---")

# TABS
tab_dash, tab_predict, tab_whatif, tab_chat, tab_copilot = st.tabs([
    "📊  DASHBOARD",
    "🔮  PREDICT",
    "🧪  WHAT-IF",
    "💬  CHAT",
    "🤖  COPILOT",
])

# TAB 1 — DASHBOARD
with tab_dash:
    st.markdown("## Analytics Dashboard")

    has_data = st.session_state.result is not None

    # KPI Row 
    r = st.session_state.result or {}
    full = st.session_state.result_full or {}

    if has_data:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("💰 Est. Cost",  fmt_inr(r.get("estimated_cost", 0)))
        c2.metric("⏱ Timeline",   f"{r.get('estimated_time', 0):.0f} d")
        c3.metric("📊 DCS Score",  f"{r.get('dcs_score', 0)}")
        c4.metric("🌡 Risk",       r.get("risk", {}).get("label", "—"))
        c5.metric("📐 Area",       f"{area:,} sq ft")
        st.markdown("")
    else:
        st.markdown("""
<div class="bs-card bs-card-accent" style="text-align:center;padding:2rem">
  <div style="font-family:'Rajdhani',sans-serif;font-size:1.4rem;color:#00d4ff">
    Run a prediction to populate the dashboard
  </div>
  <div class="label-sm" style="margin-top:0.4rem">
    Use the PREDICT tab → click Analyse Project
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("---")

    #Two columns layout 
    left, right = st.columns([3, 2], gap="medium")

    with left:
        # ── Risk Gauge ──
        st.markdown('<div class="section-title">Risk Gauge</div>', unsafe_allow_html=True)
        if has_data:
            risk_info = r.get("risk", {})
            conf = risk_info.get("confidence", 0.5)
            label = risk_info.get("label", "Medium")
            rc = risk_color(label)
            st.markdown(f"""
<div class="bs-card">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
    <div><span class="dot-{rc}"></span> &nbsp;<b style="font-family:'Rajdhani',sans-serif;font-size:1.1rem">{label} Risk</b></div>
    <div class="mono" style="color:var(--text1)">{conf*100:.0f}% confidence</div>
  </div>
  {simple_bar_html(conf, 1.0, rc)}
</div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="bs-card" style="color:var(--text2)">No data yet.</div>', unsafe_allow_html=True)

        # ── DCS Score ──
        st.markdown('<div class="section-title">Decision Confidence Score</div>', unsafe_allow_html=True)
        if has_data:
            dcs = r.get("dcs_score", 0)
            dc = dcs_color(dcs)
            st.markdown(f"""
<div class="bs-card">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
    <div style="font-family:'Rajdhani',sans-serif;font-size:2.4rem;font-weight:700;color:{'#00e576' if dc=='ok' else '#ffb020' if dc=='warn' else '#ff3c5a'}">{dcs}</div>
    <div class="label-sm">out of 100</div>
  </div>
  {simple_bar_html(dcs, 100, dc)}
  <div class="label-sm" style="margin-top:4px">
    {'Excellent — proceed with confidence' if dcs>=80 else 'Moderate — review inputs' if dcs>=50 else 'Low — high uncertainty'}
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="bs-card" style="color:var(--text2)">No data yet.</div>', unsafe_allow_html=True)

        # ── Insights Summary ──
        st.markdown('<div class="section-title">Smart Insights</div>', unsafe_allow_html=True)
        insights = full.get("insights", [])
        if insights:
            for ins in insights:
                st.markdown(f'<div class="insight-pill">{ins}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="bs-card" style="color:var(--text2)">Run a prediction to see insights.</div>', unsafe_allow_html=True)

    with right:
        # ── Material Prices ──
        st.markdown('<div class="section-title">Live Material Prices</div>', unsafe_allow_html=True)
        materials = full.get("materials", {})
        base_prices = {"cement": 350, "steel": 60, "sand": 50, "aggregate": 40}
        units = {"cement": "₹/bag", "steel": "₹/kg", "sand": "₹/cu.ft", "aggregate": "₹/cu.ft"}

        if materials:
            for mat, price in materials.items():
                base = base_prices.get(mat, price)
                delta_pct = ((price - base) / base) * 100
                arrow = "▲" if delta_pct > 0 else "▼"
                col_arrow = "#ff3c5a" if delta_pct > 0 else "#00e576"
                pct_bar = min(100, int((price / (base * 1.5)) * 100))
                st.markdown(f"""
<div class="bs-card" style="padding:0.7rem 1rem;margin-bottom:0.5rem">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <span style="font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:600">{mat.upper()}</span>
    <span class="label-sm" style="color:var(--text1)">{units.get(mat,'')}</span>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin:4px 0">
    <span style="font-family:'Space Mono',monospace;font-size:1.1rem;color:var(--accent)">₹{price:.1f}</span>
    <span style="font-size:0.75rem;color:{col_arrow}">{arrow} {abs(delta_pct):.1f}%</span>
  </div>
  <div class="mat-bar-outer"><div class="mat-bar-inner" style="width:{pct_bar}%"></div></div>
</div>""", unsafe_allow_html=True)

            mi = full.get("material_index", 0)
            mi_col = "#ff3c5a" if mi > 1.15 else "#ffb020" if mi > 1.05 else "#00e576"
            st.markdown(f"""
<div class="bs-card bs-card-accent mono" style="padding:0.6rem 1rem">
  Material Price Index &nbsp;<b style="color:{mi_col}">{mi:.3f}</b>
  {'  ⚠️ Elevated' if mi > 1.1 else '  ✅ Normal'}
</div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="bs-card" style="color:var(--text2)">No material data yet. Run a prediction.</div>', unsafe_allow_html=True)

        # ── Project Fingerprint ──
        st.markdown("")
        st.markdown('<div class="section-title">Project Fingerprint</div>', unsafe_allow_html=True)
        factors = {
            "Location Factor": (location_factor, 0.5, 2.0),
            "Weather Risk":    (weather_index,   0.0, 1.0),
            "Equipment Avail": (equipment_availability, 0.0, 1.0),
            "Efficiency":      (efficiency / 5,  0.0, 1.0),
            "Inflation":       (inflation_factor, 0.5, 2.0),
        }
        for name, (val, lo, hi) in factors.items():
            norm = (val - lo) / (hi - lo)
            fc = "ok" if norm < 0.4 else "warn" if norm < 0.7 else "danger"
            st.markdown(f"""
<div style="margin:4px 0">
  <div style="display:flex;justify-content:space-between" class="label-sm">
    <span>{name}</span><span>{val:.2f}</span>
  </div>
  {simple_bar_html(norm, 1.0, fc)}
</div>""", unsafe_allow_html=True)

    # ── Scenario History ──
    st.markdown("---")
    st.markdown('<div class="section-title">Scenario Comparison History</div>', unsafe_allow_html=True)

    scenario_data = st.session_state.scenario_results
    if scenario_data and scenario_data.get("status") == "success":
        sc_list = scenario_data["data"]["scenarios"]
        if sc_list:
            df_rows = []
            for sc in sc_list:
                if "result" in sc:
                    df_rows.append({
                        "Scenario":    sc["scenario"],
                        "Cost (₹L)":  round(sc["result"]["estimated_cost"] / 1_00_000, 2),
                        "Time (days)": sc["result"]["estimated_time"],
                        "DCS":         sc["result"]["dcs_score"],
                        "Cost Δ":      sc["impact"]["cost_change"],
                        "Time Δ":      sc["impact"]["time_change"],
                    })
            if df_rows:
                df_hist = pd.DataFrame(df_rows)
                st.dataframe(
                    df_hist.style.background_gradient(subset=["DCS"], cmap="RdYlGn")
                              .background_gradient(subset=["Cost (₹L)"], cmap="RdYlGn_r"),
                    use_container_width=True,
                )
                # Bar chart
                chart_df = df_hist.set_index("Scenario")[["Cost (₹L)", "Time (days)", "DCS"]]
                st.bar_chart(chart_df, use_container_width=True)
    else:
        st.markdown('<div class="bs-card" style="color:var(--text2)">Run What-If analysis to see scenario comparison.</div>', unsafe_allow_html=True)

# TAB 2 — PREDICT
with tab_predict:
    st.markdown("## Base Project Prediction")
    st.markdown('<div class="label-sm" style="margin-bottom:1rem">Configure inputs in the sidebar, then run the analysis.</div>', unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run = st.button("🔮  Analyse Project", key="btn_predict")

    if run:
        if not api_ok:
            st.error("API is offline. Please start the FastAPI server.", icon="🔴")
        else:
            with st.spinner("Running prediction engines..."):
                data, err = api_post(API_PREDICT, base_payload)

            if err:
                st.error(err)
            elif data.get("status") != "success":
                st.error(data.get("message", "Unknown error from API"))
            else:
                st.session_state.result      = data["data"]
                st.session_state.result_full = data
                # push to history
                st.session_state.prediction_history.append({
                    **base_payload,
                    **data["data"],
                })
                st.success("✅ Analysis complete! Head to the Dashboard for full analytics.")

    if st.session_state.result:
        r = st.session_state.result
        full = st.session_state.result_full

        st.markdown("---")
        # KPI row
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💰 Estimated Cost",     fmt_inr(r["estimated_cost"]))
        c2.metric("⏱ Estimated Timeline", f"{r['estimated_time']:.0f} days")
        c3.metric("📊 DCS Score",          f"{r['dcs_score']} / 100")
        c4.metric("🌡 Risk Level",         r["risk"]["label"])

        st.markdown("")

        left2, right2 = st.columns(2, gap="medium")

        with left2:
            # Risk breakdown
            st.markdown('<div class="section-title">Risk Analysis</div>', unsafe_allow_html=True)
            conf = r["risk"]["confidence"]
            rc = risk_color(r["risk"]["label"])
            st.markdown(f"""
<div class="bs-card bs-card-{rc}">
  <div class="label-sm">Risk Level</div>
  <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;font-weight:700">{r["risk"]["label"]}</div>
  <div class="label-sm" style="margin-top:6px">Confidence: {conf*100:.0f}%</div>
  {simple_bar_html(conf, 1.0, rc)}
</div>""", unsafe_allow_html=True)

            # Insights
            st.markdown('<div class="section-title">Smart Insights</div>', unsafe_allow_html=True)
            for ins in full.get("insights", []):
                st.markdown(f'<div class="insight-pill">{ins}</div>', unsafe_allow_html=True)
            if not full.get("insights"):
                st.markdown('<div class="bs-card bs-card-ok mono" style="font-size:0.82rem">✅ No critical warnings detected.</div>', unsafe_allow_html=True)

        with right2:
            # AI explanation
            explanation = full.get("explanation", "")
            st.markdown('<div class="section-title">AI Explanation</div>', unsafe_allow_html=True)
            if explanation:
                st.markdown(f'<div class="bs-card bs-card-accent" style="font-size:0.87rem;line-height:1.6">{explanation}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="bs-card" style="color:var(--text2)">No AI explanation available.</div>', unsafe_allow_html=True)

            # Material index
            st.markdown('<div class="section-title">Material Index</div>', unsafe_allow_html=True)
            mi = full.get("material_index", 0)
            mi_col = "danger" if mi > 1.15 else "warn" if mi > 1.05 else "ok"
            st.markdown(f"""
<div class="bs-card bs-card-{mi_col}">
  <div class="label-sm">Current Material Price Index</div>
  <div style="font-family:'Rajdhani',sans-serif;font-size:2.2rem;font-weight:700">{mi:.4f}</div>
  {simple_bar_html(mi - 0.5, 1.5, mi_col)}
</div>""", unsafe_allow_html=True)

        # Cost breakdown estimate table
        st.markdown('<div class="section-title">Input Summary</div>', unsafe_allow_html=True)
        summary_data = {
            "Parameter": ["Area", "Floors", "Labor Cost", "Transport", "Location Factor", "Inflation", "Efficiency", "Weather Risk"],
            "Value":     [f"{area} sq ft", str(floors), fmt_inr(labor_cost), fmt_inr(transport_cost),
                          f"{location_factor:.2f}", f"{inflation_factor:.2f}", f"{efficiency:.1f}/5", f"{weather_index:.2f}"],
        }
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    else:
        st.markdown("""
<div class="bs-card bs-card-accent" style="text-align:center;padding:2.5rem;margin-top:1rem">
  <div style="font-family:'Rajdhani',sans-serif;font-size:1.3rem;color:var(--accent)">
    Configure inputs in the sidebar and click Analyse Project
  </div>
</div>""", unsafe_allow_html=True)

# TAB 3 — WHAT-IF
with tab_whatif:
    st.markdown("## Multi-Scenario What-If Engine")
    st.markdown('<div class="label-sm" style="margin-bottom:1rem">Build multiple project scenarios and compare their outcomes side-by-side.</div>', unsafe_allow_html=True)

    num_scenarios = st.slider("Number of Scenarios", 1, 5, 2, key="num_sc")
    scenarios = []

    for i in range(num_scenarios):
        with st.expander(f"⚙️  Scenario {i+1}", expanded=(i == 0)):
            sc_c1, sc_c2, sc_c3, sc_c4 = st.columns(4)
            with sc_c1:
                name     = st.text_input("Name",         f"Scenario {i+1}", key=f"sc_name_{i}")
                floors_s = st.number_input("Floors",      value=floors,      key=f"sc_f_{i}")
            with sc_c2:
                labor_s  = st.number_input("Labor Cost",  value=labor_cost,  key=f"sc_l_{i}")
                weather_s= st.slider("Weather Risk", 0.0, 1.0, weather_index, 0.05, key=f"sc_w_{i}")
            with sc_c3:
                mat_q_s  = st.selectbox("Mat. Quality", [1,2,3], index=material_quality-1,
                                         format_func=lambda x:{1:"Economy",2:"Standard",3:"Premium"}[x], key=f"sc_mq_{i}")
                infl_s   = st.slider("Inflation",    0.5, 2.0, inflation_factor, 0.05, key=f"sc_inf_{i}")
            with sc_c4:
                eff_s    = st.slider("Efficiency",   0.0, 5.0, efficiency,      0.1,  key=f"sc_eff_{i}")

            scenarios.append({
                "name": name,
                "changes": {
                    "floors": floors_s, "labor_cost": labor_s,
                    "weather_index": weather_s, "material_quality": mat_q_s,
                    "inflation_factor": infl_s, "efficiency": eff_s,
                },
            })

    col_wbtn, _ = st.columns([1, 3])
    with col_wbtn:
        run_what = st.button("🧪  Run Analysis", key="btn_whatif")

    if run_what:
        if not api_ok:
            st.error("API is offline.", icon="🔴")
        else:
            with st.spinner("Simulating scenarios..."):
                data, err = api_post(API_MULTI, {"base": base_payload, "scenarios": scenarios})

            if err:
                st.error(err)
            elif data.get("status") != "success":
                st.error(data.get("message", "API error"))
            else:
                st.session_state.scenario_results = data
                st.success("✅ Scenarios complete! See Dashboard for combined analytics.")

    if st.session_state.scenario_results:
        sdata = st.session_state.scenario_results
        if sdata.get("status") == "success":
            sc_list = sdata["data"]["scenarios"]
            base_r  = sdata["data"]["base"]

            st.markdown("---")

            # Best scenario badge
            valid = [s for s in sc_list if "result" in s]
            if valid:
                best = max(valid, key=lambda x: x["result"]["dcs_score"])
                st.markdown(f"""
<div class="bs-card bs-card-ok" style="display:flex;align-items:center;gap:1rem">
  <span style="font-size:1.6rem">🏆</span>
  <div>
    <div class="label-sm">Best Scenario</div>
    <div style="font-family:'Rajdhani',sans-serif;font-size:1.3rem;font-weight:700">{best['scenario']}</div>
    <div class="label-sm">DCS: {best['result']['dcs_score']} · Cost: {fmt_inr(best['result']['estimated_cost'])} · Time: {best['result']['estimated_time']:.0f}d</div>
  </div>
</div>""", unsafe_allow_html=True)

            # Comparison grid
            st.markdown("")
            n_cols = min(len(valid), 3)
            cols_grid = st.columns(n_cols) if n_cols > 0 else []
            for idx, sc in enumerate(valid):
                with cols_grid[idx % n_cols]:
                    imp   = sc["impact"]
                    c_col = "danger" if imp["cost_change"] > 0 else "ok"
                    t_col = "danger" if imp["time_change"] > 0 else "ok"
                    d_col = "ok"     if imp["dcs_change"]  > 0 else "danger"
                    dcs_sc = sc["result"]["dcs_score"]
                    dc     = dcs_color(dcs_sc)
                    st.markdown(f"""
<div class="bs-card" style="border-top:3px solid var(--accent)">
  <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:0.8rem">{sc['scenario']}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;margin-bottom:0.8rem">
    <div class="bs-card" style="padding:0.5rem 0.7rem;margin:0">
      <div class="label-sm">Cost</div>
      <div class="mono" style="font-size:0.9rem">{fmt_inr(sc['result']['estimated_cost'])}</div>
    </div>
    <div class="bs-card" style="padding:0.5rem 0.7rem;margin:0">
      <div class="label-sm">Time</div>
      <div class="mono" style="font-size:0.9rem">{sc['result']['estimated_time']:.0f}d</div>
    </div>
  </div>
  <div class="label-sm">DCS</div>
  {simple_bar_html(dcs_sc, 100, dc)}
  <div style="margin:0.6rem 0 0.3rem" class="label-sm">Changes vs Base</div>
  <div>
    <span class="bs-badge bs-badge-{c_col}">Cost {'+' if imp['cost_change']>=0 else ''}{fmt_inr(imp['cost_change'])}</span>&nbsp;
    <span class="bs-badge bs-badge-{t_col}">Time {'+' if imp['time_change']>=0 else ''}{imp['time_change']:.0f}d</span>&nbsp;
    <span class="bs-badge bs-badge-{d_col}">DCS {'+' if imp['dcs_change']>=0 else ''}{imp['dcs_change']:.1f}</span>
  </div>
  {"<div class='insight-pill' style='margin-top:0.6rem;font-size:0.8rem'>"+sc['insight'][:180]+"…</div>" if sc.get('insight') else ''}
</div>""", unsafe_allow_html=True)

            # Comparison chart
            st.markdown('<div class="section-title" style="margin-top:1rem">Comparative Chart</div>', unsafe_allow_html=True)
            df_chart = pd.DataFrame([
                {
                    "Scenario":    sc["scenario"],
                    "Cost (₹L)":  round(sc["result"]["estimated_cost"] / 1_00_000, 2),
                    "Time (days)": sc["result"]["estimated_time"],
                    "DCS Score":   sc["result"]["dcs_score"],
                }
                for sc in valid
            ]).set_index("Scenario")
            st.bar_chart(df_chart, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 — CHAT
# ══════════════════════════════════════════════
with tab_chat:
    st.markdown("## BuildSense AI Chat")
    st.markdown('<div class="label-sm" style="margin-bottom:1rem">Ask questions about your project, cost optimisation, materials, timelines, and more.</div>', unsafe_allow_html=True)

    # Chat history display
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
<div class="bs-card bs-card-accent" style="text-align:center;padding:2rem;margin:1rem 0">
  <div style="font-size:1.5rem;margin-bottom:0.4rem">💬</div>
  <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem">Ask me anything about your construction project</div>
  <div class="label-sm" style="margin-top:0.4rem">
    Try: "How can I reduce cost?" · "What's the risk?" · "Estimate timeline"
  </div>
</div>""", unsafe_allow_html=True)
        else:
            for role, msg in st.session_state.chat_history:
                if role == "You":
                    st.markdown(f'<div style="text-align:right"><div class="chat-user">{msg}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-ai"><span style="font-family:Space Mono,monospace;font-size:0.7rem;color:var(--accent)">BuildSense AI</span><br>{msg}</div>', unsafe_allow_html=True)

    st.markdown("")
    chat_col1, chat_col2 = st.columns([5, 1])
    with chat_col1:
        user_input = st.text_input("Message", placeholder="Ask about materials, cost, timeline, risk…", label_visibility="collapsed", key="chat_input")
    with chat_col2:
        send = st.button("Send →", key="chat_send")

    # Quick prompts
    st.markdown('<div class="label-sm" style="margin:0.5rem 0">Quick prompts:</div>', unsafe_allow_html=True)
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick = None
    with qc1:
        if st.button("Reduce cost?", key="q1"): quick = "How can I reduce project cost?"
    with qc2:
        if st.button("Timeline tips", key="q2"): quick = "How to improve project timeline?"
    with qc3:
        if st.button("Risk factors", key="q3"): quick = "What are the main risk factors?"
    with qc4:
        if st.button("Material advice", key="q4"): quick = "Give me advice on material selection"

    final_input = quick or (user_input if send else None)

    if final_input:
        if not api_ok:
            st.error("API offline.", icon="🔴")
        else:
            with st.spinner("Thinking…"):
                data, err = api_post(API_CHAT, {"message": final_input, "features": base_payload})

            if err:
                reply = f"⚠️ {err}"
            elif data:
                reply = data.get("response", data.get("detail", "No response"))
            else:
                reply = "Could not get response."

            st.session_state.chat_history.append(("You", final_input))
            st.session_state.chat_history.append(("AI", reply))
            st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑 Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

# TAB 5 — COPILOT
with tab_copilot:
    st.markdown("## AI Copilot — Scenario Optimizer")
    st.markdown('<div class="label-sm" style="margin-bottom:1rem">The Copilot ranks all your What-If scenarios against your goal and recommends the best path forward.</div>', unsafe_allow_html=True)

    goal_col, _ = st.columns([2, 4])
    with goal_col:
        goal = st.selectbox("🎯 Optimization Goal", [
            ("balanced",    "⚖️  Balanced (Cost + Time + Quality)"),
            ("min_cost",    "💸  Minimize Cost"),
            ("fastest",     "⚡  Fastest Completion"),
            ("max_quality", "🏅  Maximum Quality (DCS)"),
        ], format_func=lambda x: x[1], key="copilot_goal")
        goal_key = goal[0]

    # Inline scenario builder for copilot
    st.markdown('<div class="section-title">Scenarios to Evaluate</div>', unsafe_allow_html=True)
    cp_num = st.slider("Scenarios", 1, 5, 2, key="cp_num")
    cp_scenarios = []
    for i in range(cp_num):
        with st.expander(f"⚙️  Copilot Scenario {i+1}", expanded=(i == 0)):
            cc1, cc2, cc3 = st.columns(3)
            with cc1:
                cp_name  = st.text_input("Name", f"Option {i+1}", key=f"cp_n_{i}")
                cp_fl    = st.number_input("Floors",   value=floors,       key=f"cp_f_{i}")
            with cc2:
                cp_lb    = st.number_input("Labor Cost", value=labor_cost, key=f"cp_l_{i}")
                cp_wt    = st.slider("Weather", 0.0, 1.0, weather_index, 0.05, key=f"cp_w_{i}")
            with cc3:
                cp_eff   = st.slider("Efficiency", 0.0, 5.0, efficiency, 0.1, key=f"cp_e_{i}")
                cp_mat   = st.selectbox("Material Quality", [1,2,3], index=material_quality-1,
                                         format_func=lambda x:{1:"Economy",2:"Standard",3:"Premium"}[x], key=f"cp_mq_{i}")
            cp_scenarios.append({
                "name": cp_name,
                "changes": {"floors": cp_fl, "labor_cost": cp_lb, "weather_index": cp_wt,
                             "efficiency": cp_eff, "material_quality": cp_mat},
            })

    col_cpbtn, _ = st.columns([1, 3])
    with col_cpbtn:
        run_copilot = st.button("🤖  Run Copilot", key="btn_copilot")

    if run_copilot:
        if not api_ok:
            st.error("API offline.", icon="🔴")
        else:
            with st.spinner("Copilot analysing scenarios…"):
                data, err = api_post(API_COPILOT, {
                    "base": base_payload,
                    "scenarios": cp_scenarios,
                    "goal": goal_key,
                })

            if err:
                st.error(err)
            elif data.get("status") != "success":
                st.error(data.get("message", "Copilot error"))
            else:
                st.session_state.copilot_data = data

    if st.session_state.copilot_data:
        cd = st.session_state.copilot_data
        st.markdown("---")

        # Best scenario
        best_cp = cd.get("best", {})
        if best_cp:
            bres = best_cp.get("result", {})
            bimp = best_cp.get("impact", {})
            c_col = "ok" if bimp.get("cost_change", 0) <= 0 else "warn"
            st.markdown(f"""
<div class="bs-card bs-card-ok" style="display:flex;align-items:center;gap:1.5rem;padding:1.4rem">
  <div style="font-size:2.2rem">🏆</div>
  <div style="flex:1">
    <div class="label-sm">RECOMMENDED SCENARIO</div>
    <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;font-weight:700;color:var(--ok)">{best_cp.get('scenario','—')}</div>
    <div style="display:flex;gap:1rem;margin-top:0.4rem">
      <span class="mono" style="font-size:0.82rem">Cost: {fmt_inr(bres.get('estimated_cost',0))}</span>
      <span class="mono" style="font-size:0.82rem">Time: {bres.get('estimated_time',0):.0f}d</span>
      <span class="mono" style="font-size:0.82rem">DCS: {bres.get('dcs_score',0)}</span>
      <span class="mono" style="font-size:0.82rem">Score: {best_cp.get('score',0):.2f}</span>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        # Ranked list
        ranked = cd.get("ranked", [])
        if ranked:
            st.markdown("")
            st.markdown('<div class="section-title">Full Ranking</div>', unsafe_allow_html=True)
            medal = {0: "gold", 1: "silver", 2: "bronze"}
            for idx, sc in enumerate(ranked):
                if "result" not in sc:
                    continue
                sc_r   = sc["result"]
                sc_imp = sc.get("impact", {})
                dc_rank = dcs_color(sc_r.get("dcs_score", 0))
                mn = medal.get(idx, "")
                st.markdown(f"""
<div class="rank-item">
  <div class="rank-num {mn}">#{idx+1}</div>
  <div style="flex:1">
    <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:600">{sc['scenario']}</div>
    <div style="display:flex;gap:0.8rem;margin-top:2px">
      <span class="label-sm">Score: <b style="color:var(--accent)">{sc.get('score',0):.2f}</b></span>
      <span class="label-sm">Cost: {fmt_inr(sc_r.get('estimated_cost',0))}</span>
      <span class="label-sm">DCS: {sc_r.get('dcs_score',0)}</span>
    </div>
  </div>
  <div>{simple_bar_html(max(0, sc.get('score', 0)), max(1, ranked[0].get('score',1)) if ranked else 1, dc_rank)}</div>
</div>""", unsafe_allow_html=True)

        # Smart suggestions
        suggestions = cd.get("suggestions", [])
        if suggestions:
            st.markdown("")
            st.markdown('<div class="section-title">Smart Suggestions</div>', unsafe_allow_html=True)
            for s in suggestions:
                st.markdown(f'<div class="insight-pill">💡 {s}</div>', unsafe_allow_html=True)

        # LLM explanation
        llm_exp = cd.get("llm_explanation", "")
        if llm_exp:
            st.markdown("")
            st.markdown('<div class="section-title">AI Deep Analysis</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bs-card bs-card-accent" style="font-size:0.87rem;line-height:1.7">{llm_exp}</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("---")
fc1, fc2, fc3 = st.columns(3)
fc1.markdown('<div class="label-sm">⬡ BuildSense AI &nbsp;·&nbsp; v1.0</div>', unsafe_allow_html=True)
fc2.markdown('<div class="label-sm" style="text-align:center">Decision Intelligence Engine</div>', unsafe_allow_html=True)
fc3.markdown('<div class="label-sm" style="text-align:right">FastAPI + Streamlit</div>', unsafe_allow_html=True)
