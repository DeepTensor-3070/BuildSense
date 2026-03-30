<div align="center">

<img src="https://img.shields.io/badge/BuildSense-AI-00d4ff?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzAwZDRmZiIgZD0iTTEyIDJMMyA3djEwbDkgNSA5LTV2LTEwTDEyIDJ6Ii8+PC9zdmc+" />

# ⬡ BuildSense AI

### *Construction Decision Intelligence Engine*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![HuggingFace](https://img.shields.io/badge/🤗_Transformers-4.40+-FFD21E?style=flat-square)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-00e576?style=flat-square)]()

<br/>

> **BuildSense AI** is an end-to-end AI-powered construction intelligence platform built for the Indian market.  
> It predicts project cost, timeline, and decision confidence — then recommends the optimal path forward  
> using multi-scenario what-if analysis, an LLM-powered chatbot, and an autonomous Copilot optimizer.

<br/>

![BuildSense AI Dashboard](https://via.placeholder.com/900x420/0a0c10/00d4ff?text=BuildSense+AI+%E2%80%94+Dashboard+Preview)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Folder Structure](#-folder-structure)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Running the App](#-running-the-app)
- [API Reference](#-api-reference)
- [Module Breakdown](#-module-breakdown)
- [ML Models](#-ml-models)
- [UI Pages](#-ui-pages)
- [Indian Market Context](#-indian-market-context)
- [Configuration](#-configuration)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧠 Overview

BuildSense AI bridges the gap between raw construction data and intelligent decision-making. It is designed for **project managers, civil engineers, contractors, and developers** operating in the Indian construction market.

The platform takes 18 project parameters as input — area, material quality, location, soil type, labor cost, weather exposure, and more — and produces:

- **Estimated project cost** in ₹ (Indian Rupees), calibrated to regional conditions
- **Project timeline** in days
- **Decision Confidence Score (DCS)** — a composite metric reflecting how reliable the prediction is
- **Risk label and confidence** — Low / Medium / High with probability score
- **Smart insights** — rule-based flags for weather risk, soil issues, inflation, low efficiency
- **Live material price index** — simulated real-time cement, steel, sand, aggregate prices
- **What-If scenario comparison** — run up to 5 modified scenarios side-by-side against the base case
- **AI Copilot** — ranks all scenarios against a user-defined optimization goal
- **LLM-powered Chat** — ask questions in plain language about the project

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔮 **Prediction Engine** | ML models (cost, time, risk, DCS) trained on synthetic Indian construction data |
| 🧪 **Multi What-If Engine** | Compare up to 5 scenario mutations vs. the base project in parallel |
| 🤖 **AI Copilot** | Goal-based optimizer — balanced / min cost / fastest / max quality |
| 💬 **NLP Chatbot** | Intent-aware chatbot backed by GPT-2 + rule engine |
| 🧠 **GenAI Insights** | Flan-T5 powered narrative explanations for scenario changes |
| 📊 **Analytics Dashboard** | Risk gauge, DCS bar, material price trends, project fingerprint |
| 🏗️ **Indian Market Data** | DSR 2023-24 inspired rates, North India regional factors, IS code references |
| ⚡ **FastAPI Backend** | Fully async REST API with CORS support, Pydantic validation |
| 🎨 **Dark UI** | Cyberpunk industrial Streamlit frontend — Rajdhani + Space Mono typography |

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT FRONTEND                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │Dashboard │ │ Predict  │ │ What-If  │ │ Chat │ Copilot│  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └───────┬───────┘  │
└───────┼─────────────┼────────────┼───────────────┼──────────┘
        │             │  HTTP/REST  │               │
        ▼             ▼             ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                          │
│  GET /health   POST /predict   POST /multi-what-if           │
│  POST /chat    POST /copilot                                 │
└──────┬──────────────┬────────────────────────────┬──────────┘
       │              │                            │
       ▼              ▼                            ▼
┌─────────────┐ ┌──────────────────────┐ ┌────────────────────┐
│  ML MODELS  │ │    AI / LLM LAYER    │ │  BUSINESS LOGIC    │
│  predict.py │ │  genai.py (Flan-T5)  │ │  insights.py       │
│  - cost     │ │  chatbot.py (GPT-2)  │ │  material.py       │
│  - time     │ │  copilot.py          │ │  copilot.py        │
│  - risk     │ └──────────────────────┘ └────────────────────┘
│  - dcs      │
└─────────────┘
```

---

## 📁 Folder Structure

```
BuildSense/
│
├── 📄 README.md                    # This file
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore
├── 📄 .env.example                 # Environment variable template
│
├── 🚀 backend/                         # FastAPI Backend
│   ├── main.py                     # App entry point, all routes
│   ├── chatbot.py                  # Intent detection + GPT-2 chat handler
│   ├── copilot.py                  # Scenario ranking + Copilot engine
│   ├── genai.py                    # Flan-T5 what-if narrative generator
│   ├── insights.py                 # Rule-based smart insight generator
│   └── material.py                 # Live material price simulation + index
│
├── 🤖 models/                      # ML Model layer
│   ├── predict.py                  # Unified prediction interface (predict_all)
│   ├── cost.ipynb               # Cost estimation model training script
│   ├── time.ipynb               # Timeline model training script
│   ├── risk.ipynb               # Risk classification model training script
│   ├── dcs.ipynb                # DCS score model training script
│   |
│   └── saved/                      # Serialised model artefacts
│       ├── cost_model.pkl
│       ├── time_model.pkl
│       ├── risk_model.pkl
│       ├── dcs_model.pkl
│       └── scaler.pkl
│
├── 🎨 frontend/                    # Streamlit Frontend
│   └── app.py                      # Full multi-tab Streamlit UI
│
├── 📊 data/                        # Data assets
│   ├── processed     
│   ├── raw
│   └── material_baseline.json      

```

---

## 🛠️ Tech Stack

### Backend
| Layer | Technology | Purpose |
|---|---|---|
| API Framework | FastAPI 0.110+ | REST API, Pydantic validation, async routing |
| ML Runtime | scikit-learn 1.4+ | Gradient Boosting, Random Forest models |
| LLM (GenAI) | `google/flan-t5-small` via HuggingFace | What-if narrative explanations |
| Chatbot | `gpt2` via HuggingFace Transformers | Natural language construction Q&A |
| Data | NumPy, Pandas | Feature engineering and processing |
| Server | Uvicorn | ASGI server |

### Frontend
| Layer | Technology | Purpose |
|---|---|---|
| UI Framework | Streamlit 1.32+ | Multi-tab dashboard and forms |
| HTTP Client | Requests | API communication |
| Data Display | Pandas DataFrames | Tabular results and comparisons |
| Charts | Streamlit native `st.bar_chart` | Scenario comparison visualization |
| Typography | Rajdhani, Space Mono, DM Sans | Dark industrial design language |

---

## ⚙️ Installation

### Prerequisites

- Python **3.10+**
- pip or conda
- Git
- 2 GB+ RAM (for HuggingFace model loading)

### 1 — Clone the Repository

```bash
git clone https://github.com/DeepTensor-3070/BuildSense.git
cd BuildSense
```

### 2 — Create a Virtual Environment

```bash
# Using venv
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
.venv\Scripts\activate             # Windows

# OR using conda
conda create -n buildsense python=3.10
conda activate buildsense
```

### 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`** contents:

```txt
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic>=2.6.0
streamlit>=1.32.0
requests>=2.31.0
pandas>=2.1.0
numpy>=1.26.0
scikit-learn>=1.4.0
transformers>=4.40.0
torch>=2.2.0
joblib>=1.3.0
python-dotenv>=1.0.0
```

> **Note on torch:** For CPU-only environments use `pip install torch --index-url https://download.pytorch.org/whl/cpu` to get a smaller install.

### 4 — Train the ML Models

If you do not have pre-trained `.pkl` files in `models/saved/`, generate data and train:

```bash
cd models
python generate_data.py          # Creates data/synthetic_dataset.csv
python train_cost.py             # Saves models/saved/cost_model.pkl
python train_time.py             # Saves models/saved/time_model.pkl
python train_risk.py             # Saves models/saved/risk_model.pkl
python train_dcs.py              # Saves models/saved/dcs_model.pkl
```

---

## 🚀 Running the App

Open **two terminals** from the project root.

### Terminal 1 — Start the FastAPI Backend

```bash
cd api
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Verify it's running:
```
http://127.0.0.1:8000/          → {"message": "🚀 BuildSense AI API is running"}
http://127.0.0.1:8000/health    → {"status": "ok"}
http://127.0.0.1:8000/docs      → Interactive Swagger UI
```

### Terminal 2 — Start the Streamlit Frontend

```bash
cd frontend
streamlit run app.py
```

The app opens automatically at:
```
http://localhost:8501
```

---

## 📡 API Reference

### `GET /`
Health ping.

**Response:**
```json
{ "message": "🚀 BuildSense AI API is running" }
```

---

### `GET /health`
Lightweight health check polled by the frontend status indicator.

**Response:**
```json
{ "status": "ok", "message": "BuildSense AI API is healthy" }
```

---

### `POST /predict`
Run a full prediction for a single project configuration.

**Request Body:**
```json
{
  "area": 1500,
  "material_quality": 2,
  "location_factor": 1.3,
  "labor_cost": 60000,
  "project_type": 1,
  "floors": 2,
  "soil_type": 1,
  "weather_index": 0.4,
  "material_price_index": 1.2,
  "contractor_experience": 5,
  "equipment_availability": 0.8,
  "project_complexity": 2,
  "permits_delay": 5,
  "transport_cost": 20000,
  "inflation_factor": 1.1,
  "cost_per_sqft_est": 2.4,
  "labor_intensity": 40,
  "efficiency": 4.0
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "estimated_cost": 1842500.0,
    "estimated_time": 95,
    "dcs_score": 74,
    "risk": {
      "label": "Medium",
      "confidence": 0.68
    }
  },
  "insights": [
    "⚠️ Rising inflation may increase material costs"
  ],
  "explanation": "The modifications suggest a moderate cost increase driven by...",
  "materials": {
    "cement": 345.20,
    "steel": 62.80,
    "sand": 48.50,
    "aggregate": 38.90
  },
  "material_index": 1.024,
  "message": ""
}
```

---

### `POST /multi-what-if`
Run multiple modified scenario predictions against a base project.

**Request Body:**
```json
{
  "base": { ...ProjectInput... },
  "scenarios": [
    {
      "name": "Reduced Labor",
      "changes": { "labor_cost": 45000, "floors": 2 }
    },
    {
      "name": "Premium Materials",
      "changes": { "material_quality": 3, "inflation_factor": 1.3 }
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "base": { ...base result... },
    "scenarios": [
      {
        "scenario": "Reduced Labor",
        "changes": { "labor_cost": 45000 },
        "result": { ...modified result... },
        "impact": {
          "cost_change": -85000.0,
          "time_change": 3.0,
          "dcs_change": -2.0
        },
        "insight": "Reducing labor cost saves ₹85,000 but slightly..."
      }
    ]
  }
}
```

---

### `POST /chat`
Send a natural language message to the BuildSense chatbot.

**Request Body:**
```json
{
  "message": "How can I reduce the project cost?",
  "features": { ...ProjectInput... }
}
```

**Response:**
```json
{
  "status": "success",
  "response": "To reduce cost, you can use medium-quality materials, optimize labor usage..."
}
```

---

### `POST /copilot`
Run the AI Copilot — ranks scenarios by a target optimization goal.

**Request Body:**
```json
{
  "base": { ...ProjectInput... },
  "scenarios": [ ...list of scenario objects... ],
  "goal": "balanced"
}
```

**Goal options:** `balanced` · `min_cost` · `fastest` · `max_quality`

**Response:**
```json
{
  "status": "success",
  "best": {
    "scenario": "Reduced Labor",
    "score": 4821.5,
    "result": { ... },
    "impact": { ... }
  },
  "ranked": [ ... ],
  "suggestions": [
    "Improve labor efficiency to reduce time"
  ],
  "llm_explanation": "The Reduced Labor scenario achieves the best balance..."
}
```

---

## 🧩 Module Breakdown

### `api/main.py`
Entry point for the FastAPI application. Defines all routes, applies CORS middleware, validates Pydantic input schemas, and orchestrates calls to all sub-modules. Handles graceful error responses so the frontend never receives unhandled 500s.

### `api/insights.py`
Pure rule-based engine that inspects input features and prediction results, emitting human-readable warning strings. Rules cover weather risk, soil quality, project complexity, contractor efficiency, inflation, high cost, extended timeline, and positive DCS confirmation.

### `api/material.py`
Simulates a live material price feed (to be replaced with a real API). Returns randomised prices within realistic Indian market bands for cement, steel, sand, and aggregate, and computes a weighted material price index relative to DSR baseline prices.

### `api/genai.py`
Loads `google/flan-t5-small` via HuggingFace Transformers and generates brief narrative explanations of what-if scenario changes. Accepts base result, modified result, and computed impact dict, and returns a concise plain-English explanation of why costs or timelines shifted.

### `api/chatbot.py`
Two-layer chatbot: a keyword-based intent classifier (`predict` / `advice` / `what_if` / `general`) and a GPT-2 text generation fallback for general queries. For `predict` intent, it calls the ML model directly and returns formatted output.

### `api/copilot.py`
Scenario evaluation and ranking engine. The `evaluate_scenario()` function computes a scalar score per scenario based on the chosen goal. `copilot_engine()` ranks all scenarios, identifies the best, generates smart suggestions, and calls GenAI for an LLM-level explanation.

### `models/predict.py`
Unified prediction interface. `predict_all(features)` loads saved model artefacts, runs cost/time/risk/DCS inference in one call, and returns a clean result dict. `predict_with_dcs(features)` is the chatbot-facing variant.

---

## 🤖 ML Models

BuildSense uses four independent scikit-learn models trained on synthetic data calibrated to Indian construction norms:

| Model | Type | Target | Metric |
|---|---|---|---|
| **Cost Estimator** | Gradient Boosting Regressor | `estimated_cost` (₹) | MAE, R² |
| **Timeline Estimator** | Random Forest Regressor | `estimated_time` (days) | MAE, RMSE |
| **Risk Classifier** | Random Forest Classifier | `risk_label` (Low/Med/High) | F1, Accuracy |
| **DCS Scorer** | Gradient Boosting Regressor | `dcs_score` (0–100) | MAE |

### Input Features (18)

| Feature | Type | Description |
|---|---|---|
| `area` | float | Total built-up area in sq ft |
| `material_quality` | int (1–3) | Economy / Standard / Premium |
| `location_factor` | float (0.5–2.0) | Regional cost multiplier |
| `labor_cost` | float | Total labour cost in ₹ |
| `project_type` | int (1–3) | Residential / Commercial / Industrial |
| `floors` | int | Number of floors |
| `soil_type` | int (1–3) | Good / Average / Poor |
| `weather_index` | float (0–1) | Weather disruption risk |
| `material_price_index` | float | Live material cost index |
| `contractor_experience` | int | Years of experience |
| `equipment_availability` | float (0–1) | Equipment readiness ratio |
| `project_complexity` | int (1–3) | Simple / Moderate / Complex |
| `permits_delay` | int | Expected permit delay in days |
| `transport_cost` | float | Logistics/transport cost in ₹ |
| `inflation_factor` | float | Inflation multiplier |
| `cost_per_sqft_est` | float | User's estimated cost per sq ft |
| `labor_intensity` | float | Labour hours intensity score |
| `efficiency` | float (0–5) | Contractor efficiency rating |

---

## 🖥️ UI Pages

### 📊 Dashboard
The central analytics board. Automatically populates after the first prediction. Shows:
- **KPI Row** — Cost, Timeline, DCS Score, Risk Level, Area
- **Risk Gauge** — progress bar with confidence percentage
- **DCS Score Meter** — colour-coded bar (green / amber / red)
- **Smart Insights** — collated warning pills from the rule engine
- **Live Material Prices** — price bars with % delta vs baseline for cement, steel, sand, aggregate
- **Material Price Index** — composite trend indicator
- **Project Fingerprint** — normalised bars for 5 key input factors
- **Scenario History Table** — comparison DataFrame + bar chart for all What-If runs

### 🔮 Predict
Single-project prediction form. Reads all 18 inputs from the sidebar. On submit, calls `POST /predict` and displays cost/time/DCS/risk cards, insights, AI explanation, and an input summary table.

### 🧪 What-If
Multi-scenario engine. Build 1–5 scenarios by modifying floors, labor cost, weather, material quality, inflation, and efficiency. Results appear as a side-by-side card grid with change badges and a comparative bar chart.

### 💬 Chat
Intent-aware chatbot interface. Styled message bubbles (user right, AI left). Quick-prompt buttons: "Reduce cost?", "Timeline tips", "Risk factors", "Material advice". Full chat history with clear button.

### 🤖 Copilot
Autonomous optimizer. Choose a goal, define scenarios, and the Copilot ranks them with gold/silver/bronze medals, provides smart suggestions, and generates an LLM narrative explanation.

---

## 🇮🇳 Indian Market Context

BuildSense is intentionally calibrated for the **Indian construction market**:

- **DSR 2023-24** — Delhi Schedule of Rates 2023-24 used as cost baseline
- **North India regional factors** — location multipliers reflect Delhi NCR, UP, Haryana conditions
- **IS Code references** — soil classification follows IS 1498, project categories align with Indian construction norms
- **₹ denomination** — all cost outputs in Indian Rupees with lakh/crore formatting
- **Material benchmarks** — cement (~₹350/bag), steel (~₹60/kg), sand (~₹50/cu.ft) match current North India market rates
- **Weather index** — calibrated to monsoon disruption patterns (June–September high-risk window)

---

## ⚙️ Configuration

Create a `.env` file in the project root (copy from `.env.example`):

```env
# API Configuration
API_HOST=127.0.0.1
API_PORT=8000

# Frontend Configuration
STREAMLIT_PORT=8501
API_BASE_URL=http://127.0.0.1:8000

# Model paths
MODEL_DIR=./models/saved

# LLM settings (optional — reduces inference time)
GENAI_MAX_TOKENS=150
CHATBOT_MAX_TOKENS=150
GENAI_TEMPERATURE=0.7

# Material API (future)
# MATERIAL_API_KEY=your_key_here
# MATERIAL_API_URL=https://api.example.com/prices
```

---

## 🗺️ Roadmap

- [x] Base prediction engine (cost, time, risk, DCS)
- [x] Multi-scenario what-if engine
- [x] Rule-based smart insights
- [x] GPT-2 chatbot with intent detection
- [x] Flan-T5 GenAI explanations
- [x] Copilot ranking engine
- [x] Dark industrial Streamlit UI with analytics dashboard
- [x] FastAPI backend with CORS and health check
- [ ] Replace simulated material prices with real Indian commodities API
- [ ] OpenAI GPT-4o / Claude integration for higher-quality explanations
- [ ] RAG chatbot over IS code / DSR document knowledge base
- [ ] User authentication and project save/load
- [ ] PDF report generation for project proposals
- [ ] Historical project database with trend analytics
- [ ] Mobile-responsive Progressive Web App
- [ ] Docker Compose deployment
- [ ] CI/CD pipeline with GitHub Actions

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/DeepTensor-3070/BuildSense.git
cd BuildSense

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes and commit
git add .
git commit -m "feat: add your feature description"

# 5. Push and open a Pull Request
git push origin feature/your-feature-name
```

### Commit Message Convention
```
feat:     New feature
fix:      Bug fix
docs:     Documentation changes
style:    Formatting, no logic change
refactor: Code restructure
test:     Adding tests
chore:    Build process or tooling
```

---

## 👤 Author

<table>
<tr>
<td align="center">
<b>Subhanshu Verma</b><br/>
<i>AI / Deep Learning · Computer Vision</i><br/>
B.Tech · India<br/>
<br/>
<a href="https://github.com/DeepTensor-3070">
  <img src="https://img.shields.io/badge/GitHub-DeepTensor--3070-181717?style=flat-square&logo=github" />
</a>
</td>
</tr>
</table>

> 🏆 2nd Place in Track — AI ARENA 2026, Gen AI Track · KIET Group of Institutions  
> Team Pragnix · Project: BuiltSense AI

---

## 📄 License

```
MIT License — Copyright (c) 2026 Subhanshu Verma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
```

---

<div align="center">

**⬡ BuildSense AI** — *Built for India's Construction Future*

[![Stars](https://img.shields.io/github/stars/DeepTensor-3070/BuildSense?style=social)](https://github.com/DeepTensor-3070/BuildSense)
[![Forks](https://img.shields.io/github/forks/DeepTensor-3070/BuildSense?style=social)](https://github.com/DeepTensor-3070/BuildSense)

</div>
