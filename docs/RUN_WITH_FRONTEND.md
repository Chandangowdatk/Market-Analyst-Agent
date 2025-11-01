# 🎨 Run with Frontend - Complete Guide

## 🎯 What You Get

A beautiful web interface where you can:
- ✅ **Drag & drop documents** to upload
- ✅ **Chat with your documents** using AI
- ✅ **See real-time responses** with tool usage
- ✅ **Monitor system status** live

---

## 🚀 Quick Start (2 Terminals)

### **Terminal 1: Start Backend (API Server)**

```bash
cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"
./start.sh
```

**Wait for:**
```
✅ Starting FastAPI server...
Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal open! ✋

---

### **Terminal 2: Start Frontend (Web UI)**

```bash
cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"
./run_frontend.sh
```

**You'll see:**
```
🌐 Starting Frontend Server
✅ Frontend will be available at:
   → http://localhost:3000
```

---

### **Terminal 3: Open in Browser**

```bash
open http://localhost:3000
```

**Or manually open:** http://localhost:3000

---

## 🎨 Using the Frontend

### **Left Panel: Document Upload**

1. **Drag & drop** your `.txt` file into the upload area
2. **Or click** to browse and select a file
3. **Watch** as it processes and uploads to the RAG pipeline
4. **Status shows:** "✅ Success! X chunks created"

### **Right Panel: Chat Interface**

1. **Type** your question in the input box
2. **Press Enter** or click the send button
3. **Watch** as the AI processes your query
4. **See** the answer with:
   - Tool used (qa_tool, insights_tool, or extract_tool)
   - Execution time
   - Source citations

### **System Status (Bottom Left)**

Shows:
- ✅ Connection status
- 📦 Number of vectors in database
- 🤖 AI model being used

---

## 📝 Example Workflow

### **Step 1: Upload Document**

Drag `data/innovate_inc_report.txt` to the upload area.

**Result:**
```
✅ Success! 5 chunks created
You can now ask questions about this document
```

---

### **Step 2: Ask Questions**

**Try these:**

**Q&A Questions** (uses qa_tool - RAG):
- "What is Innovate Inc's market share?"
- "Who are the main competitors?"
- "What are the company's strengths?"

**Insights Questions** (uses insights_tool):
- "Give me an executive summary"
- "Analyze the competitive landscape"
- "What are the key takeaways?"

**Data Extraction** (uses extract_tool):
- "Extract all data as JSON"
- "Give me structured data"

---

## 🎬 Visual Tour

```
┌────────────────────────────────────────────────────────┐
│  📊 Market Analyst Agent                               │
│  AI-powered market research analysis                   │
├────────────────────────────────────────────────────────┤
│                                                        │
│  📄 DROP YOUR DOCUMENT HERE                           │
│     or click to browse                                │
│     Supports .txt files                               │
│                                                        │
│  ⏳ Ready to upload...                                │
│                                                        │
│  🔧 System Status                                     │
│     ✅ Connected                                       │
│     📦 Vectors: 5                                     │
│     🤖 Model: gemini-2.5-flash                        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│  Ask Questions                                         │
│  🟢 Ready to answer                                    │
├────────────────────────────────────────────────────────┤
│                                                        │
│  👤 What is the market share?                         │
│                                                        │
│  🤖 Innovate Inc. holds a 12% market share.           │
│     qa_tool • 2500ms                                  │
│     📚 Sources: 3. Competitive Landscape              │
│                                                        │
├────────────────────────────────────────────────────────┤
│  [Type your question here...                    ] ➤   │
└────────────────────────────────────────────────────────┘
```

---

## 🔧 Features

### **Upload Section**
- ✅ Drag & drop support
- ✅ File type validation (.txt)
- ✅ Upload progress indicator
- ✅ Success/error messages
- ✅ Chunk count display

### **Chat Section**
- ✅ Beautiful message bubbles
- ✅ User vs Agent differentiation
- ✅ Loading animation while processing
- ✅ Tool badge showing which tool was used
- ✅ Execution time display
- ✅ Source citations
- ✅ Auto-scroll to latest message
- ✅ Keyboard support (Enter to send)

### **System Monitoring**
- ✅ Real-time health checks
- ✅ Vector count monitoring
- ✅ Connection status
- ✅ Auto-refresh every 30 seconds

---

## 🎯 Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Browser   │ ---> │   Frontend  │ ---> │   Backend   │
│ (You!)      │      │   :3000     │      │   :8000     │
└─────────────┘      └─────────────┘      └─────────────┘
                            │                     │
                            │                     ↓
                            │              ┌─────────────┐
                            │              │   Pinecone  │
                            │              │  Vector DB  │
                            │              └─────────────┘
                            │                     │
                            │                     ↓
                            │              ┌─────────────┐
                            └─────────────>│   Gemini    │
                                          │     LLM     │
                                          └─────────────┘
```

---

## 🐛 Troubleshooting

### **Problem: Frontend won't load**

**Solution:**
```bash
# Check if backend is running
curl http://localhost:8000/api/health

# If not, start it:
./start.sh
```

---

### **Problem: "Cannot connect to server"**

**Check:**
1. Is backend running? (Terminal 1 should show "Uvicorn running")
2. Is it on port 8000? (Check terminal output)
3. CORS enabled? (Already configured in main.py)

---

### **Problem: Upload fails**

**Check:**
1. File is `.txt` format
2. File size is reasonable (< 10MB)
3. Backend has write permissions
4. API keys are configured in `.env`

---

### **Problem: Chat not responding**

**Check:**
1. Did you initialize vector store? (`./init_vectorstore.sh`)
2. Are API keys valid in `.env`?
3. Check backend terminal for error messages

---

## 🎨 Customization

### **Change Frontend Port**

Edit `run_frontend.sh`:
```bash
python3 -m http.server 3000  # Change 3000 to your port
```

### **Change Backend Port**

Edit `src/main.py`:
```python
uvicorn.run("...", port=8000)  # Change 8000 to your port
```

Then update frontend's `API_URL` in `index.html`:
```javascript
const API_URL = 'http://localhost:8000';  // Update port
```

---

## 🚀 Production Deployment

For production:

1. **Build frontend** (optional - use frameworks like React/Vue)
2. **Use Nginx** as reverse proxy
3. **Add authentication** (JWT tokens)
4. **Enable HTTPS** (SSL certificates)
5. **Use process manager** (PM2, systemd)
6. **Add monitoring** (Sentry, Datadog)

---

## 📊 Performance

- **Frontend:** Instant UI, no build needed
- **Backend:** Fast API responses (< 3s typical)
- **Upload:** Depends on file size
- **Chat:** Real-time streaming (can be added)

---

## 🎉 You're Ready!

```bash
# Terminal 1:
./start.sh

# Terminal 2:
./run_frontend.sh

# Browser:
http://localhost:3000
```

**Enjoy your beautiful Market Analyst Agent!** 🚀

