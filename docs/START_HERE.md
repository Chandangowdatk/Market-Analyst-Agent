# ⚡ START HERE - One Page Guide

## 🎯 What You're Building

A smart system that answers questions about your market research document.

---

## 📋 Setup (Do This Once)

### Step 1: Get 3 API Keys

| Service | URL | What It Does |
|---------|-----|--------------|
| Google Gemini | https://makersuite.google.com/app/apikey | Answers questions |
| OpenAI | https://platform.openai.com/api-keys | Searches documents |
| Pinecone | https://app.pinecone.io/ | Stores document chunks |

### Step 2: Save Keys

```bash
cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"

# Create .env file
cat > .env << EOF
GOOGLE_API_KEY=your_actual_google_key
OPENAI_API_KEY=your_actual_openai_key
PINECONE_API_KEY=your_actual_pinecone_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=market-analyst-index
EOF
```

### Step 3: Load Document into Database

```bash
./init_vectorstore.sh
```

**✅ Setup complete!** You only do this once.

---

## 🚀 Run It (Do This Every Time)

```bash
./start.sh
```

**Server runs at:** http://localhost:8000

**Keep this terminal open!**

---

## 🧪 Test It

**Option 1: Browser** (Easiest)
```
Open: http://localhost:8000/docs
```

**Option 2: Terminal** (Quick test)
```bash
# New terminal window:
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the market share?"}'
```

**Expected Answer:**
```json
{
  "answer": "Innovate Inc. holds a 12% market share.",
  "tool_used": "qa_tool"
}
```

---

## 🎯 That's It!

```
Setup (once)  →  Run (anytime)  →  Test  →  Done! ✅
```

**Having issues?** Check `SIMPLE_SETUP.md` for detailed help.

