"""
InsightPilot AI — Production Security Headers & Defense Middleware
Enforces HTTP security headers, payload boundaries, and protective transport policies.
"""

from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.app.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces OWASP-recommended HTTP security headers
    across all API responses while maintaining Next.js and documentation compatibility.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # 1. Prevent MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # 2. Prevent clickjacking (frame hijacking)
        response.headers["X-Frame-Options"] = "DENY"

        # 3. Cross-Site Scripting (XSS) filter protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # 4. Strict Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 5. Restrict sensitive browser permissions/features
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"

        # 6. HTTP Strict Transport Security (HSTS) in production
        if settings.APP_ENV == "production" or request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

        # 7. Sensitive dynamic API data cache prevention
        if request.url.path.startswith("/api/v1/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"

        return response
