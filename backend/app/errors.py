"""
InsightPilot AI — API Error Handling & Structured Exceptions
Provides standardized error responses without leaking internal stack traces or paths.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class APIError(Exception):
    """Base API domain exception."""
    def __init__(self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class KPINotFoundError(APIError):
    """Raised when a requested KPI is not defined or supported."""
    def __init__(self, kpi_id: str):
        super().__init__(
            code="KPI_NOT_FOUND",
            message=f"KPI with identifier '{kpi_id}' is not recognized or supported by the analytics engine.",
            status_code=status.HTTP_404_NOT_FOUND
        )

class EvidenceNotFoundError(APIError):
    """Raised when a requested evidence node ID cannot be found."""
    def __init__(self, evidence_id: str):
        super().__init__(
            code="EVIDENCE_NOT_FOUND",
            message=f"Evidence record with identifier '{evidence_id}' was not found in the verified repository.",
            status_code=status.HTTP_404_NOT_FOUND
        )

class InvalidInvestigationRequestError(APIError):
    """Raised when investigation parameters are invalid or out of bounds."""
    def __init__(self, message: str):
        super().__init__(
            code="INVALID_INVESTIGATION_REQUEST",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class InvalidPersonaAPIError(APIError):
    """Raised when an unsupported persona is requested."""
    def __init__(self, persona: str):
        super().__init__(
            code="INVALID_PERSONA",
            message=f"Unsupported persona '{persona}'. Supported personas: 'CFO', 'REGIONAL_SALES_MANAGER'.",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class AIServiceUnavailableAPIError(APIError):
    """Raised when Gemini API is unconfigured or unreachable."""
    def __init__(self, detail: str = "AI Reasoning Service is currently unavailable."):
        super().__init__(
            code="AI_SERVICE_UNAVAILABLE",
            message=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

class AIGroundingAPIError(APIError):
    """Raised when generated AI narrative fails post-generation grounding checks."""
    def __init__(self, detail: str = "AI reasoning output failed grounding validation."):
        super().__init__(
            code="AI_GROUNDING_FAILED",
            message=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

def register_error_handlers(app: FastAPI) -> None:
    """Registers unified JSON exception handlers on the FastAPI application."""
    
    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message
                }
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        code_map = {
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
            500: "INTERNAL_SERVER_ERROR",
            503: "SERVICE_UNAVAILABLE"
        }
        code = code_map.get(exc.status_code, "HTTP_ERROR")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": code,
                    "message": str(exc.detail) if exc.detail else "An HTTP error occurred."
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "The incoming request failed validation constraints."
                }
            }
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected internal server error occurred while processing the request."
                }
            }
        )
