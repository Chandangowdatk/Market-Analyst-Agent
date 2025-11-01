"""
Q&A Tool using RAG (Retrieval-Augmented Generation).
"""
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
try:
    from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore[import-not-found]
except Exception:
    class ChatGoogleGenerativeAI:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "langchain_google_genai is not installed. Add 'langchain-google-genai' to requirements and install."
            )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from services.vector_store import VectorStoreManager


# Initialize components
vector_store_manager = VectorStoreManager()
# Get retriever with lower threshold for better recall
retriever = vector_store_manager.get_retriever(k=8, score_threshold=0.3)

llm = ChatGoogleGenerativeAI(
    model=Config.GEMINI_MODEL,
    google_api_key=Config.GOOGLE_API_KEY,
    temperature=0,
    convert_system_message_to_human=True  # Required for Gemini
)


@tool
def qa_tool(query: str) -> str:
    """
    Answer specific FACTUAL questions about the Innovate Inc. market research report.
    
    Use this tool for:
    - Questions starting with What, When, Who, Which, How many
    - Specific data lookups (market share, growth rates, competitors)
    - Company information queries
    - SWOT analysis questions
    
    Examples:
    - "What is Innovate Inc's current market share?"
    - "Who are the main competitors?"
    - "What are the company's weaknesses?"
    - "How much is the market projected to grow?"
    
    Args:
        query: The factual question to answer from the report
        
    Returns:
        Answer with source citations from the report
    """
    try:
        # Retrieve relevant documents (LangChain 1.0 uses .invoke() instead of .get_relevant_documents())
        try:
            source_docs = retriever.invoke(query)
            
            # Fallback: if threshold filtering removed all docs, try without threshold
            if not source_docs:
                fallback_retriever = vector_store_manager.get_retriever(k=8, score_threshold=None)
                source_docs = fallback_retriever.invoke(query)
                
        except Exception as retriever_error:
            return f"Error retrieving documents: {str(retriever_error)}. Please check if documents are uploaded and the vector store is configured correctly."

        # Prepare context
        if not source_docs:
            return "No relevant documents found in the vector database. Please upload a .txt file first via the upload endpoint."

        context = "\n\n".join(doc.page_content for doc in source_docs)

        # Check if context is empty
        if not context.strip():
            return "Documents retrieved but no content found. Please check the uploaded document format."

        # Build prompt template (proper messages format for Gemini)
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful analyst. Use the provided context to answer the question concisely. If the answer cannot be found in the context, say you don't know."),
            ("human", "Context:\n{context}\n\nQuestion: {query}")
        ])

        # Create chain and invoke
        try:
            chain = qa_prompt | llm
            answer_msg = chain.invoke({
                "context": context,
                "query": query
            })
        except Exception as llm_error:
            return f"Error calling language model: {str(llm_error)}. Please check API key and model configuration."

        # Normalize answer text
        try:
            answer = getattr(answer_msg, "content", None) or str(answer_msg)
        except Exception:
            answer = str(answer_msg)
        
        if not answer or answer.strip() == "":
            return "Received empty response from the language model. Please try again."

        # Extract sources
        sources = [
            doc.metadata.get("section", "Unknown Section")
            for doc in source_docs
        ]
        
        # Format response with citations
        unique_sources = list(set(sources))
        if unique_sources:
            citations = f"\n\n📚 Sources: {', '.join(unique_sources)}"
            return f"{answer}{citations}"
        
        return answer
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Error processing query: {str(e)}\n\nDetails: {error_details[:500]}"  # Limit error details length