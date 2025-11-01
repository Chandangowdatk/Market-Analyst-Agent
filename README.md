# 📊 AI Market Analyst Agent

A full-stack AI-powered market research analysis system built with LangChain, FastAPI, and React. This intelligent agent uses RAG (Retrieval-Augmented Generation) with Pinecone vector database to provide Q&A, strategic insights, and structured data extraction from market research documents.

## ✨ Features

- **🤖 Multi-Tool Agent**: Automatically routes queries to specialized tools
  - **Q&A Tool**: Answer specific factual questions with source citations
  - **Insights Tool**: Generate strategic summaries and market analysis
  - **Extract Tool**: Export structured data in JSON format
  
- **📄 RAG Pipeline**: Upload documents → Process & Chunk → Embed → Store in Pinecone
- **🎨 Minimal UI**: Clean, Gemini-inspired dark interface
- **⚡ Real-time Processing**: Fast document ingestion and query responses
- **🔍 Semantic Search**: Advanced vector similarity search with HuggingFace embeddings

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  (Minimal, aesthetic UI)
└────────┬────────┘
         │
    ┌────▼────┐
    │ FastAPI │  (REST API)
    └────┬────┘
         │
    ┌────▼────────────────┐
    │ LangChain Agent     │
    │ (Gemini 2.5 Flash)  │
    └─────┬───────────────┘
          │
    ┌─────▼──────┬──────────┬──────────┐
    │  QA Tool   │ Insights │ Extract  │
    └─────┬──────┴────┬─────┴────┬─────┘
          │           │          │
    ┌─────▼───────────▼──────────▼─────┐
    │   Pinecone Vector Database        │
    │   (all-MiniLM-L12-v2 embeddings)  │
    └───────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- Google Gemini API key
- Pinecone API key

### Backend Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Market_Analyst_Agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required environment variables:
- `GOOGLE_API_KEY`: Your Google Gemini API key
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENVIRONMENT`: Pinecone environment (e.g., `us-east-1`)
- `PINECONE_INDEX_NAME`: Your Pinecone index name

5. **Run the backend**
```bash
python src/main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Start the development server**
```bash
npm start
```

The UI will be available at `http://localhost:3000`

## 📖 Usage

### 1. Upload Documents

Click the **"+"** icon or **"Upload Document"** chip to upload a `.txt` market research document. The system will:
- Process the document into semantic chunks
- Generate embeddings using `all-MiniLM-L12-v2`
- Store vectors in Pinecone

### 2. Ask Questions

Type your query in the input field. The agent automatically routes to the appropriate tool:

**Q&A queries:**
```
What is their flagship product?
Who are the main competitors?
What is the market size?
```

**Insights queries:**
```
Summarize the key findings
What are the strategic opportunities?
Give me an overview of the competitive landscape
```

**Extract queries:**
```
Extract all data as JSON
Give me the structured data from the report
```

## 🛠️ Tech Stack

### Backend
- **LangChain 1.0.3**: Agent orchestration and RAG
- **FastAPI**: REST API framework
- **Google Gemini 2.5 Flash**: LLM for agent and tools
- **Pinecone**: Serverless vector database
- **HuggingFace Transformers**: Embedding model (`all-MiniLM-L12-v2`)
- **Pydantic**: Data validation

### Frontend
- **React 18**: UI framework
- **Material-UI (MUI)**: Component library
- **Axios**: HTTP client

## 📁 Project Structure

```
Market_Analyst_Agent/
├── src/
│   ├── agent.py              # LangChain agent setup
│   ├── main.py               # FastAPI application
│   ├── config.py             # Configuration management
│   ├── tools/
│   │   ├── qa_tool.py        # Q&A with RAG
│   │   ├── insights_tool.py  # Strategic insights
│   │   └── extract_tool.py   # Structured data extraction
│   ├── services/
│   │   ├── vector_store.py   # Pinecone operations
│   │   └── document_processor.py  # Document chunking
│   └── schemas/
│       └── models.py         # Pydantic models
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   └── App.css           # Styling
│   └── package.json
├── data/
│   └── innovate_inc_report.txt  # Sample document
├── requirements.txt
├── .env.example
└── README.md
```

## 🔑 API Endpoints

### `POST /api/upload`
Upload and process a document
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@document.txt"
```

### `POST /api/query`
Query the AI agent
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the market size?"}'
```

### `GET /api/health`
Health check and system status
```bash
curl http://localhost:8000/api/health
```

## 🧪 Example Queries

**Q&A:**
- "What is Innovate Inc's flagship product?"
- "Who are the main competitors?"
- "What is the current market size?"

**Insights:**
- "Summarize the SWOT analysis"
- "What are the key market opportunities?"
- "Give me strategic insights about the competitive landscape"

**Extract:**
- "Extract all data as JSON"
- "Give me the structured market data"

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Vector storage by [Pinecone](https://www.pinecone.io/)
- UI inspired by Google Gemini interface

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ using LangChain, FastAPI, and React
