# 🚀 How to Run the Market Analyst Agent

## ⚡ Quick Start (5 Steps)

### **Step 1: Create .env File** (First time only)

Create a file named `.env` in the project root:

```bash
cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"
touch .env
```

Add your API keys to `.env`:

```bash
# Required API Keys
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here

# Pinecone Configuration
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=market-analyst-index
```

**Get API Keys:**
- **Google (Gemini)**: https://makersuite.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys
- **Pinecone**: https://app.pinecone.io/

---

### **Step 2: Activate Virtual Environment**

```bash
cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

### **Step 3: Set Python Path**

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

Or for permanent setup, add to your `~/.zshrc`:

```bash
echo 'export PYTHONPATH="${PYTHONPATH}:/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"' >> ~/.zshrc
source ~/.zshrc
```

---

### **Step 4: Initialize Vector Store** (First time only)

This ingests the sample document into Pinecone:

```bash
python -c "
import sys
sys.path.insert(0, '.')

from src.services.vector_store import VectorStoreManager
from src.services.document_processor import DocumentProcessor

print('📚 Loading and processing document...')
processor = DocumentProcessor()
text = processor.load_document('data/innovate_inc_report.txt')
documents = processor.process_document(text, 'innovate_inc_report.txt')

print(f'✅ Created {len(documents)} chunks')
print('🔄 Uploading to Pinecone...')

vector_store = VectorStoreManager()
result = vector_store.ingest_documents(documents)

if result['status'] == 'success':
    print(f'✅ Successfully ingested {result[\"chunks_processed\"]} chunks')
    print(f'📦 Namespace: {result[\"namespace\"]}')
else:
    print(f'❌ Error: {result[\"error\"]}')
"
```

Expected output:
```
📚 Loading and processing document...
✅ Created 5 chunks
🔄 Uploading to Pinecone...
✅ Successfully ingested 5 chunks
📦 Namespace: innovate_inc
```

---

### **Step 5: Start the API Server**

```bash
python src/main.py
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

🎉 **Your Market Analyst Agent is now running!**

---

## 🧪 Testing the System

Open a **new terminal** (keep the server running) and test:

### **1. Health Check**

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "configuration": {
    "gemini_model": "gemini-2.5-flash",
    "embedding_model": "text-embedding-3-small",
    "pinecone_index": "market-analyst-index",
    "namespace": "innovate_inc",
    "langchain_version": "1.0.3"
  },
  "vector_store": {
    "total_vectors": 5,
    "dimension": 1536
  }
}
```

---

### **2. Test Q&A Tool** (Factual Questions)

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Innovate Inc'\''s current market share?"
  }'
```

Expected response:
```json
{
  "answer": "Innovate Inc. holds a 12% market share.\n\n📚 Sources: 3. Competitive Landscape",
  "tool_used": "qa_tool",
  "session_id": "session_1234567890",
  "execution_time_ms": 2500
}
```

---

### **3. Test Insights Tool** (Strategic Analysis)

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Give me an executive summary of the report"
  }'
```

Expected response:
```json
{
  "answer": "**Executive Summary**\n\nInnovate Inc. operates in the AI workflow automation market...\n\n---\n💡 Analysis Type: Strategic Insights",
  "tool_used": "insights_tool",
  "session_id": "session_1234567891",
  "execution_time_ms": 3200
}
```

---

### **4. Test Extract Tool** (JSON Data)

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Extract all data as JSON"
  }'
```

Expected response:
```json
{
  "answer": "{\n  \"company_name\": \"Innovate Inc.\",\n  \"product_name\": \"Automata Pro\",\n  ...\n}",
  "tool_used": "extract_tool",
  "session_id": "session_1234567892",
  "execution_time_ms": 4100
}
```

---

### **5. Test Document Upload**

Upload a new document:

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@data/innovate_inc_report.txt"
```

Expected response:
```json
{
  "message": "Document processed successfully",
  "filename": "innovate_inc_report.txt",
  "chunks_created": 5,
  "namespace": "innovate_inc",
  "status": "success"
}
```

---

## 🌐 Interactive Testing (Browser)

Visit in your browser:

```
http://localhost:8000/docs
```

This opens **Swagger UI** where you can:
- ✅ Test all endpoints interactively
- ✅ See request/response schemas
- ✅ Try different queries

---

## 📋 Complete Run Script

Save this as `run.sh`:

```bash
#!/bin/bash

# Market Analyst Agent - Run Script

PROJECT_DIR="/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"

