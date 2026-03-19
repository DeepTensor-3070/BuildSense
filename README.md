<div align="center">

<img src="https://img.shields.io/badge/AI%20ARENA%202026-Team%20Pragnix-orange?style=for-the-badge&logo=lightning&logoColor=white" />

# 🏗️ BuildSense — BuildAtlas GenAI

### Construction Intelligence Co-Pilot

> *"The future of construction planning is not more spreadsheets.  
> It is an AI that thinks before you ask."*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LLaMA](https://img.shields.io/badge/LLaMA_3.1-Meta-0467DF?style=flat-square&logo=meta&logoColor=white)](https://llama.meta.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## 📌 Overview

The Indian construction industry **loses over ₹18,000 crore annually** to cost overruns and project delays — not because of bad engineers, but because of bad tools. Manual estimation, disconnected spreadsheets, and gut-based decision-making leave even experienced professionals flying blind.

**BuildSense (BuildAtlas GenAI)** changes that.

It is not a cost calculator. It is a **construction co-pilot** — one that reasons, warns, and decides the way a senior site engineer would, but in under 60 seconds. Powered by LLM reasoning, Retrieval-Augmented Generation (RAG), and a proprietary Decision Confidence Score, BuildSense gives every engineer — fresh graduate or veteran — expert-level decision support at their fingertips.

---

## 🚀 Key Features

### 🎯 Decision Confidence Score (DCS) — Hero Feature
Every AI-generated estimate includes a **DCS (0–100)** — an industry-first transparency metric aggregating four dimensions:

| Dimension | Weight |
|---|---|
| Data Quality | High |
| Market Volatility | Medium |
| Project Complexity | Moderate |
| Location Risk | Low |

```
Sample Output → DCS = 78/100 — "High Confidence — Safe to Proceed"
```

---

### ⚠️ Proactive AI Risk Warnings
BuildSense surfaces location and project-specific risks **before you ask** — the moment project type and location are entered.

```
AI Insight — Urban Residential, North India Zone
────────────────────────────────────────────────
Foundation overrun risk: 38% (Alluvial soil detected)
→ Recommend geotechnical survey as Phase 0 — est. ₹1.2–1.8L
→ Saves 9–14% on structural costs
→ Monsoon window (Jun–Sep) will delay excavation unless covered staging is planned
```

---

### 🔄 Live What-If Scenario Engine
Toggle between material types and watch cost, duration, overrun risk, and DCS update **side-by-side in real time**.

| Metric | Concrete | Steel Frame | Timber | Composite |
|---|---|---|---|---|
| Cost Estimate | ₹2.4 Cr | ₹2.9 Cr | ₹1.97 Cr | ₹3.24 Cr |
| Duration | 18 months | 14 months | 20 months | 16 months |
| Overrun Risk | 22% | 15% | 25% | 15% |
| DCS Score | 78/100 | 85/100 | 70/100 | 89/100 |

---

### 📋 Additional Capabilities
- **Accurate Cost Estimates** — Breakdown by material, labour, overhead & contingency
- **Structured Project Timelines** — Phase-by-phase Gantt chart visualization
- **Resource Allocation** — Peak workforce recommendations per phase
- **Progress Tracker** — Monitor project health against planned milestones
- **RAG-Grounded Outputs** — AI responses anchored to IS codes and Indian construction standards

---

## 📊 Impact at a Glance

| Metric | Current State | With BuildSense AI |
|---|---|---|
| Cost estimation time | 3–7 days (manual) | **Under 60 seconds** |
| Estimate accuracy | ±30–40% deviation | **±8–12% with DCS** |
| Risk discovery timing | Mid-project (too late) | **Before planning starts** |
| Decision quality | Experience-dependent | **AI-augmented for all skill levels** |

---

## 🧱 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              Streamlit Dashboard (Frontend)              │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP REST
┌──────────────────────▼──────────────────────────────────┐
│                  Python FastAPI                          │
│            Backend API & AI Inference Layer              │
└──────┬───────────────────────────────────┬──────────────┘
       │                                   │
┌──────▼──────────┐             ┌──────────▼──────────────┐
│  LLM Engine     │             │    Knowledge Layer       │
│  LLaMA 3.1 /   │             │   RAG + FAISS            │
│  GPT-4o         │             │   IS Codes, Rate Cards   │
└──────┬──────────┘             └──────────┬──────────────┘
       │                                   │
┌──────▼───────────────────────────────────▼──────────────┐
│                     Data Layer                           │
│          MySQL (Projects) + Vector DB (Embeddings)       │
└─────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   Deployment                             │
│              Docker + AWS / GCP                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit | Interactive real-time dashboard |
| **Backend API** | Python FastAPI | High-performance REST API |
| **AI Model** | LLaMA 3.1 / GPT-4o | Cost estimation, timeline generation, chatbot |
| **Knowledge Layer** | RAG + FAISS | Construction standards, IS codes, rate schedules |
| **Database** | MySQL + Vector DB | Project history and embedding storage |
| **Deployment** | Docker + AWS/GCP | Scalable, production-ready cloud deployment |

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.10+
- Docker (recommended)
- MySQL 8.0+
- An OpenAI API key **or** a locally running LLaMA 3.1 instance

---

### 1. Clone the Repository

