"""
Agent configuration using modern LangChain 1.0 API.

MODERN VERSION - Uses create_agent built on LangGraph
Migrated from deprecated create_react_agent to modern create_agent
"""
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from config import Config
from tools.qa_tool import qa_tool
from tools.insights_tool import insights_tool
from tools.extract_tool import extract_tool


def create_market_analyst_agent():
    """
    Create the AI Market Analyst agent with autonomous routing.
    
    Uses modern LangChain 1.0 patterns:
    - create_agent (built on LangGraph)
    - Simple system_prompt (no template placeholders needed)
    - Stateless by default (add middleware for memory if needed)
    
    Returns:
        Configured agent (runnable graph)
    """
    
    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model=Config.GEMINI_MODEL,
        google_api_key=Config.GOOGLE_API_KEY,
        temperature=0.1,
        convert_system_message_to_human=True  # Required for Gemini compatibility
    )
    
    # Define tools
    tools = [qa_tool, insights_tool, extract_tool]
    
    # Simple system prompt (no placeholders like {tools} or {tool_names} needed!)
    system_prompt = """You are an AI Market Analyst assistant that helps users analyze uploaded documents.

Your capabilities:
1. **Q&A Tool**: Answer specific factual questions using document retrieval
2. **Insights Tool**: Generate strategic summaries and market analysis
3. **Extract Tool**: Export structured data in JSON format

Instructions for tool selection:
- Use **qa_tool** for:
  * Simple factual questions (What/Who/When/Which/How many)
  * Quick lookups (product names, competitors, metrics, SWOT items)
  * Direct information retrieval (e.g., "what is X", "who are the competitors", "what are the SWOTs")
  
- Use **insights_tool** for:
  * Deep strategic analysis and recommendations
  * Multi-faceted summaries requiring interpretation
  * Requests explicitly asking for "analysis", "strategy", "recommendations"
  * Comprehensive overviews (e.g., "analyze the market position", "provide strategic recommendations")
  
- Use **extract_tool** when user asks for:
  * JSON format output
  * Structured data export
  * Complete data extraction in schema format

Always:
- Select the most appropriate tool based on the query intent
- Default to qa_tool for simple, direct questions
- Use insights_tool only when deep analysis is explicitly requested
- Provide clear, concise responses
- Be helpful and professional"""

    # Create agent with modern API - much simpler!
    # No AgentExecutor wrapper needed, no prompt template needed
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    
    return agent


# Initialize agent (singleton pattern)
agent = create_market_analyst_agent()

