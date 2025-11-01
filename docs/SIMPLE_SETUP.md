# 🎯 SIMPLE SETUP - No Confusion!

## 📖 Understanding the System First

Think of your system as a **restaurant**:

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR SYSTEM                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  👤 Customer (User)                                     │
│       ↓                                                 │
│       "What's the market share?"                        │
│       ↓                                                 │
│  🤖 Waiter (Agent)                                      │
│       ↓                                                 │
│       Decides which chef to ask                         │
│       ↓                                                 │
│  👨‍🍳 Three Chefs (Tools):                               │
│       • Q&A Chef (searches documents)    ← RAG HERE!   │
│       • Insights Chef (analyzes trends)                 │
│       • Extract Chef (formats data as JSON)             │
│       ↓                                                 │
│  📚 Kitchen Storage (Pinecone Database)                 │
│       Contains pre-processed document chunks            │
│       ↓                                                 │
│  ✅ Answer served back to customer                      │
└─────────────────────────────────────────────────────────┘
```

## 🎭 Two Separate Stages

### **STAGE 1: SETUP THE KITCHEN** (Do once)
Prepare the ingredients (load documents into database)

### **STAGE 2: SERVE CUSTOMERS** (Run anytime)
Take orders and serve answers

---

# 🔧 STAGE 1: SETUP THE KITCHEN (One-Time)

## Step 1.1: Get Your Keys (Ingredients)

You need 3 API keys (like getting supplies):

```bash
# Open these websites and get your keys:
# 1. Google (for AI): https://makersuite.google.com/app/apikey
# 2. OpenAI (for search): https://platform.openai.com/api-keys
# 3. Pinecone (for storage): https://app.pinecone.io/
```

## Step 1.2: Store Your Keys

```bash
cd "/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"

# Create a file to store your keys
nano .env
```

Paste this and replace with YOUR keys:

```
GOOGLE_API_KEY=paste_your_google_key_here
OPENAI_API_KEY=paste_your_openai_key_here
PINECONE_API_KEY=paste_your_pinecone_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=market-analyst-index
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

## Step 1.3: Load Documents into Database (The RAG Setup!)

**This is the "RAG setup" everyone talks about!**

```bash
./init_vectorstore.sh
```

**What happens behind the scenes:**

```
📄 Read document: data/innovate_inc_report.txt
    ↓
✂️  Split into small chunks (5 chunks)
    ↓
🔢 Convert each chunk to numbers (embeddings)
    ↓
📤 Upload to Pinecone database
    ↓
✅ Done! RAG is ready!
```

**You'll see:**
```
✅ Created 5 chunks
✅ Successfully ingested 5 chunks
📦 Namespace: innovate_inc
🎉 Vector store initialized!
```

**That's it! RAG is now set up!** 🎉

---

# 🚀 STAGE 2: SERVE CUSTOMERS (Every Time You Want to Use It)

## Step 2.1: Open the Restaurant

```bash
./start.sh
```

**You'll see:**
```
✅ Starting FastAPI server...
Server will be available at:
  → http://localhost:8000
```

