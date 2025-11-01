# 🎨 Frontend Quick Start - One Command!

## ⚡ Super Simple Launch

### **ONE command to rule them all:**

```bash
cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"
./run_all.sh
```

**This automatically:**
- ✅ Starts the backend (API server)
- ✅ Starts the frontend (Web UI)
- ✅ Opens your browser to http://localhost:3000

---

## 🎯 What You'll See

A beautiful web interface with:

```
┌─────────────────────┬──────────────────────────────┐
│  📊 Upload Panel    │  💬 Chat Panel               │
│                     │                              │
│  Drop files here    │  Ask your questions          │
│  [Upload Area]      │  [Chat Interface]            │
│                     │                              │
│  System Status:     │  👤 What's the market share? │
│  ✅ Connected       │  🤖 Innovate Inc holds 12%   │
│  📦 Vectors: 5      │      with sources...         │
└─────────────────────┴──────────────────────────────┘
```

---

## 📝 How to Use

### **1. Upload a Document**
- **Drag & drop** your `.txt` file to the left panel
- Or **click** the upload area to browse
- Wait for "✅ Success!"

### **2. Ask Questions**
- **Type** in the chat box (right panel)
- **Press Enter** or click send button
- **Watch** the AI respond with:
  - Answer
  - Which tool was used
  - Source citations

---

## 🔥 Try These Questions

**Factual (RAG):**
- "What is Innovate Inc's market share?"
- "Who are the main competitors?"
- "What are the company's weaknesses?"

**Analysis:**
- "Give me an executive summary"
- "What are the key opportunities?"
- "Analyze the competitive landscape"

**Data Export:**
- "Extract all data as JSON"
- "Give me structured data"

---

## 🛑 Stop Everything

```bash
./stop_all.sh
```

Or manually:
```bash
# Find and kill processes
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

---

## 📱 Quick Reference

| Action | Command |
|--------|---------|
| **Start Everything** | `./run_all.sh` |
| **Stop Everything** | `./stop_all.sh` |
| **Open Frontend** | http://localhost:3000 |
| **API Docs** | http://localhost:8000/docs |
| **View Logs** | `tail -f backend.log` |

---

## ✅ That's It!

```bash
./run_all.sh
```

**Your browser will open automatically!** 🎉

---

## 🎬 Demo Flow

```bash
# 1. Start
./run_all.sh

# 2. Browser opens automatically
#    → Drag innovate_inc_report.txt to upload area
#    → Type: "What is the market share?"
#    → Get instant answer with citations

# 3. When done
./stop_all.sh
```

**It's that simple!** 🚀

---

## 🐛 Troubleshooting

**Problem: "Port already in use"**
```bash
./stop_all.sh  # Stop any existing processes
./run_all.sh   # Try again
```

**Problem: ".env file not found"**
```bash
# Create it first (see START_HERE.md)
cat > .env << EOF
GOOGLE_API_KEY=your_key
OPENAI_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=market-analyst-index
EOF
```

**Problem: "Cannot connect to server"**
```bash
# Check backend log
tail -f backend.log
```

---

**Need detailed docs?** → See `RUN_WITH_FRONTEND.md`

**Just want to start?** → Run `./run_all.sh` ⚡

