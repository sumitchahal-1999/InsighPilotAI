# InsightPilot AI — HTTP Security Headers Specification

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** HTTP Security Headers, Browser Policies & Transport Hardening  
**Status:** `IMPLEMENTED & VERIFIED`

---

## 1. Implemented Security Headers Master Matrix

| Header Name | Value | Purpose | Implementation Layer | Status |
| :--- | :--- | :--- | :---: | :---: |
| **`X-Content-Type-Options`** | `nosniff` | Prevents browsers from MIME-sniffing a response away from declared content-type. | FastAPI & Next.js | `VERIFIED IMPLEMENTED` |
| **`X-Frame-Options`** | `DENY` | Protects users against Clickjacking attacks by preventing iframe embedding. | FastAPI & Next.js | `VERIFIED IMPLEMENTED` |
| **`X-XSS-Protection`** | `1; mode=block` | Enables legacy browser XSS filters to block reflected script execution. | FastAPI & Next.js | `VERIFIED IMPLEMENTED` |
| **`Referrer-Policy`** | `strict-origin-when-cross-origin` | Protects privacy by stripping URL paths on cross-origin navigation. | FastAPI & Next.js | `VERIFIED IMPLEMENTED` |
| **`Permissions-Policy`** | `geolocation=(), camera=(), microphone=()` | Disables browser hardware access for camera, mic, and location. | FastAPI & Next.js | `VERIFIED IMPLEMENTED` |
| **`Strict-Transport-Security`** | `max-age=31536000; includeSubDomains; preload` | Forces HTTPS communication for 1 full year (in production/HTTPS mode). | FastAPI `APP_ENV=production` | `VERIFIED IMPLEMENTED` |
| **`Cache-Control`** | `no-store, no-cache, must-revalidate, max-age=0` | Prevents intermediate proxies from caching sensitive financial variance API data. | FastAPI (`/api/v1/*`) | `VERIFIED IMPLEMENTED` |

---

## 2. Implementation Mechanics

### Backend Implementation (`backend/app/security.py`):
```python
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        if settings.APP_ENV == "production" or request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        if request.url.path.startswith("/api/v1/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response
```

### Frontend Implementation (`frontend/next-app/next.config.mjs`):
Enforced at the Next.js edge router for all static page and asset requests.
