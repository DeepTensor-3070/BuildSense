#!/bin/bash
# ============================================================
# BuildSense AI — Project Scaffold Script
# Run this from the repo root after cloning:
#   chmod +x scaffold.sh && ./scaffold.sh
# ============================================================

echo "⬡ Scaffolding BuildSense AI project structure..."

# ── Root files ───────────────────────────────────────────────
touch .gitignore
touch requirements.txt

cat > .env.example << 'EOF'
# API Configuration
API_HOST=127.0.0.1
API_PORT=8000

# Frontend Configuration
STREAMLIT_PORT=8501
API_BASE_URL=http://127.0.0.1:8000

# Model paths
MODEL_DIR=./models/saved

# LLM settings
GENAI_MAX_TOKENS=150
CHATBOT_MAX_TOKENS=150
GENAI_TEMPERATURE=0.7

# Material API (future)
# MATERIAL_API_KEY=your_key_here
# MATERIAL_API_URL=https://api.example.com/prices
EOF

cat > requirements.txt << 'EOF'
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
EOF

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.eggs/

# Virtual environments
.venv/
env/
venv/
ENV/

# Streamlit
.streamlit/secrets.toml

# Environment
.env

# Jupyter
.ipynb_checkpoints/
*.ipynb~

# Model artefacts (large files — use Git LFS if needed)
models/saved/*.pkl

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
EOF

# ── api/ ─────────────────────────────────────────────────────
mkdir -p api
touch api/__init__.py

# Move/create core API files (copy from root if they exist)
for f in main.py chatbot.py copilot.py genai.py insights.py material.py; do
    [ -f "$f" ] && mv "$f" api/ && echo "  ✔ Moved $f → api/$f" || touch api/$f
done

# ── models/ ──────────────────────────────────────────────────
mkdir -p models/saved
touch models/__init__.py
touch models/predict.py
touch models/train_cost.py
touch models/train_time.py
touch models/train_risk.py
touch models/train_dcs.py
touch models/generate_data.py
touch models/saved/.gitkeep          # keep folder in git

# ── frontend/ ────────────────────────────────────────────────
mkdir -p frontend
[ -f "app.py" ] && mv app.py frontend/ && echo "  ✔ Moved app.py → frontend/app.py" || touch frontend/app.py

# ── data/ ────────────────────────────────────────────────────
mkdir -p data
touch data/.gitkeep

cat > data/material_baseline.json << 'EOF'
{
  "cement":    350,
  "steel":      60,
  "sand":       50,
  "aggregate":  40
}
EOF

cat > data/dsr_rates_2023_24.json << 'EOF'
{
  "note": "Delhi Schedule of Rates 2023-24 reference values (North India)",
  "region": "Delhi NCR / North India",
  "year": "2023-24",
  "rates": {
    "residential_per_sqft_economy":  1800,
    "residential_per_sqft_standard": 2400,
    "residential_per_sqft_premium":  3500,
    "commercial_per_sqft":           3200,
    "industrial_per_sqft":           2800
  }
}
EOF

# ── notebooks/ ───────────────────────────────────────────────
mkdir -p notebooks
touch notebooks/EDA.ipynb
touch notebooks/model_benchmarking.ipynb
touch notebooks/what_if_playground.ipynb

# ── docs/ ────────────────────────────────────────────────────
mkdir -p docs/screenshots
touch docs/architecture.png
touch docs/api_reference.md

# ── tests/ ───────────────────────────────────────────────────
mkdir -p tests
touch tests/__init__.py
touch tests/test_api.py
touch tests/test_predict.py
touch tests/test_insights.py
touch tests/test_copilot.py

# ── Done ─────────────────────────────────────────────────────
echo ""
echo "✅  BuildSense AI scaffold complete!"
echo ""
echo "📁 Structure:"
echo "   api/           → FastAPI backend"
echo "   models/        → ML models + training scripts"
echo "   models/saved/  → Serialised .pkl artefacts"
echo "   frontend/      → Streamlit UI"
echo "   data/          → Training data + DSR references"
echo "   notebooks/     → Jupyter exploration"
echo "   docs/          → Diagrams + screenshots"
echo "   tests/         → Test suite"
echo ""
echo "🚀 Next steps:"
echo "   1. pip install -r requirements.txt"
echo "   2. cd models && python generate_data.py"
echo "   3. python train_cost.py && python train_time.py && python train_risk.py && python train_dcs.py"
echo "   4. cd ../api && uvicorn main:app --reload"
echo "   5. cd ../frontend && streamlit run app.py"
