"""
Strategic Insights and Summary Generation Tool.
"""
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from services.vector_store import VectorStoreManager


# Initialize components
vector_store_manager = VectorStoreManager()
# Get retriever with more documents for comprehensive analysis
retriever = vector_store_manager.get_retriever(k=10, score_threshold=0.3)

llm = ChatGoogleGenerativeAI(
    model=Config.GEMINI_MODEL,
    google_api_key=Config.GOOGLE_API_KEY,
    temperature=0.3,  # Slightly higher for creative analysis
    convert_system_message_to_human=True
)


@tool
def insights_tool(request: str) -> str:
    """
    Generate strategic insights, summaries, and market analysis from uploaded documents.
    
    Use this tool for:
    - Executive summaries and overviews
    - Strategic analysis and recommendations
    - Market trend analysis
    - Competitive landscape insights
    - Growth opportunity identification
    - Risk assessment and mitigation strategies
    - General "tell me about" or "summarize" requests
    
    Examples:
    - "Give me an executive summary of the report"
    - "What are the key market trends?"
    - "Analyze the competitive landscape"
    - "What strategic recommendations would you make?"
    - "Summarize the growth opportunities"
    - "Tell me about Innovate Inc's market position"
    
    Args:
        request: The analysis or summary request
        
    Returns:
        Comprehensive strategic insights and analysis
    """
    
    # Define analysis categories and prompts
    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior market research analyst and strategic advisor. 
Your role is to provide comprehensive, actionable insights based on market research data.

Guidelines:
1. Provide strategic, high-level analysis
2. Identify patterns, trends, and implications
3. Offer actionable recommendations when appropriate
4. Structure your response clearly with sections or bullet points
5. Be concise but thorough
6. Focus on strategic value, not just data repetition
7. Consider multiple perspectives (opportunities, risks, competitive dynamics)
8. Use professional business language

Always ground your analysis in the provided report data."""),
        ("human", """Market Research Report:
{document}

Analysis Request: {request}

Please provide comprehensive strategic insights addressing this request:""")
    ])
    
    try:
        # Retrieve relevant documents from vector store (uploaded files)
        # LangChain 1.0 uses .invoke() instead of .get_relevant_documents()
        try:
            source_docs = retriever.invoke(request)
            
            # Fallback: if threshold filtering removed all docs, try without threshold
            if not source_docs:
                fallback_retriever = vector_store_manager.get_retriever(k=10, score_threshold=None)
                source_docs = fallback_retriever.invoke(request)
        except Exception as retriever_error:
            return f"Error retrieving documents: {str(retriever_error)}. Please check if documents are uploaded and the vector store is configured correctly."
        
        # Combine retrieved documents
        if not source_docs:
            return "No documents found in the vector database. Please upload a .txt file first via the upload endpoint."
        
        document_context = "\n\n".join([
            f"Section: {doc.metadata.get('section', 'Unknown')}\n{doc.page_content}"
            for doc in source_docs
        ])
        
        # If no documents found, return helpful message
        if not document_context.strip():
            return "Documents retrieved but no content found. Please check the uploaded document format."
        
        # Create chain
        try:
            chain = analysis_prompt | llm
            
            # Execute analysis with retrieved context
            response = chain.invoke({
                "document": document_context,
                "request": request
            })
        except Exception as llm_error:
            return f"Error calling language model: {str(llm_error)}. Please check API key and model configuration."
        
        # Extract content
        insights = response.content if hasattr(response, 'content') else str(response)
        
        if not insights or insights.strip() == "":
            return "Received empty response from the language model. Please try again."
        
        # Add metadata footer
        footer = "\n\n---\n💡 **Analysis Type**: Strategic Insights\n📊 **Source**: Uploaded Documents"
        
        return f"{insights}{footer}"
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Error generating insights: {str(e)}\n\nDetails: {error_details[:500]}"

