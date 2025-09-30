# Coding Standards

## Critical Fullstack Rules

- **Type Sharing:** Define shared types in TypeScript interfaces (frontend) and Pydantic models (backend) with consistent naming and structure
- **API Calls:** Always use the centralized `apiClient` (frontend) - never use `fetch()` directly outside of `lib/api.ts`
- **Environment Variables:** Access only through config objects (`process.env` frontend, `settings` backend) - never inline `process.env` or `os.getenv()`
- **Error Handling:** All API routes must use FastAPI's HTTPException with appropriate status codes and clear `detail` messages
- **Authentication:** Always use `get_current_user` dependency for protected routes - never manually parse JWT in route handlers
- **Database Operations:** All database access must go through repository classes - never call MongoDB client directly in services or routes
- **Validation:** Use Pydantic (backend) and Zod (frontend) for all data validation - never trust client input or skip validation
- **State Updates:** Never mutate React state directly - use proper state setters and React Query mutations
- **Password Handling:** Never log, display, or return passwords - always hash with bcrypt before storage

## Naming Conventions

| Element | Frontend | Backend | Example |
|---------|----------|---------|---------|
| Components | PascalCase | - | `TaskCard.tsx` |
| Hooks | camelCase with 'use' | - | `useAuth.ts` |
| API Routes | - | kebab-case | `/api/user-profile` |
| Database Tables | - | snake_case | `user_profiles` |
| TypeScript Interfaces | PascalCase | - | `interface User` |
| Python Classes | PascalCase | PascalCase | `class UserRepository` |
| Functions | camelCase | snake_case | `getUserTasks` / `get_user_tasks` |
| Constants | UPPER_SNAKE_CASE | UPPER_SNAKE_CASE | `API_BASE_URL` / `JWT_ALGORITHM` |

---
