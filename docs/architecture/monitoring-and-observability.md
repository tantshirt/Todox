# Monitoring and Observability

## Monitoring Stack

- **Frontend Monitoring:** Vercel Analytics (automatic) + optional Sentry for error tracking
- **Backend Monitoring:** Railway metrics (CPU, memory, requests) + optional Sentry for error tracking
- **Error Tracking:** Sentry (optional) - captures frontend and backend errors with stack traces
- **Performance Monitoring:** Vercel Web Vitals for frontend, Railway response time metrics for backend

## Key Metrics

**Frontend Metrics:**
- Core Web Vitals (LCP, FID, CLS) tracked by Vercel
- JavaScript errors (Sentry if configured)
- API response times from client perspective
- User interactions and page views

**Backend Metrics:**
- Request rate (requests per second)
- Error rate (5xx responses)
- Response time (p50, p95, p99)
- Database query performance (via MongoDB Atlas monitoring)
- Memory usage and CPU utilization (Railway dashboard)

---
