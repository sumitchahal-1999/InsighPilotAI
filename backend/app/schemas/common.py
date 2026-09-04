"""
InsightPilot AI — Common API Schemas
Standardized health check and error payload models.
"""

from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = Field(..., example="ok", description="Service operating status")
    service: str = Field(..., example="insightpilot-api", description="Service name")
    version: str = Field(..., example="2.0.0", description="API version")

class ErrorDetail(BaseModel):
    code: str = Field(..., example="KPI_NOT_FOUND", description="Machine-readable error code")
    message: str = Field(..., example="Requested KPI was not found.", description="Human-readable error description")

class ErrorResponse(BaseModel):
    error: ErrorDetail
