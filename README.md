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

```bash
chmod +x run_project.sh
./run_project.sh
```
