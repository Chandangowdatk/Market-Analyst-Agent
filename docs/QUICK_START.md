# ⚡ QUICK START - 3 Commands

## 🎯 **First Time Setup** (Do Once)

### **1. Create .env file**

```bash
cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"
cat > .env << 'EOF'
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=market-analyst-index
EOF
```

**Replace the placeholder values with your actual API keys!**

Get keys from:
- **Google**: https://makersuite.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys
- **Pinecone**: https://app.pinecone.io/

---

### **2. Initialize Vector Store**

```bash
./init_vectorstore.sh
```

Expected output:
```
==========================================
📚 Initialize Vector Store (Pinecone)
==========================================
✅ Activating virtual environment...
✅ Loading document...
📚 Loading and processing document...
✅ Created 5 chunks
🔄 Uploading to Pinecone...
✅ Successfully ingested 5 chunks
📦 Namespace: innovate_inc

🎉 Vector store initialized! You can now run: ./start.sh
```

---

## 🚀 **Every Time You Want to Run**

### **3. Start the Server**

```bash
./start.sh
```

Expected output:
```
======================================
🚀 Market Analyst Agent - Quick Start
======================================
✅ Activating virtual environment...
✅ Checking vector store...
✅ Starting FastAPI server...

Server will be available at:
  → http://localhost:8000
  → http://localhost:8000/docs (Swagger UI)

Press CTRL+C to stop the server
```

---

## 🧪 **Test It Works**

Open a **new terminal** and run:

```bash
# Test health
curl http://localhost:8000/api/health

# Test Q&A
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Innovate Inc'\''s market share?"}'

# Or open in browser
open http://localhost:8000/docs
```

---

## 📝 **Summary**

```bash
# First time only:
1. Create .env with API keys
2. ./init_vectorstore.sh

# Every time:
3. ./start.sh

# Test:
4. curl http://localhost:8000/api/health
```

---

## 🔧 **Troubleshooting**

**Problem:** "Permission denied"
```bash
chmod +x start.sh init_vectorstore.sh
```

**Problem:** ".env not found"
```bash
# Create it manually or use the command from step 1
```

**Problem:** "Module not found"
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Need detailed help?** → See `RUN_GUIDE.md`

---

## 🎯 **That's It!**

You now have:
- ✅ Virtual environment with all packages
- ✅ LangChain 1.0.3 compatible code
- ✅ Simple scripts to run everything
- ✅ RAG pipeline ready to use

**Just run `./start.sh` and you're good to go!** 🚀

