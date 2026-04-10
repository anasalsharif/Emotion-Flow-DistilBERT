from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from preprocess import NLPPreprocessor

# Initialize Preprocessor
preprocessor = NLPPreprocessor()

# Initialize FastAPI app
app = FastAPI(
    title="Emotion Flow API",
    description="Real-time Emotion Classification using DistilBERT",
    version="1.0.0"
)

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pre-trained model for emotion
MODEL_NAME = "bhadresh-savani/distilbert-base-uncased-emotion"

try:
    print(f"Loading model: {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    
    # Move model to device
    device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
    print(f"Using device: {device}")
    model.to(device)
    model.eval()
except Exception as e:
    print(f"Failed to load model: {e}")
    # Fallback

class EmotionRequest(BaseModel):
    text: str

class EmotionResponse(BaseModel):
    label: str
    score: float
    all_scores: dict
    processed_text: str

@app.post("/predict", response_model=EmotionResponse)
async def predict_emotion(req: EmotionRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
    # 1. Classical NLP Preprocessing (Regex + Edit Distance)
    preprocessed_data = preprocessor.process(req.text)
    clean_text = preprocessed_data["processed"]
        
    inputs = tokenizer(clean_text, return_tensors="pt", truncation=True, max_length=512)
    
    # Move inputs to same device as model
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=1)[0]
    
    # Get top prediction
    top_class_idx = torch.argmax(probabilities).item()
    top_class_label = model.config.id2label[top_class_idx]
    top_score = probabilities[top_class_idx].item()
    
    # Map all scores for the charts
    all_scores = {
        model.config.id2label[i]: round(prob.item(), 4)
        for i, prob in enumerate(probabilities)
    }
    
    return {
        "label": top_class_label,
        "score": round(top_score, 4),
        "all_scores": all_scores,
        "processed_text": clean_text
    }

@app.get("/")
def health_check():
    return {"status": "ok", "model": MODEL_NAME}
