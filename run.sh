#!/bin/bash

# Simple run script - No complexity!

cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"

echo "🚀 Starting Market Analyst Agent"
echo ""

# Check .env
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Create it with:"
    echo "  GOOGLE_API_KEY=your_key"
    echo "  OPENAI_API_KEY=your_key"
    echo "  PINECONE_API_KEY=your_key"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Run backend
echo "✅ Starting backend on http://localhost:8000"
python src/main.py

