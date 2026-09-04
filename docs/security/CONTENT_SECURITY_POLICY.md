# InsightPilot AI — Content Security Policy (CSP) Architecture

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Content Security Policy (CSP) Directives, Edge Injection & Compatibility  
**Status:** `CSP ARCHITECTURE DEFINED & VERIFIED`

---

## 1. CSP Directive Specification

To prevent Cross-Site Scripting (XSS) and data injection while preserving Next.js App Router hydration, Tailwind CSS styles, and Lucide icons, the following baseline CSP policy is defined:

```text
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  img-src 'self' data: https: blob:;
  font-src 'self' data: https://fonts.gstatic.com;
  connect-src 'self' https://* http://127.0.0.1:* http://localhost:*;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-ancestors 'none';
```

---

## 2. Directive Rationale & Compatibility Analysis

| Directive | Configured Value | Rationale & Compatibility |
| :--- | :--- | :--- |
| **`default-src`** | `'self'` | Restricts all unspecified resource types to the application's origin. |
| **`script-src`** | `'self' 'unsafe-inline' 'unsafe-eval'` | Required for Next.js 14 client-side hydration chunks and React runtime evaluation. |
| **`style-src`** | `'self' 'unsafe-inline' https://fonts.googleapis.com` | Permits Tailwind CSS inline classes and Google Fonts stylesheets. |
| **`img-src`** | `'self' data: https: blob:` | Allows SVG chart rendering, data URIs, and avatar icons. |
| **`connect-src`** | `'self' https://* http://127.0.0.1:* http://localhost:*` | Permits AJAX queries to the FastAPI backend locally and across HTTPS production domains. |
| **`object-src`** | `'none'` | Completely blocks Flash, Java applets, and legacy plugin exploits. |
| **`frame-ancestors`**| `'none'` | Enforces strict clickjacking defense across modern browsers. |

---

## 3. Production Deployment Recommendation

In production cloud environments (e.g. Vercel / Cloudflare), CSP headers can be injected at the edge proxy layer without modifying application binaries.
