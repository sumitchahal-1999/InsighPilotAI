"""
InsightPilot AI — FastAPI Application Entry Point
Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.errors import register_error_handlers
from backend.app.routes.health import router as health_router
from backend.app.routes.kpis import router as kpis_router
from backend.app.routes.investigations import router as investigations_router
from backend.app.routes.evidence import router as evidence_router
from backend.app.routes.ai import router as ai_router
from backend.app.routes.recommendations import router as recommendations_router
from backend.app.routes.simulations import router as simulations_router
from backend.app.routes.demo import router as demo_router

def create_app() -> FastAPI:
    """Factory creating and configuring the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "REST API exposing the deterministic KPI calculations, multi-factor driver analyses, "
            "cryptographic evidence lineage graphs, action recommendations, what-if simulations, "
            "and grounded Gemini reasoning of InsightPilot AI."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # Configure CORS Middleware
    cors_origins = settings.CORS_ORIGINS
    allow_credentials = "*" not in cors_origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configure Security Headers Middleware
    from backend.app.security import SecurityHeadersMiddleware
    app.add_middleware(SecurityHeadersMiddleware)

    # Configure Request Correlation & Telemetry Logging Middleware
    from backend.app.logging import RequestCorrelationMiddleware
    app.add_middleware(RequestCorrelationMiddleware)


    # Register Error Handlers

    register_error_handlers(app)

    # Register Routes
    app.include_router(health_router)
    app.include_router(kpis_router, prefix=settings.API_PREFIX)
    app.include_router(investigations_router, prefix=settings.API_PREFIX)
    app.include_router(evidence_router, prefix=settings.API_PREFIX)
    app.include_router(ai_router, prefix=settings.API_PREFIX)
    app.include_router(recommendations_router, prefix=settings.API_PREFIX)
    app.include_router(simulations_router, prefix=settings.API_PREFIX)
    app.include_router(demo_router, prefix=settings.API_PREFIX)

    return app

app = create_app()
