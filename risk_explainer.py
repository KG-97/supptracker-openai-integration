"""
SuppTracker OpenAI Integration - Risk Explanation Module

Minimal production-ready FastAPI endpoint for structured risk explanations.
Uses OpenAI Structured Outputs to guarantee type-safe JSON responses.

Usage:
  POST /api/insights/explain-risk
  Body: {"stack": [...], "risk_scores": {...}}

Cost: ~$0.0007 per call using gpt-4.1-mini
"""

from openai import OpenAI
from pydantic import BaseModel
from typing import List, Dict, Literal
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class RiskExplanation(BaseModel):
    """Structured risk explanation schema - guaranteed by OpenAI Structured Outputs"""
    risk_level: Literal["low", "moderate", "high", "critical"]
    user_friendly_summary: str
    warnings: List[str]
    next_steps: List[str]
    affected_compounds: List[str]
    confidence_score: float  # 0.0 to 1.0


def explain_risk(stack: List[Dict], risk_scores: Dict) -> RiskExplanation:
    """
    Generate structured risk explanation from SuppTracker data.
    
    Args:
        stack: List of supplements with their properties
        risk_scores: Dict of interaction/risk scores from your backend
    
    Returns:
        RiskExplanation: Structured explanation matching your schema
    """
    
    # Build context prompt from your backend data
    context = f"""
User's Current Stack:
{format_stack(stack)}

Risk Assessment Scores:
{format_scores(risk_scores)}

Provide a clear, actionable risk explanation for this supplement combination.
"""
    
    response = client.chat.completions.parse(
        model="gpt-4.1-mini",  # $0.40 input / $1.60 output per 1M tokens
        messages=[
            {
                "role": "system",
                "content": "You are a supplement safety expert. Analyze the user's stack and provide clear risk explanations based on the provided scores. Be direct and actionable."
            },
            {
                "role": "user",
                "content": context
            }
        ],
        response_format=RiskExplanation  # Structured Outputs ensures this schema
    )
    
    return response.choices[0].message.parsed


def format_stack(stack: List[Dict]) -> str:
    """Format stack for LLM consumption"""
    return "\n".join([
        f"- {s['name']}: {s.get('dosage', 'N/A')} ({s.get('timing', 'unspecified')})"
        for s in stack
    ])


def format_scores(scores: Dict) -> str:
    """Format risk scores for LLM consumption"""
    return "\n".join([
        f"{key}: {value}"
        for key, value in scores.items()
    ])


# FastAPI endpoint example
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/api/insights/explain-risk", response_model=RiskExplanation)
async def api_explain_risk(stack: List[Dict], risk_scores: Dict):
    """
    Generate AI-powered risk explanation for user's supplement stack.
    
    Example request:
    ```json
    {
      "stack": [
        {"name": "Magnesium Glycinate", "dosage": "400mg", "timing": "evening"},
        {"name": "Vitamin D3", "dosage": "5000 IU", "timing": "morning"}
      ],
      "risk_scores": {
        "interaction_severity": 0.2,
        "cumulative_load": 0.4,
        "timing_conflicts": 0.0
      }
    }
    ```
    """
    try:
        explanation = explain_risk(stack, risk_scores)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")


if __name__ == "__main__":
    # Test with dummy data
    test_stack = [
        {"name": "Magnesium Glycinate", "dosage": "400mg", "timing": "evening"},
        {"name": "Zinc Picolinate", "dosage": "30mg", "timing": "evening"},
        {"name": "Calcium", "dosage": "1000mg", "timing": "evening"}
    ]
    
    test_scores = {
        "interaction_severity": 0.7,  # High - Zinc/Calcium/Magnesium compete
        "cumulative_load": 0.5,
        "timing_conflicts": 0.8
    }
    
    result = explain_risk(test_stack, test_scores)
    print(f"\nRisk Level: {result.risk_level}")
    print(f"\nSummary: {result.user_friendly_summary}")
    print(f"\nWarnings: {', '.join(result.warnings)}")
    print(f"\nNext Steps: {', '.join(result.next_steps)}")
