# Emotion Flow: Real-time Emotion Intelligence Dashboard

Emotion Flow is an intelligent application that classifies the emotional sentiment of text in real-time. It leverages a modern Transformer-based architecture (DistilBERT) and a classical NLP preprocessing pipeline.

## Features
- **Real-time Inference**: Fast emotion detection on CPU.
- **NLP Preprocessing**: Custom Regex normalization and Levenshtein Edit Distance for spell correction.
- **Interactive Dashboard**: Sleek Next.js frontend with live probability visualizations.
- **High Efficiency**: Uses DistilBERT for production-ready performance.

## Tech Stack
- **Frontend**: Next.js (TailwindCSS / Glassmorphism)
- **Backend**: FastAPI (Python)
- **AI Framework**: PyTorch & HuggingFace Transformers
- **Model**: `distilbert-base-uncased-emotion`

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+

### Running the Project
The easiest way to start both the backend and frontend is to use the provided run script:

Follow these steps to get everything running locally (recommended from project root):

1. Create and activate a virtual environment (macOS / Linux):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:

```bash
cd frontend && npm install && cd ..
```

4. Start both backend and frontend (from project root):

```bash
chmod +x run_project.sh
./run_project.sh
```

Quick verification

- Health check (backend):

```bash
curl http://localhost:8000/
```

- Run the demo test script (makes a few sample POST requests):

```bash
python3 test_surprise.py
```

Notes

- The model weights are downloaded from HuggingFace the first time the backend starts; an internet connection and some disk space are required.
- If the backend fails to start due to missing packages, re-run `pip install -r requirements.txt` while the virtual environment is active.

