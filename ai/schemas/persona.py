"""
InsightPilot AI — Persona Schemas & Guidance
Defines executive user personas and their analytical emphasis.
"""

from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel, Field

class PersonaType(str, Enum):
    CFO = "CFO"
    REGIONAL_SALES_MANAGER = "REGIONAL_SALES_MANAGER"

class PersonaProfile(BaseModel):
    persona: PersonaType = Field(..., description="Target executive persona")
    role_title: str = Field(..., description="Full executive title")
    focus_areas: list[str] = Field(..., description="Primary analytical focal areas")
    tone: str = Field(..., description="Desired communication style")

PERSONA_PROFILES: Dict[str, PersonaProfile] = {
    "CFO": PersonaProfile(
        persona=PersonaType.CFO,
        role_title="Chief Financial Officer",
        focus_areas=[
            "Revenue and gross margin variance",
            "Financial exposure and EBITDA risk",
            "Enterprise-level resource allocation",
            "Executive risk and governance"
        ],
        tone="Strategic, financially rigorous, high-level, and decision-oriented"
    ),
    "REGIONAL_SALES_MANAGER": PersonaProfile(
        persona=PersonaType.REGIONAL_SALES_MANAGER,
        role_title="Regional Sales & Operations Manager",
        focus_areas=[
            "Distribution center fulfillment and stockouts",
            "Distributor purchase order deferrals",
            "SKU delivery backorders and customer sentiment",
            "Competitor pricing pressure in regional accounts"
        ],
        tone="Tactical, operational, account-centric, and execution-focused"
    )
}

def resolve_persona(persona_input: str) -> PersonaProfile:
    """Normalizes and validates persona string against supported profiles."""
    norm = persona_input.strip().upper().replace(" ", "_").replace("-", "_")
    if norm in ("CFO", "CHIEF_FINANCIAL_OFFICER"):
        return PERSONA_PROFILES["CFO"]
    elif norm in ("REGIONAL_SALES_MANAGER", "SALES_MANAGER", "RSM"):
        return PERSONA_PROFILES["REGIONAL_SALES_MANAGER"]
    else:
        raise ValueError(f"Unsupported persona '{persona_input}'. Supported: 'CFO', 'REGIONAL_SALES_MANAGER'.")
