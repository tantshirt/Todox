# Tech Stack

## Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|-----------|---------|---------|-----------|
| Frontend Language | TypeScript | 5.x | Type-safe JavaScript for frontend | Catches errors at compile time, improves IDE support, required by Next.js and Shadcn UI |
| Frontend Framework | Next.js | 14+ | React framework with App Router | Server-side rendering, file-based routing, optimal Vercel deployment, built-in optimization |
| UI Component Library | Shadcn UI | Latest | Accessible, unstyled component primitives | Radix UI-based accessibility, Tailwind styling, no runtime overhead, easy customization |
| State Management | React Query (TanStack Query) | 5.x | Server state management and caching | Handles API calls, caching, loading/error states, reduces boilerplate, optimistic updates |
| Backend Language | Python | 3.11+ | Backend application language | Strong typing with mypy, extensive libraries, FastAPI native support, developer familiarity |
| Backend Framework | FastAPI | 0.104+ | High-performance async web framework | Auto-generated OpenAPI docs, Pydantic integration, async/await support, fast execution |
| API Style | REST | OpenAPI 3.0 | RESTful HTTP API | Standard approach, clear semantics, FastAPI native support, easy to document and test |
| Database | MongoDB Atlas | 7.0+ | NoSQL document database | Flexible schema for MVP iteration, M0 free tier, managed service, easy Railway integration |
| Cache | None (MVP) | - | No caching initially | Can add Redis later if needed; premature for MVP scale |
| File Storage | None (MVP) | - | No file uploads in MVP | Future: Could use Vercel Blob or Railway volumes if needed |
| Authentication | JWT + bcrypt | PyJWT 2.x, bcrypt 4.x | Token-based auth and password hashing | Stateless authentication, secure password storage, industry standard |
| Frontend Testing | Vitest | 1.x | Unit tests for utilities | Fast Vite-based testing, TypeScript support, minimal setup |
| Backend Testing | Pytest | 7.x | Backend unit and integration tests | Standard Python testing, async support, extensive plugins, fixtures |
| E2E Testing | Playwright | 1.40+ | End-to-end UI testing | Cross-browser testing, auto-wait, trace recording, MCP integration available |
| Build Tool | npm/pip | npm 10+, pip 23+ | Package management | Standard tools for respective ecosystems |
| Bundler | Next.js built-in | Turbopack | Frontend bundling and optimization | Included with Next.js 14+, no additional configuration |
| IaC Tool | None (MVP) | - | No infrastructure as code | Railway and Vercel use dashboard/git-based deploys |
| CI/CD | GitHub Actions | N/A | Automated testing and deployment | Free for public repos, integrated with GitHub, simple YAML config |
| Monitoring | Sentry (Optional) | Latest | Error tracking and performance | Optional DSN integration, captures frontend and backend errors |
| Logging | Railway Logs + Vercel Logs | Platform native | Application logging | Built into deployment platforms, no additional setup |
| CSS Framework | Tailwind CSS | 3.x | Utility-first styling | Fast development, small bundle size, Shadcn UI native support |


---
