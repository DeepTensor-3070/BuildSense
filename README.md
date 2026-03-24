<div align="center">

<br />

```
██████╗ ██╗   ██╗██╗██╗     ██████╗ ███████╗███████╗███╗   ██╗███████╗███████╗
██╔══██╗██║   ██║██║██║     ██╔══██╗██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝
██████╔╝██║   ██║██║██║     ██║  ██║███████╗█████╗  ██╔██╗ ██║███████╗█████╗  
██╔══██╗██║   ██║██║██║     ██║  ██║╚════██║██╔══╝  ██║╚██╗██║╚════██║██╔══╝  
██████╔╝╚██████╔╝██║███████╗██████╔╝███████║███████╗██║ ╚████║███████║███████╗
╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝
```

**AI-powered code analysis and build intelligence — understand your codebase before it breaks.**

<br />

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)]()


</div>

---

## What is BuildSense?

BuildSense is an AI-powered code analysis and build intelligence platform that gives developers deep, actionable insight into their codebase. It statically and dynamically analyses your project, detects structural weaknesses, dependency risks, and build failures — then explains them in plain language using a fine-tuned ML pipeline.

Whether you're onboarding to a legacy codebase, debugging a flaky CI pipeline, or hardening your architecture before a major release, BuildSense turns opaque build noise into clear, prioritised guidance.

> **Think of it as a senior engineer watching your build — one who never sleeps, never guesses, and always explains their reasoning.**

---

## ✨ Features

### 🧠 AI-Driven Code Analysis
BuildSense uses a machine learning model trained on thousands of real-world codebases to detect anti-patterns, complexity hotspots, and latent bugs — not just style violations.

### 🔍 Build Failure Diagnosis
Feed BuildSense your CI/CD logs and it will pinpoint the root cause, trace it back to the relevant code change, and suggest a fix — in seconds.

### 📊 Dependency Risk Scoring
Every dependency in your project is scored for security vulnerability exposure, staleness, and license compatibility. Know your risk surface at a glance.

### 🗺️ Architecture Visualisation
BuildSense generates interactive call graphs, module dependency maps, and coupling heatmaps rendered in the React frontend — making your system architecture tangible.

### ⚡ Incremental Analysis
Only changed files are re-analysed on each run. BuildSense caches intermediate results intelligently so large monorepos stay fast.

### 🔔 Smart Alerting
Set thresholds for complexity scores, test coverage delta, or dependency age — and get notified the moment a PR crosses the line, before it merges.

### 🖥️ React Dashboard
A clean, interactive frontend lets you drill into file-level reports, compare snapshots across commits, and export findings as JSON, HTML, or PDF.

---

## 🎬 Demo

> Screenshots and a live demo link will be added here. In the meantime, clone the repo and run `make demo` to spin up a local demo with a sample project.

```
make demo
# → Launches the React dashboard at http://localhost:3000
# → Runs BuildSense against the bundled sample project
# → Results stream in live as analysis completes
```

---

## 📦 Installation

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10 or higher |
| Node.js | 18 or higher |
| pip | latest |
| npm / yarn | latest |

### 1. Clone the repository

```bash
git clone https://github.com/DeepTensor-3070/BuildSense.git
cd BuildSense
```

### 2. Set up the Python backend

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set up the React frontend

```bash
cd frontend
npm install
cd ..
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in the required values:

```env
# Core
BUILDSENSE_SECRET_KEY=your-secret-key

# Model settings
MODEL_PATH=./models/buildsense_v1.pkl
ANALYSIS_WORKERS=4

# Frontend API base URL
VITE_API_BASE_URL=http://localhost:8000
```

### 5. Run database migrations (if applicable)

```bash
python manage.py migrate
```

---

## 🚀 Usage

### Starting the application

**Backend (API server):**

```bash
# From the project root, with the virtual environment active
python -m buildsense.server --port 8000
```

**Frontend (React dashboard):**

```bash
cd frontend
npm run dev
# → http://localhost:3000
```

Or start everything together:

```bash
make start
```

---

### Analysing a project

**Via CLI:**

```bash
# Analyse the current directory
buildsense analyse .

# Analyse a specific path
buildsense analyse /path/to/your/project

# Analyse and output JSON
buildsense analyse . --format json --output report.json

# Analyse and set a minimum quality score threshold (exits non-zero if below)
buildsense analyse . --min-score 75
```

**Via the dashboard:**

1. Open `http://localhost:3000`
2. Click **New Analysis** and provide a path or upload a zip archive
3. Watch results populate in real time
4. Drill into any file or module for detailed findings