**Keep this terminal open!** (It's like keeping the restaurant open)

---

## Step 2.2: Test If It's Working

Open a **NEW terminal** (don't close the first one!) and try:

### Test 1: Is the kitchen open?

```bash
curl http://localhost:8000/api/health
```

**Good response:**
```json
{"status": "healthy"}
```

### Test 2: Ask a question (RAG in action!)

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the market share?"}'
```

**Good response:**
```json
{
  "answer": "Innovate Inc. holds a 12% market share.",
  "tool_used": "qa_tool"
}
```

**🎉 If you see this, RAG is working!**

---

# 🔍 Understanding RAG (The Magic Explained)

When you ask "What is the market share?", here's what happens:

```
1. Your Question
   "What is the market share?"
        ↓
2. Convert to Numbers (Embedding)
   [0.123, -0.456, 0.789, ...] (1536 numbers)
        ↓
3. Search Pinecone Database
   Find similar chunks from the document
   ↓ Found 4 relevant chunks:
   • "Innovate Inc. holds a 12% market share..."
   • "Primary competitors are Synergy Systems..."
   • "The global market is valued at $15 billion..."
   • "Well-positioned for growth..."
        ↓
4. Send to AI (Gemini)
   AI: "Based on these chunks, the answer is..."
        ↓
5. Get Answer
   "Innovate Inc. holds a 12% market share."
        ↓
6. Add Citation
   "📚 Sources: Section 3. Competitive Landscape"
```

**That's RAG!** Retrieve → Augment → Generate

---

# 🎯 Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                  HOW YOUR SYSTEM WORKS                      │
└─────────────────────────────────────────────────────────────┘

SETUP (Once):
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Document │ --> │  Chunks  │ --> │ Pinecone │
│   .txt   │     │   1-5    │     │ Database │
└──────────┘     └──────────┘     └──────────┘
    Load          Process         Store

INTERACTION (Every query):
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │ --> │  Agent   │ --> │   Tool   │ --> │  Answer  │
│  Query   │     │  Routes  │     │  Searches│     │   Back   │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
  "Question"      Picks tool      Uses RAG        With citation
```

---

# ✅ Checklist: Am I Set Up Correctly?

Run through this checklist:

- [ ] I created `.env` file with my 3 API keys
- [ ] I ran `./init_vectorstore.sh` (saw "Successfully ingested")
- [ ] I ran `./start.sh` (server is running)
- [ ] I tested with `curl http://localhost:8000/api/health`
- [ ] I asked a question and got an answer with citations

**If all checked ✅ → You're done! System is working!**

---

# 🤔 Common Confusions Clarified

## "What is RAG setup?"

**RAG setup = Loading documents into Pinecone**

That's what `./init_vectorstore.sh` does. You do it once.

## "What is interaction?"

**Interaction = Starting the server and asking questions**

That's what `./start.sh` does. You do this every time you want to use it.

## "Do I need to run both?"

**Yes, but in order:**

1. **First time:** Run `init_vectorstore.sh` (setup RAG)
2. **Every time:** Run `start.sh` (start server)
3. **Then:** Ask questions (interact)

## "How do I know RAG is working?"

**When you get an answer WITH citations:**

```
Answer: "Innovate Inc. holds a 12% market share."
📚 Sources: 3. Competitive Landscape
         ↑
This proves RAG found and used the document!
```

---

# 🎮 Interactive Testing (Easiest Way!)

Instead of curl commands, use your browser:

```bash
# 1. Start server
./start.sh

# 2. Open browser
open http://localhost:8000/docs
```

You'll see a nice interface where you can:
- Click on `/api/query`
- Click "Try it out"
- Type your question
- Click "Execute"
- See the answer instantly!

---

# 🚨 Troubleshooting

## Problem: "Command not found: ./start.sh"

**Solution:**
```bash
chmod +x start.sh init_vectorstore.sh
```

## Problem: "Module not found"

**Solution:**
```bash
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Problem: "API key invalid"

**Solution:**
- Check your `.env` file
- Make sure there are no extra spaces
- Make sure you copied the FULL key

## Problem: "No answer returned"

**Solution:**
Did you run `./init_vectorstore.sh` first?
This loads the documents into Pinecone.

---

# 📝 Quick Reference Card

```bash
# ONE-TIME SETUP:
1. Get API keys from websites
2. Create .env file with keys
3. Run: ./init_vectorstore.sh

# EVERY TIME YOU USE IT:
1. Run: ./start.sh
2. Open new terminal
3. Test: curl http://localhost:8000/api/health
4. Ask: curl -X POST http://localhost:8000/api/query \
       -H "Content-Type: application/json" \
       -d '{"query": "Your question here"}'

# OR USE BROWSER:
1. Run: ./start.sh
2. Visit: http://localhost:8000/docs
3. Click and type!
```

---

# 🎯 Summary

**RAG Setup (Once):**
- Get keys → Create .env → Run init script

**Interaction (Every time):**
- Start server → Ask questions → Get answers

**That's it!** No more confusion! 🎉

---

**Need help?** Just follow the checklist above step by step!

