# 🚀 SIMPLE START - Ignore Everything Else!

## Just Do These 3 Things:

### 1. Create `.env` file (once)

```bash
cat > .env << 'EOF'
GOOGLE_API_KEY=your_google_key
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=market-analyst-index
EOF
```

Get keys from:
- https://makersuite.google.com/app/apikey
- https://platform.openai.com/api-keys
- https://app.pinecone.io/

### 2. Start backend

```bash
source venv/bin/activate
export PYTHONPATH="$(pwd):$PYTHONPATH"
python src/main.py
```

### 3. Open frontend (new terminal)

```bash
cd frontend
python3 -m http.server 3000
```

Then open: http://localhost:3000

---

## That's It!

**Ignore all the `.sh` scripts** - they're optional automation.

**Just run the 3 commands above manually.** Simple!

