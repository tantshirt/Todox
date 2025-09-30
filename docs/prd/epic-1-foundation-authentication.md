# Epic 1: Foundation & Authentication

**Epic Goal:** Establish the foundational project structure with working CI/CD, database connectivity, and a complete authentication system that allows users to register, log in, and access protected routes. This epic delivers immediate value by providing a deployable application with working user management and sets the stage for all subsequent feature development.

## Story 1.1: Project Setup & Repository Scaffolding

As a developer,
I want the project repository initialized with proper structure and tooling,
so that we have a solid foundation for development with CI/CD, linting, and type checking in place.

**Acceptance Criteria:**

1. Repository is initialized with monorepo structure containing `/frontend` and `/backend` directories
2. Backend scaffolded with FastAPI, pyproject.toml/requirements.txt, and basic app structure (routes, services, models, db directories)
3. Frontend scaffolded with Next.js 14+ using App Router, TypeScript, and Shadcn UI configured
4. Root-level `.gitignore` excludes environment files, node_modules, Python cache, and IDE files
5. `.env.example` files present in both frontend and backend with required variable templates
6. GitHub Actions CI workflow configured to run linting and type checks on both tiers
7. README.md created with project description, tech stack, and setup instructions
8. Repository is public and accessible

## Story 1.2: Database Connection & User Model

As a developer,
I want MongoDB Atlas connection established with a User model,
so that we can persist user data securely and query it efficiently.

**Acceptance Criteria:**

1. MongoDB Atlas cluster is provisioned and connection string available
2. Backend has database client module (`db/client.py`) with connection pooling configured
3. User Pydantic model defined with fields: id, email, hashed_password, created_at, updated_at
4. User repository class (`db/repositories/users_repo.py`) implements methods: create_user, find_by_email, find_by_id
5. Database connection health check endpoint (`GET /health`) returns 200 with database status
6. Unit tests verify User model validation and repository methods using test database
7. Environment variable `MONGODB_URI` properly loads from `.env`

## Story 1.3: User Registration API

As a new user,
I want to register with email and password,
so that I can create an account and access the application.

**Acceptance Criteria:**

1. API endpoint `POST /auth/register` accepts JSON body with email and password
2. Password must be at least 8 characters and validated with Pydantic
3. Email must be valid format and unique (return 409 Conflict if already exists)
4. Password is hashed using bcrypt before storing in database
5. Successful registration returns 201 status with JSON response containing user id and email (no password)
6. Registration fails with clear error messages for: invalid email format, weak password, duplicate email
7. Unit tests cover: successful registration, duplicate email rejection, validation errors
8. Endpoint is documented and accessible

## Story 1.4: User Login API & JWT Generation

As an existing user,
I want to log in with my credentials,
so that I can access my protected tasks and data.

**Acceptance Criteria:**

1. API endpoint `POST /auth/login` accepts JSON body with email and password
2. System verifies email exists and password hash matches stored hash
3. Successful login returns 200 status with JSON containing `access_token` (JWT) and `expires_in` (seconds)
4. JWT is signed with secret from environment variable `JWT_SECRET` and includes user_id and expiry
5. Login fails with 401 Unauthorized for: non-existent email, incorrect password
6. JWT expiry time is configurable via `JWT_EXPIRES_IN` environment variable (default: 3600 seconds)
7. Unit tests cover: successful login, invalid credentials rejection, JWT token structure validation
8. Auth service module (`services/auth_service.py`) implements password verification and token generation logic

## Story 1.5: JWT Authentication Middleware & Protected Routes

As the system,
I want to verify JWT tokens on protected routes,
so that only authenticated users can access their data.

**Acceptance Criteria:**

1. FastAPI dependency (`core/deps.py`) implements JWT verification that extracts and validates tokens from Authorization header
2. Dependency decodes JWT, verifies signature, checks expiry, and returns user_id
3. Invalid, expired, or missing tokens return 401 Unauthorized with clear error message
4. Test endpoint `GET /auth/me` requires authentication and returns current user's email and id
5. CORS middleware configured to allow requests from frontend origin (via `CORS_ORIGINS` environment variable)
6. Unit tests cover: valid token acceptance, expired token rejection, invalid signature rejection, missing token rejection
7. Integration test verifies: register → login → access protected route flow

## Story 1.6: Frontend Login & Registration Pages

As a user,
I want accessible login and registration pages,
so that I can authenticate and access the application through the UI.

**Acceptance Criteria:**

1. Login page created at `/auth/login` with form containing email and password fields
2. Registration page created at `/auth/register` with form containing email and password fields
3. Forms use Shadcn UI components with proper accessibility (labels, focus states, ARIA attributes)
4. Client-side validation using Zod ensures: valid email format, password minimum length before submission
5. Form submissions call respective backend API endpoints (`POST /auth/register`, `POST /auth/login`)
6. Successful login stores JWT token securely (httpOnly cookie or secure localStorage with documented rationale)
7. Successful registration redirects to login page with success message
8. Successful login redirects to dashboard/task list page
9. API errors display as toast notifications or inline error messages with clear, actionable text
10. Loading states show during API calls (disabled buttons, spinners)
11. Basic styling applied using Tailwind CSS and Shadcn components for professional appearance

## Story 1.7: Frontend Authentication State & Protected Routes

As a user,
I want my authentication state persisted and enforced,
so that I remain logged in across page refreshes and cannot access protected pages without authentication.

**Acceptance Criteria:**

1. Authentication context/hook (`lib/auth.ts`) manages: token storage, current user state, login/logout functions
2. Token is retrieved from storage on app initialization and validated
3. Protected routes (dashboard, tasks, labels) redirect to login if no valid token present
4. User can log out via logout button which clears token and redirects to login page
5. API client (`lib/api.ts`) automatically includes JWT token in Authorization header for all requests
6. Expired token triggers logout and redirect to login page
7. `/` root route redirects authenticated users to dashboard, non-authenticated to login

## Story 1.8: Deployment to Railway & Vercel

As a developer,
I want the application deployed to production environments,
so that the live application is accessible and users can test it.

**Acceptance Criteria:**

1. Backend deployed to Railway with environment variables configured: `MONGODB_URI`, `JWT_SECRET`, `JWT_EXPIRES_IN`, `CORS_ORIGINS`
2. Railway service exposes backend URL (e.g., `https://todox-backend.up.railway.app`)
3. Frontend deployed to Vercel with environment variable `NEXT_PUBLIC_API_URL` pointing to Railway backend URL
4. Vercel deployment accessible at public URL (e.g., `https://todox.vercel.app`)
5. Health check endpoint (`GET /health`) returns 200 on Railway deployment
6. Frontend login page loads successfully on Vercel
7. End-to-end flow verified: register on production → login on production → access dashboard
8. Deployment documented in README with links to live URLs

---