echo "🚀 Starting Market Analyst Agent..."

# Step 1: Navigate to project
cd "$PROJECT_DIR" || exit 1

# Step 2: Activate venv
source venv/bin/activate

# Step 3: Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Step 4: Check .env file
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "→ Please create .env with your API keys"
    exit 1
fi

# Step 5: Start server
echo "✅ Starting FastAPI server..."
python src/main.py
```

Make it executable:
```bash
chmod +x run.sh
./run.sh
```

---

## 🔧 Troubleshooting

### **Problem: Import Errors**

```
ModuleNotFoundError: No module named 'Market_Analyst_Agent'
```

**Solution:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

### **Problem: API Key Errors**

```
Error: GOOGLE_API_KEY not found
```

**Solution:**
1. Check `.env` file exists
2. Check API keys are valid (no quotes needed)
3. Restart the server after editing `.env`

---

### **Problem: Pinecone Connection Failed**

```
Error: Failed to connect to Pinecone
```

**Solution:**
1. Verify `PINECONE_API_KEY` is correct
2. Check `PINECONE_ENVIRONMENT` matches your Pinecone dashboard
3. Ensure internet connection is active

---

### **Problem: Port Already in Use**

```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use a different port
python src/main.py --port 8001
```

---

### **Problem: Virtual Environment Not Found**

```
source: no such file or directory: venv/bin/activate
```

**Solution:**
```bash
# Recreate venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📊 What Happens When You Run

```
┌─────────────────────────────────────────────┐
│  1. Load .env file                           │
│     → Read API keys                          │
├─────────────────────────────────────────────┤
│  2. Initialize Vector Store                  │
│     → Connect to Pinecone                    │
│     → Load OpenAI embeddings                 │
├─────────────────────────────────────────────┤
│  3. Initialize Tools                         │
│     → qa_tool (RAG pipeline)                 │
│     → insights_tool (full doc analysis)      │
│     → extract_tool (structured extraction)   │
├─────────────────────────────────────────────┤
│  4. Create Agent                             │
│     → Initialize Gemini LLM                  │
│     → Create ReAct agent                     │
│     → Setup AgentExecutor                    │
├─────────────────────────────────────────────┤
│  5. Start FastAPI Server                     │
│     → Listen on http://0.0.0.0:8000          │
│     → Enable CORS                            │
│     → Ready for requests                     │
└─────────────────────────────────────────────┘
```

---

## 🎯 Typical Workflow

```bash
# Terminal 1: Start server
cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python src/main.py

# Terminal 2: Test queries
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the market size?"}'

# Terminal 3: Monitor logs
tail -f logs/app.log  # if you add logging
```

---

## 📱 Development Tips

### **Enable Verbose Mode**

To see agent reasoning, the agent already has `verbose=True` in `agent.py`:

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # ✅ Already enabled
    ...
)
```

You'll see output like:
```
> Entering new AgentExecutor chain...
I need to find the market share information.
Action: qa_tool
Action Input: What is Innovate Inc's market share?
Observation: Innovate Inc. holds a 12% market share...
Thought: I have the answer.
Final Answer: Innovate Inc. holds a 12% market share.
> Finished chain.
```

---

### **Hot Reload During Development**

FastAPI has auto-reload enabled in `main.py`:

```python
uvicorn.run(
    "Market_Analyst_Agent.src.main:app",
    host="0.0.0.0",
    port=8000,
    reload=True  # ✅ Auto-reload on code changes
)
```

Edit any Python file → server restarts automatically!

---

## 🎉 Success Checklist

Before considering it "working":

- ✅ `.env` file created with valid API keys
- ✅ Virtual environment activated
- ✅ PYTHONPATH set correctly
- ✅ Vector store initialized (documents ingested)
- ✅ Server starts without errors
- ✅ Health endpoint returns "healthy"
- ✅ Q&A tool responds with citations
- ✅ Insights tool provides analysis
- ✅ Extract tool returns valid JSON

---

## 🚀 Production Deployment

For production, consider:

1. **Use process manager**: `gunicorn` or `supervisor`
2. **Add authentication**: JWT or API keys
3. **Add rate limiting**: Prevent abuse
4. **Setup monitoring**: Track errors and performance
5. **Use environment variables**: Don't commit `.env`
6. **Add caching**: Redis for frequent queries
7. **Setup CI/CD**: Automated testing and deployment

---

**You're ready to run! Start with Step 1 if you haven't created `.env` yet.** 🚀

