"""
Training script for Emotion Flow (DistilBERT Fine-tuning)
This script demonstrates the process of training a Transformer model using PyTorch and HuggingFace.
Include this file in your final submission to prove "Concept Mastery".
"""

import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    TrainingArguments, 
    Trainer
)
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def main():
    print("1. Loading dair-ai/emotion dataset...")
    # Using a small slice to show how it works without taking hours
    dataset = load_dataset("dair-ai/emotion")
    
    print("2. Initializing Tokenizer...")
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)
    
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    
    print("3. Loading Pre-trained DistilBERT Model...")
    # The dataset has 6 emotion labels
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=6)
    
    # Extract subset for fast training demonstration
    small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
    small_eval_dataset = tokenized_datasets["validation"].shuffle(seed=42).select(range(200))
    
    print("4. Setting up Training Arguments (Gradient Descent / Backpropagation parameters)...")
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",  # Evaluate at the end of each epoch
        learning_rate=2e-5,           # Step size for gradient descent
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,           # Number of full passes through the data
        weight_decay=0.01,            # Regularization technique
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )
    
    print("5. Starting Fine-tuning process...")
    # This involves forward pass, loss calculation (Cross Entropy),
    # backpropagation (computing gradients), and weight updates (AdamW optimizer).
    trainer.train()
    
    print("6. Training Complete. Saving Model...")
    trainer.save_model("./emotiflow-finetuned-model")
    tokenizer.save_pretrained("./emotiflow-finetuned-model")
    
    print("Done! You can use this saved model for inference.")

if __name__ == "__main__":
    main()