**Diagnosing a build log:**

```bash
# Pipe a CI log directly into BuildSense
cat build.log | buildsense diagnose

# Or point at a log file
buildsense diagnose --log build.log --verbose
```

**Example output:**

```
BuildSense v1.0.0  ·  Analysing: my-project/

  ✔  Parsed 142 files (2.3s)
  ✔  Dependency graph constructed
  ✔  ML model inference complete

  ┌─ Summary ──────────────────────────────────────────────────┐
  │  Quality Score    74 / 100    ↓ 3 from last snapshot       │
  │  Critical Issues  2                                         │
  │  Warnings         11                                        │
  │  Dependency Risks 4  (1 high, 3 medium)                    │
  └────────────────────────────────────────────────────────────┘

  CRITICAL  src/core/pipeline.py:204
            Cyclomatic complexity 38 — refactor recommended

  CRITICAL  package.json
            lodash@4.17.20 has known CVE-2021-23337 (high severity)

  Run `buildsense report` to open the full HTML report.
```

---

## 📡 API Reference

The BuildSense backend exposes a REST API. All endpoints return JSON.

### `POST /api/analyse`

Start a new analysis job.

**Request body:**

```json
{
  "path": "/absolute/path/to/project",
  "options": {
    "include_deps": true,
    "min_complexity_threshold": 10,
    "ignore_patterns": ["**/node_modules/**", "**/__pycache__/**"]
  }
}
```

**Response:**

```json
{
  "job_id": "a3f9c821-...",
  "status": "queued",
  "created_at": "2026-03-24T10:00:00Z"
}
```

---

### `GET /api/analyse/{job_id}`

Poll the status of an analysis job.

**Response:**

```json
{
  "job_id": "a3f9c821-...",
  "status": "complete",
  "score": 74,
  "issues": [...],
  "dependency_risks": [...],
  "completed_at": "2026-03-24T10:00:18Z"
}
```

---

### `POST /api/diagnose`

Diagnose a build log.

**Request body:**

```json
{
  "log": "<raw build log text>",
  "context": {
    "language": "python",
    "build_tool": "pytest"
  }
}
```

**Response:**

```json
{
  "root_cause": "ImportError in src/utils/loader.py — circular import with src/core/pipeline.py",
  "likely_commit": "abc1234",
  "suggested_fix": "Move shared types to a separate src/types.py module to break the cycle.",
  "confidence": 0.91
}
```

---

### `GET /api/snapshots`

List all stored analysis snapshots for comparison.

---

### `GET /api/snapshots/{snapshot_id}/diff`

Return a structured diff between two snapshots.

**Query params:** `compare_to=<snapshot_id>`

---

## 🤝 Contributing

Contributions are very welcome! Here's how to get started.

### Development setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/BuildSense.git
cd BuildSense

# Install dev dependencies
pip install -r requirements-dev.txt

cd frontend && npm install && cd ..
```

### Running tests

```bash
# Python tests
pytest tests/ -v

# Frontend tests
cd frontend && npm test
```

### Submitting a PR

1. **Create a branch** from `main` — use a descriptive name like `feat/add-go-support` or `fix/dependency-scorer-edge-case`
2. **Make your changes** — keep commits focused and atomic
3. **Add or update tests** — PRs that reduce test coverage will not be merged
4. **Run the full test suite** and make sure everything passes
5. **Open a Pull Request** — describe what you changed and why

### Reporting issues

Please use [GitHub Issues](https://github.com/DeepTensor-3070/BuildSense/issues) and include:
- BuildSense version (`buildsense --version`)
- Python and Node versions
- Steps to reproduce
- Expected vs actual behaviour
- Relevant logs or error output

---

## 📁 Project Structure

```
BuildSense/
├── buildsense/           # Core Python package
│   ├── analyser/         # Static & ML-based code analysis
│   ├── diagnostics/      # Build log diagnosis engine
│   ├── dependencies/     # Dependency risk scoring
│   ├── server/           # FastAPI/Flask REST API
│   └── models/           # Trained ML model files
├── frontend/             # React dashboard
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Route-level pages
│   │   └── api/          # API client hooks
│   └── public/
├── tests/                # Python test suite
├── requirements.txt
├── requirements-dev.txt
├── Makefile
└── .env.example
```

---

## 📄 License

BuildSense is released under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ by [DeepTensor-3070](https://github.com/DeepTensor-3070) and contributors.

<br />

⭐ **If BuildSense helps you, give the repo a star — it means a lot.**

</div>