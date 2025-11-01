"""
Structured Data Extraction Tool.
"""
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import json

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from schemas.models import MarketResearchData
from services.vector_store import VectorStoreManager


# Initialize components
vector_store_manager = VectorStoreManager()
# Get retriever with more documents for comprehensive extraction
retriever = vector_store_manager.get_retriever(k=15, score_threshold=0.3)

llm = ChatGoogleGenerativeAI(
    model=Config.GEMINI_MODEL,
    google_api_key=Config.GOOGLE_API_KEY,
    temperature=0,  # Deterministic for data extraction
)


@tool
def extract_tool(request: str) -> str:
    """
    Extract structured data from uploaded documents in JSON format.
    
    Use this tool for:
    - Requests for structured data or JSON output
    - Data extraction requests
    - When user asks for "all data" or "complete information"
    - Export or download requests
    
    Examples:
    - "Extract all data as JSON"
    - "Give me the structured data from the report"
    - "Export the report data"
    - "I need the data in JSON format"
    
    Args:
        request: Description of the extraction request
        
    Returns:
        JSON string with complete structured market research data
    """
    
    # Define the extraction prompt
    extraction_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a data extraction specialist. Extract information from the market research report into valid JSON format.

CRITICAL INSTRUCTIONS - READ CAREFULLY:
1. Extract ALL required fields - NEVER use 0 or "Unknown" unless the data is truly missing
2. For numbers: Extract the ACTUAL numeric value from the text:
   - "$15 billion" or "$15 billion" → 15.0
   - "22%" or "CAGR of 22%" → 22.0
   - "12% market share" or "holds a 12% market share" → 12.0
   - "over $40 billion" or "$40 billion by 2030" → 40.0
3. Company name: Extract the EXACT company name mentioned (usually in introduction or title)
4. Product name: Extract the EXACT product name in quotes or mentioned explicitly
5. Report period: Look for dates like "Q3 2025", "Q1 2024", etc. in the title or introduction
6. Competitors: Extract ALL competitors mentioned with their market shares - do not miss any!
7. SWOT: Extract ALL items from each category (strengths, weaknesses, opportunities, threats)
8. Return ONLY valid JSON - no markdown code blocks, no explanation, no comments

