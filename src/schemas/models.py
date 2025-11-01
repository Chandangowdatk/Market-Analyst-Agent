"""
Pydantic models for structured data extraction.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class CompetitorData(BaseModel):
    """Competitor information."""
    company_name: str = Field(description="Name of the competitor company")
    market_share: float = Field(description="Market share percentage")


class SWOTAnalysis(BaseModel):
    """SWOT Analysis structure."""
    strengths: List[str] = Field(description="List of company strengths")
    weaknesses: List[str] = Field(description="List of weaknesses")
    opportunities: List[str] = Field(description="List of opportunities")
    threats: List[str] = Field(description="List of threats")


class MarketResearchData(BaseModel):
    """Complete structured market research data."""
    company_name: str = Field(description="Name of the company")
    product_name: str = Field(description="Name of the flagship product")
    report_period: str = Field(description="Reporting period (e.g., Q3 2025)")
    current_market_size_billions: float = Field(
        description="Current market size in billions USD"
    )
    projected_market_size_2030_billions: float = Field(
        description="Projected market size by 2030 in billions USD"
    )
    cagr_percent: float = Field(
        description="Compound Annual Growth Rate as percentage"
    )
    company_market_share_percent: float = Field(
        description="Company's market share as percentage"
    )
    competitors: List[CompetitorData] = Field(
        description="List of main competitors with market shares"
    )
    swot: SWOTAnalysis = Field(description="SWOT analysis")


class QueryRequest(BaseModel):
    """API request model for queries."""
    query: str = Field(..., description="User query or question")
    session_id: Optional[str] = Field(None, description="Session ID for conversation memory")


class QueryResponse(BaseModel):
    """API response model."""
    answer: str = Field(..., description="Agent's response")
    tool_used: Optional[str] = Field(None, description="Tool that was used")
    session_id: str = Field(..., description="Session ID")
    execution_time_ms: Optional[int] = Field(None, description="Execution time in milliseconds")