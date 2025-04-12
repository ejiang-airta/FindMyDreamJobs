#!/bin/bash

# Download the spaCy model if not already present
python -m spacy download en_core_web_sm

# Start FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000
