# Technical Assumptions

## Repository Structure

**Monorepo**
- Single repository containing both frontend and backend code
- Clear separation between `/frontend` and `/backend` directories
- Shared configuration files at root level
- Single CI/CD workflow for both tiers

## Service Architecture

**Monolith architecture for both tiers:**
- **Backend:** Single FastAPI application with modular structure (routes, services, repositories)
- **Frontend:** Single Next.js application using App Router
- No microservices complexity—all business logic runs in single deployable units
- RESTful API communication between frontend and backend
- Stateless backend with JWT-based authentication

## Testing Requirements

**Full Testing Pyramid:**
- **Unit Tests (Backend):** Pytest for services, repositories, and utility functions
- **Unit Tests (Frontend):** Vitest/Jest for utilities and helper functions (minimal, as needed)
- **E2E Tests:** Playwright covering critical user journeys (auth, task CRUD, labels)
- **API Contract Tests:** Verify request/response schemas match Pydantic models
- **CI Integration:** All tests must pass before merge to main branches

## Additional Technical Assumptions and Requests

- **Frontend:** Next.js 14+, TypeScript, Shadcn UI components, React Query or SWR for data fetching, Zod for client-side validation
- **Backend:** FastAPI, Pydantic models, Uvicorn server, Motor or Beanie for MongoDB async access, PyJWT or authlib for JWT handling
- **Database:** MongoDB Atlas with collections for users, tasks, and labels
- **Deployment:** Railway for backend (auto-deploy on tag), Vercel for frontend (auto-deploy on push to main with preview URLs on PRs)
- **Observability:** Optional Sentry DSN integration for error tracking on both tiers
- **Environment Management:** Environment variables configured via Railway and Vercel dashboards, with `.env.example` files in repository
- **MCPs for Development Workflow:**
  - Playwright MCP for E2E test execution and trace recording
  - MongoDB MCP for safe data seeding and schema validation
  - Shadcn MCP for UI component scaffolding
  - Railway MCP for backend deployment and log access
  - Context7 MCP for structured prompt generation and development workflows

---