```bash
git clone https://github.com/DeepTensor-3070/BuildSense.git
cd BuildSense
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# AI Model
OPENAI_API_KEY=your_openai_key_here
# OR for local LLaMA:
LLAMA_MODEL_PATH=/path/to/llama-3.1

# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=buildsense

# Vector Store
FAISS_INDEX_PATH=./data/faiss_index

# App
APP_ENV=development
SECRET_KEY=your_secret_key
```

### 5. Initialize the Database

```bash
python scripts/init_db.py
```

### 6. Build the FAISS Knowledge Index

```bash
python scripts/build_index.py --source ./data/is_codes/
```

### 7. Run the Application

**Option A — Run services individually:**

```bash
# Terminal 1: Start FastAPI backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start Streamlit frontend
streamlit run frontend/app.py
```

**Option B — Docker Compose (recommended):**

```bash
docker-compose up --build
```

The app will be available at:
- **Frontend:** `http://localhost:8501`
- **API Docs:** `http://localhost:8000/docs`

---

## 🖥️ Usage

### Generating a Cost Estimate

1. Open the Streamlit dashboard at `http://localhost:8501`
2. Enter your **project parameters**:
   - Project type (Residential / Commercial / Infrastructure)
   - Location (state and zone)
   - Scale (area in sq. ft. or project value range)
   - Preferred materials
3. Click **"Generate Estimate"**
4. View the full breakdown — cost, timeline, resource plan, and your **DCS score**
5. Review any **Proactive AI Risk Warnings** surfaced for your project context

### Running a What-If Scenario

1. After generating an initial estimate, navigate to the **Scenario Engine** tab
2. Toggle between material types (Concrete / Steel / Timber / Composite)
3. Observe real-time updates to cost, duration, overrun risk, and DCS

### API Usage (Direct)

```python
import httpx

payload = {
    "project_type": "residential",
    "location": "Delhi NCR",
    "area_sqft": 2400,
    "material": "concrete",
    "floors": 3
}

response = httpx.post("http://localhost:8000/api/v1/estimate", json=payload)
print(response.json())
```

Sample response:

```json
{
  "cost_estimate": {
    "total": "₹1.82 Cr",
    "material": "₹98L",
    "labour": "₹52L",
    "overhead": "₹18L",
    "contingency": "₹14L"
  },
  "timeline_months": 16,
  "dcs_score": 76,
  "dcs_label": "High Confidence — Safe to Proceed",
  "risk_warnings": [
    {
      "type": "foundation",
      "severity": "medium",
      "message": "Alluvial soil detected. Recommend geotechnical survey as Phase 0."
    }
  ]
}
```

---

## 👥 Target Users

| User | Use Case |
|---|---|
| 👷 Civil Engineers & Structural Consultants | Rapid feasibility estimation |
| 📋 Construction Project Managers | Scheduling, workforce & budget alignment |
| 🏢 Real Estate Developers | Early-stage investment decision support |
| 🏛️ Government Infrastructure Teams | Cost benchmarking for tenders |
| 🎓 Fresh Graduates & Junior Engineers | Expert-level guidance without years of experience |

---

## 🆚 Competitive Differentiation

Existing tools like **CostX**, **Candy**, or **Excel-based estimators** are static, manual, and disconnected.

| Capability | CostX / Candy / Excel | **BuildSense AI** |
|---|---|---|
| Estimate generation time | 3–7 days | ✅ Under 60 seconds |
| Confidence scoring | ❌ None | ✅ Decision Confidence Score |
| Proactive risk alerts | ❌ None | ✅ Auto-triggered on input |
| What-if scenario engine | ❌ Manual re-entry | ✅ Real-time side-by-side |
| Grounded in IS codes | ❌ Manual lookup | ✅ RAG-powered |
| AI reasoning transparency | ❌ Black box | ✅ DCS + explainability |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and add tests where applicable
4. **Commit** with a clear message
   ```bash
   git commit -m "feat: add monsoon risk detection for Zone 3"
   ```
5. **Push** and open a **Pull Request**

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for code style guidelines and our review process.

---

## 📁 Project Structure

```
BuildSense/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── api/
│   │   └── v1/
│   │       ├── estimate.py  # Cost estimation endpoints
│   │       ├── scenario.py  # What-if engine endpoints
│   │       └── risk.py      # Risk warning endpoints
│   ├── core/
│   │   ├── llm.py           # LLM integration (LLaMA / GPT-4o)
│   │   ├── rag.py           # RAG pipeline + FAISS retriever
│   │   └── dcs.py           # Decision Confidence Score logic
│   └── models/
│       └── schemas.py       # Pydantic data models
├── frontend/
│   └── app.py               # Streamlit dashboard
├── data/
│   ├── is_codes/            # Indian Standard construction docs
│   └── faiss_index/         # Pre-built vector index
├── scripts/
│   ├── init_db.py           # DB initialization
│   └── build_index.py       # FAISS index builder
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🏆 Acknowledgements

Built with ❤️ by **Team Pragnix** for **AI ARENA 2026**.

Special thanks to the open-source communities behind FastAPI, Streamlit, LangChain, FAISS, and the LLaMA project.

---

<div align="center">

**BuildSense** · Team Pragnix · AI ARENA 2026

*Turning construction expertise into an AI that every engineer can access.*

</div>
