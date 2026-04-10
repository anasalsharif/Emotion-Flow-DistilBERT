#!/bin/bash
echo "Starting Emotion Flow Backend and Frontend..."

# Start backend in background
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend in foreground
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Cleanup on Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID" SIGINT

wait
