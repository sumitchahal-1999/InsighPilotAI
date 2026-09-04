"""
InsightPilot AI — Production Structured Logging & Request Correlation Middleware
Provides request tracing, latency calculation, and structured logging without credential leakage.
"""

import time
import uuid
import logging
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("insightpilot.telemetry")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "service": "insightpilot-api", %(message)s}'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class RequestCorrelationMiddleware(BaseHTTPMiddleware):
    """
    Middleware that attaches a unique X-Request-ID to every incoming HTTP request,
    measures request latency in milliseconds, and emits a structured telemetry log.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 1. Resolve or generate correlation request ID
        incoming_id = request.headers.get("X-Request-ID") or request.headers.get("X-Correlation-ID")
        request_id = incoming_id if incoming_id else f"req_{uuid.uuid4().hex[:12]}"
        
        request.state.request_id = request_id
        start_time = time.perf_counter()

        # 2. Process request through downstream pipeline
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as exc:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            log_payload = {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": 500,
                "latency_ms": latency_ms,
                "error_category": "INTERNAL_SERVER_ERROR",
                "error_message": "Unhandled exception during request processing"
            }
            logger.error(json.dumps(log_payload).strip("{}"))
            raise exc

        # 3. Calculate latency and attach correlation headers
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-Ms"] = str(latency_ms)

        # 4. Emit structured JSON telemetry log (filtering any sensitive path/query tokens)
        log_payload = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "latency_ms": latency_ms,
            "client_ip": request.client.host if request.client else "unknown"
        }
        
        # Log at INFO or WARNING based on HTTP status
        if status_code >= 400:
            logger.warning(json.dumps(log_payload).strip("{}"))
        else:
            logger.info(json.dumps(log_payload).strip("{}"))

        return response
