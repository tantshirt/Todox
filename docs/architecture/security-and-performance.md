# Security and Performance

## Security Requirements

**Frontend Security:**
- **CSP Headers:** Configured in `next.config.js` to restrict script sources and prevent XSS
- **XSS Prevention:** React's automatic escaping + Zod validation on all inputs
- **Secure Storage:** JWT stored in `httpOnly` cookie or `localStorage` with clear documentation of trade-offs

**Backend Security:**
- **Input Validation:** Pydantic models validate all request bodies with type checking and constraints
- **Rate Limiting:** Use `slowapi` library to limit requests per IP (e.g., 100 requests/minute per IP)
- **CORS Policy:** Configured to only allow requests from Vercel frontend domain (`CORS_ORIGINS` env var)

**Authentication Security:**
- **Token Storage:** Frontend stores JWT securely (recommendation: httpOnly cookie for production)
- **Session Management:** JWT with expiry, no server-side session storage (stateless)
- **Password Policy:** Minimum 8 characters enforced on both frontend (Zod) and backend (Pydantic)

## Performance Optimization

**Frontend Performance:**
- **Bundle Size Target:** < 200KB initial JS bundle
- **Loading Strategy:** Code splitting by route (Next.js automatic), lazy load modals
- **Caching Strategy:** React Query caches API responses with 5-minute stale time, background refetch on window focus

**Backend Performance:**
- **Response Time Target:** < 500ms for API endpoints (95th percentile)
- **Database Optimization:** MongoDB indexes on `owner_id` fields, compound index on `owner_id + created_at` for tasks
- **Caching Strategy:** No backend caching initially; can add Redis for session caching if needed

---