REQUIRED JSON STRUCTURE (all fields are required):
{{
  "company_name": "string (exact company name - usually in title or introduction)",
  "product_name": "string (exact product name - look for quoted names)",
  "report_period": "string (extract from title, e.g., 'Q3 2025')",
  "current_market_size_billions": float (extract the CURRENT market size number, e.g., 15.0 for "$15 billion"),
  "projected_market_size_2030_billions": float (extract the PROJECTED 2030 size, e.g., 40.0 for "$40 billion by 2030"),
  "cagr_percent": float (extract CAGR percentage, e.g., 22.0 for "22% CAGR"),
  "company_market_share_percent": float (extract the company's market share, e.g., 12.0 for "12% market share"),
  "competitors": [
    {{"company_name": "string", "market_share": float}},
    {{"company_name": "string", "market_share": float}}
    // Include ALL competitors mentioned
  ],
  "swot": {{
    "strengths": ["string", "string", ...],  // Extract ALL strengths listed
    "weaknesses": ["string", "string", ...],  // Extract ALL weaknesses listed
    "opportunities": ["string", "string", ...],  // Extract ALL opportunities listed
    "threats": ["string", "string", ...]  // Extract ALL threats listed
  }}
}}

EXAMPLES OF CORRECT EXTRACTION:
- Text: "currently valued at approximately $15 billion" → current_market_size_billions: 15.0
- Text: "CAGR of 22%" → cagr_percent: 22.0
- Text: "holds a 12% market share" → company_market_share_percent: 12.0
- Text: "reaching a potential market size of over $40 billion by 2030" → projected_market_size_2030_billions: 40.0
- Text: "Synergy Systems (18% market share)" → {{"company_name": "Synergy Systems", "market_share": 18.0}}
- Text: "Innovate Inc. Market Research Report - Q3 2025" → report_period: "Q3 2025"

DO NOT:
- Use 0 for numeric fields unless the value is truly missing
- Use "Unknown" for text fields unless the data is truly missing
- Skip any competitors mentioned in the document
- Miss any SWOT items listed"""),
        ("human", "Market Research Report:\n{document}\n\nExtract ALL data into the exact JSON structure above. Read the document carefully and extract the ACTUAL values mentioned. Return only valid JSON (no markdown, no code blocks):")
    ])
    
    try:
        # Retrieve relevant documents from vector store (uploaded files)
        # LangChain 1.0 uses .invoke() instead of .get_relevant_documents()
        try:
            source_docs = retriever.invoke(request)
            
            # Fallback: if threshold filtering removed all docs, try without threshold
            if not source_docs:
                fallback_retriever = vector_store_manager.get_retriever(k=15, score_threshold=None)
                source_docs = fallback_retriever.invoke(request)
        except Exception as retriever_error:
            return json.dumps({
                "error": "Error retrieving documents",
                "details": str(retriever_error),
                "message": "Please check if documents are uploaded and the vector store is configured correctly."
            }, indent=2)
        
        # Combine retrieved documents
        if not source_docs:
            return json.dumps({
                "error": "No documents found",
                "message": "Please upload a .txt file first via the upload endpoint."
            }, indent=2)
        
        # Clean PDF extraction artifacts (extra spaces)
        import re
        document_context = "\n\n".join([
            f"Section: {doc.metadata.get('section', 'Unknown')}\n{re.sub(r' +', ' ', doc.page_content)}"
            for doc in source_docs
        ])
        
        # If no documents found, return helpful message
        if not document_context.strip():
            return json.dumps({
                "error": "Documents retrieved but no content found",
                "message": "Please check the uploaded document format."
            }, indent=2)
        
        # Create chain
        try:
            chain = extraction_prompt | llm
            
            # Execute extraction with retrieved context
            response = chain.invoke({"document": document_context})
        except Exception as llm_error:
            return json.dumps({
                "error": "Error calling language model",
                "details": str(llm_error),
                "message": "Please check API key and model configuration."
            }, indent=2)
        
        # Extract JSON from response (handle markdown code blocks)
        content = response.content.strip() if hasattr(response, 'content') else str(response).strip()
        
        if not content:
            return json.dumps({
                "error": "Empty response from language model",
                "message": "Please try again."
            }, indent=2)
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]  # Remove ```json
        elif content.startswith("```"):
            content = content[3:]  # Remove ```
        
        if content.endswith("```"):
            content = content[:-3]  # Remove trailing ```
        
        content = content.strip()
        
        # Validate JSON
        try:
            parsed_data = json.loads(content)
            
            # Check for missing required fields before validation
            required_fields = [
                "company_name", "product_name", "report_period",
                "current_market_size_billions", "projected_market_size_2030_billions",
                "cagr_percent", "company_market_share_percent", "competitors", "swot"
            ]
            missing_fields = [field for field in required_fields if field not in parsed_data]
            
            if missing_fields:
                return json.dumps({
                    "error": "Missing required fields in extracted data",
                    "missing_fields": missing_fields,
                    "extracted_fields": list(parsed_data.keys()),
                    "partial_data": parsed_data,
                    "raw_response": content[:1000]
                }, indent=2)
            
            # Validate against Pydantic model
            validated_data = MarketResearchData(**parsed_data)
            
            # Return formatted JSON
            return validated_data.model_dump_json(indent=2)
        except json.JSONDecodeError as e:
            return json.dumps({
                "error": "Failed to parse JSON",
                "details": str(e),
                "raw_response": content[:1000]
            }, indent=2)
        except Exception as validation_error:
            # Provide more detailed validation error
            error_msg = str(validation_error)
            return json.dumps({
                "error": "Failed to validate extracted data",
                "details": error_msg,
                "parsed_data": parsed_data if 'parsed_data' in locals() else None,
                "raw_response": content[:1000]
            }, indent=2)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return json.dumps({
            "error": "Extraction failed",
            "details": str(e),
            "traceback": error_details[:500]
        }, indent=2)