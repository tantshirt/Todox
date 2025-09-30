# Todox Fullstack Architecture Document

## Introduction

This document outlines the complete fullstack architecture for Todox, including backend systems, frontend implementation, and their integration. It serves as the single source of truth for AI-driven development, ensuring consistency across the entire technology stack.

This unified approach combines what would traditionally be separate backend and frontend architecture documents, streamlining the development process for modern fullstack applications where these concerns are increasingly intertwined.

### Starter Template or Existing Project

**N/A - Greenfield project**

This is a new project built from scratch following the PRD requirements. No starter templates are being used. The architecture is custom-designed to meet the specific needs of the Todox task management application.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-01-12 | 1.0 | Initial architecture document | Winston (Architect) |

---

## High Level Architecture

### Technical Summary

Todox is a fullstack task management application built with a monolith architecture on both frontend and backend tiers. The frontend is a Next.js 14+ application using App Router with TypeScript and Shadcn UI components, providing a responsive, accessible user interface. The backend is a FastAPI Python application with modular organization (routes, services, repositories), communicating with a MongoDB Atlas database for data persistence. The two tiers communicate via a RESTful API with JWT-based authentication ensuring stateless, secure session management. The application deploys to Railway for backend hosting and Vercel for frontend hosting, both with automatic CI/CD pipelines. This architecture prioritizes simplicity, maintainability, and rapid MVP delivery while maintaining clean separation of concerns and testability through comprehensive Playwright E2E tests and unit tests on both tiers.

### Platform and Infrastructure Choice

**Platform:** Railway (Backend) + Vercel (Frontend) + MongoDB Atlas (Database)

**Key Services:**
- **Railway:** Backend API hosting with automatic deployments on tag pushes, environment variable management, log streaming
- **Vercel:** Frontend hosting with edge network CDN, automatic deployments on main branch, preview URLs for pull requests
- **MongoDB Atlas:** Managed MongoDB database with M0 free tier, connection pooling, automated backups
- **GitHub Actions:** CI/CD for linting, type checking, and automated testing before deployment

**Deployment Host and Regions:**
- Railway: Auto-selected region (typically US-based for free tier)
- Vercel: Global edge network with automatic CDN distribution
- MongoDB Atlas: Shared M0 cluster (region: nearest to Railway deployment)

**Rationale:** This stack provides zero-cost MVP deployment with minimal configuration while maintaining production-ready capabilities. Railway and Vercel both offer generous free tiers suitable for demonstration and initial user load. MongoDB Atlas M0 tier provides 512MB storage sufficient for MVP. The combination supports the October 2025 deadline with rapid deployment workflows and minimal infrastructure management overhead.

### Repository Structure

**Structure:** Monorepo with frontend and backend in separate directories

**Monorepo Tool:** Simple directory-based monorepo (no specialized tooling like Nx or Turborepo)

**Package Organization:**
- `/frontend` - Next.js application with all frontend code
- `/backend` - FastAPI application with all backend code
- Root-level shared configs (`.github/workflows`, `.gitignore`, `README.md`)
- Separate `package.json` (frontend) and `pyproject.toml`/`requirements.txt` (backend)
- No shared packages initially (can add if needed for type sharing in future iterations)

**Rationale:** Simple monorepo structure avoids complexity of workspace tools while keeping all code in a single repository. This supports atomic commits affecting both tiers, unified version control, and simplified CI/CD. For MVP scope with 2 distinct deployment targets, a basic directory structure is sufficient and reduces cognitive overhead for AI agents.

### High Level Architecture Diagram

```mermaid
graph TB
    User[User Browser] -->|HTTPS| Vercel[Vercel Frontend<br/>Next.js App]
    Vercel -->|API Calls<br/>HTTPS + JWT| Railway[Railway Backend<br/>FastAPI Server]
    Railway -->|MongoDB Protocol| MongoDB[(MongoDB Atlas<br/>Database)]
    
    Railway -.->|Error Tracking| Sentry[Sentry<br/>Optional]
    Vercel -.->|Error Tracking| Sentry
    
    GitHub[GitHub Repository] -->|Push/PR| GHA[GitHub Actions<br/>CI/CD]
    GHA -->|Deploy on tag| Railway
    GHA -->|Deploy on push| Vercel
    
    Dev[Developer] -->|Push Code| GitHub
    Dev -.->|Local Dev| LocalFE[Local Frontend<br/>:3000]
    Dev -.->|Local Dev| LocalBE[Local Backend<br/>:8000]
    LocalFE -->|API Calls| LocalBE
    LocalBE -->|MongoDB Protocol| MongoDB
    
    style Vercel fill:#000,stroke:#fff,color:#fff
    style Railway fill:#9333ea,stroke:#fff,color:#fff
    style MongoDB fill:#13aa52,stroke:#fff,color:#fff
    style GHA fill:#2088FF,stroke:#fff,color:#fff
```

### Architectural Patterns

- **Monolith Architecture:** Single deployable unit for both frontend and backend - _Rationale:_ MVP scope benefits from simplicity; avoids microservices complexity while maintaining clear separation via repository structure
- **JAMstack Principles:** JavaScript app (Next.js) + API (FastAPI) + Markup (SSR/SSG) - _Rationale:_ Leverages Vercel's edge network for fast static delivery while dynamic data comes from Railway API
- **Repository Pattern:** Abstract database operations behind repository interfaces - _Rationale:_ Separates data access from business logic, enabling easier testing and potential future database migrations
- **Service Layer:** Business logic in service classes, routes as thin controllers - _Rationale:_ Maintains testability, keeps routes focused on HTTP concerns, enables logic reuse
- **Component-Based UI:** React components with TypeScript and Shadcn UI primitives - _Rationale:_ Reusability, maintainability, type safety, and accessibility built into component library
- **JWT Stateless Authentication:** Token-based auth stored client-side, verified per request - _Rationale:_ Scales horizontally without session storage, suitable for separate frontend/backend deployments
- **API Gateway Pattern:** Single FastAPI app serving all API routes with CORS config - _Rationale:_ Centralized auth middleware, rate limiting potential, consistent error handling

---

## Tech Stack

### Technology Stack Table

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

## Data Models

### User

**Purpose:** Represents an authenticated user account with credentials and metadata

**Key Attributes:**
- `id`: ObjectId - Unique MongoDB identifier (auto-generated)
- `email`: string - User's email address (unique, required)
- `hashed_password`: string - bcrypt hashed password (required, never exposed in responses)
- `created_at`: datetime - Account creation timestamp
- `updated_at`: datetime - Last modification timestamp

#### TypeScript Interface

```typescript
// Shared type for frontend use (password fields excluded)
export interface User {
  id: string;
  email: string;
  created_at: string; // ISO 8601 format
  updated_at: string; // ISO 8601 format
}

// Frontend-only types for auth
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: 'bearer';
  expires_in: number; // seconds
}
```

#### Relationships
- One-to-many with Task (one user owns many tasks)
- One-to-many with Label (one user owns many labels)

---

### Task

**Purpose:** Represents a single task/todo item with priority, deadline, and optional description

**Key Attributes:**
- `id`: ObjectId - Unique MongoDB identifier
- `title`: string - Task title (required, max 200 chars)
- `description`: string | null - Optional longer description
- `priority`: enum('High', 'Medium', 'Low') - Task priority (required)
- `deadline`: date - Due date (required, ISO 8601 date string)
- `status`: enum('open', 'done') - Completion status (default: 'open')
- `label_ids`: array of ObjectId - References to assigned labels
- `owner_id`: ObjectId - Reference to User who owns this task (required)
- `created_at`: datetime - Creation timestamp
- `updated_at`: datetime - Last modification timestamp

#### TypeScript Interface

```typescript
export type TaskPriority = 'High' | 'Medium' | 'Low';
export type TaskStatus = 'open' | 'done';

export interface Task {
  id: string;
  title: string;
  description: string | null;
  priority: TaskPriority;
  deadline: string; // ISO 8601 date string
  status: TaskStatus;
  label_ids: string[];
  owner_id: string;
  created_at: string;
  updated_at: string;
}

// Request types for task operations
export interface CreateTaskRequest {
  title: string;
  description?: string;
  priority: TaskPriority;
  deadline: string; // ISO 8601 date
  label_ids?: string[];
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string | null;
  priority?: TaskPriority;
  deadline?: string;
  status?: TaskStatus;
  label_ids?: string[];
}
```

#### Relationships
- Many-to-one with User (task belongs to one user)
- Many-to-many with Label (task can have multiple labels, labels can apply to multiple tasks)

---

### Label

**Purpose:** Represents a custom category/tag for organizing tasks

**Key Attributes:**
- `id`: ObjectId - Unique MongoDB identifier
- `name`: string - Label name (required, max 50 chars, unique per user)
- `owner_id`: ObjectId - Reference to User who owns this label (required)
- `created_at`: datetime - Creation timestamp

#### TypeScript Interface

```typescript
export interface Label {
  id: string;
  name: string;
  owner_id: string;
  created_at: string;
}

// Request types for label operations
export interface CreateLabelRequest {
  name: string;
}

export interface UpdateLabelRequest {
  name: string;
}
```

#### Relationships
- Many-to-one with User (label belongs to one user)
- Many-to-many with Task (label can apply to multiple tasks)

---

## API Specification

### REST API Specification

```yaml
openapi: 3.0.0
info:
  title: Todox API
  version: 1.0.0
  description: RESTful API for Todox task management application
servers:
  - url: http://localhost:8000
    description: Local development
  - url: https://todox-backend.up.railway.app
    description: Production (Railway)

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
    
    Task:
      type: object
      properties:
        id:
          type: string
        title:
          type: string
        description:
          type: string
          nullable: true
        priority:
          type: string
          enum: [High, Medium, Low]
        deadline:
          type: string
          format: date
        status:
          type: string
          enum: [open, done]
        label_ids:
          type: array
          items:
            type: string
        owner_id:
          type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
    
    Label:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        owner_id:
          type: string
        created_at:
          type: string
          format: date-time
    
    AuthResponse:
      type: object
      properties:
        access_token:
          type: string
        token_type:
          type: string
          default: bearer
        expires_in:
          type: integer
          description: Token expiry time in seconds
    
    Error:
      type: object
      properties:
        detail:
          type: string

paths:
  /health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                  database:
                    type: string
  
  /auth/register:
    post:
      summary: Register a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Validation error
        '409':
          description: Email already exists
  
  /auth/login:
    post:
      summary: Login with email and password
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '401':
          description: Invalid credentials
  
  /auth/me:
    get:
      summary: Get current user info
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Current user data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          description: Unauthorized
  
  /tasks:
    get:
      summary: List all tasks for authenticated user
      security:
        - BearerAuth: []
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Task'
        '401':
          description: Unauthorized
    
    post:
      summary: Create a new task
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - title
                - priority
                - deadline
              properties:
                title:
                  type: string
                description:
                  type: string
                priority:
                  type: string
                  enum: [High, Medium, Low]
                deadline:
                  type: string
                  format: date
                label_ids:
                  type: array
                  items:
                    type: string
      responses:
        '201':
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: Validation error
        '401':
          description: Unauthorized
  
  /tasks/{id}:
    patch:
      summary: Update a task
      security:
        - BearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                description:
                  type: string
                  nullable: true
                priority:
                  type: string
                  enum: [High, Medium, Low]
                deadline:
                  type: string
                  format: date
                status:
                  type: string
                  enum: [open, done]
                label_ids:
                  type: array
                  items:
                    type: string
      responses:
        '200':
          description: Task updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: Validation error
        '401':
          description: Unauthorized
        '404':
          description: Task not found
    
    delete:
      summary: Delete a task
      security:
        - BearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Task deleted
        '401':
          description: Unauthorized
        '404':
          description: Task not found
  
  /labels:
    get:
      summary: List all labels for authenticated user
      security:
        - BearerAuth: []
      responses:
        '200':
          description: List of labels
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Label'
        '401':
          description: Unauthorized
    
    post:
      summary: Create a new label
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  maxLength: 50
      responses:
        '201':
          description: Label created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Label'
        '400':
          description: Validation error
        '401':
          description: Unauthorized
        '409':
          description: Label name already exists for this user
  
  /labels/{id}:
    patch:
      summary: Update a label
      security:
        - BearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  maxLength: 50
      responses:
        '200':
          description: Label updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Label'
        '400':
          description: Validation error
        '401':
          description: Unauthorized
        '404':
          description: Label not found
        '409':
          description: Label name already exists
    
    delete:
      summary: Delete a label
      security:
        - BearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Label deleted (also removed from all tasks)
        '401':
          description: Unauthorized
        '404':
          description: Label not found
```


---

## Components

### Frontend Components

#### Authentication Module
**Responsibility:** Handles user registration, login, logout, and auth state management

**Key Interfaces:**
- `useAuth()` hook - Provides auth context (user, login, logout, register functions)
- `<ProtectedRoute>` wrapper - Redirects to login if unauthenticated
- Login and Register page components

**Dependencies:** API Client, React Query, Next.js router

**Technology Stack:** Next.js App Router pages, React Context API, React Query for auth API calls, Zod validation

#### Task Management Module
**Responsibility:** Task CRUD operations, task list display, task forms

**Key Interfaces:**
- Task List page component - Displays all user tasks
- Task Create/Edit modals - Forms for task operations
- `useTasks()` hook - React Query wrapper for task API calls
- `useTask(id)` hook - Single task fetching

**Dependencies:** API Client, Auth Module (protected routes), Shadcn UI components

**Technology Stack:** Next.js pages, React Query mutations/queries, Shadcn Dialog/Form/Card components, Zod validation

#### Label Management Module
**Responsibility:** Label CRUD operations, label assignment to tasks

**Key Interfaces:**
- Labels page component - Label list and management
- Label picker component - Multi-select for task forms
- `useLabels()` hook - React Query wrapper for label API calls

**Dependencies:** API Client, Auth Module, Shadcn UI components

**Technology Stack:** Next.js pages, React Query, Shadcn Select/Checkbox components

#### API Client
**Responsibility:** Centralized HTTP client with JWT token injection and error handling

**Key Interfaces:**
- `apiClient.get/post/patch/delete()` methods
- Automatic Authorization header injection
- Standardized error response parsing

**Dependencies:** Auth context for token access

**Technology Stack:** Fetch API or Axios, TypeScript interfaces for API contracts

---

### Backend Components

#### Authentication Service
**Responsibility:** User registration, login, password hashing, JWT generation and verification

**Key Interfaces:**
- `register_user(email, password)` - Creates new user
- `authenticate_user(email, password)` - Verifies credentials
- `create_access_token(user_id)` - Generates JWT
- `verify_token(token)` - Validates and decodes JWT

**Dependencies:** User Repository, bcrypt, PyJWT

**Technology Stack:** FastAPI routes (`/auth/*`), Pydantic models, bcrypt for hashing, PyJWT for tokens

#### Task Service
**Responsibility:** Business logic for task operations

**Key Interfaces:**
- `create_task(owner_id, task_data)` - Creates new task
- `get_tasks_by_owner(owner_id)` - Retrieves user's tasks
- `update_task(task_id, owner_id, updates)` - Updates task with ownership check
- `delete_task(task_id, owner_id)` - Deletes task with ownership check

**Dependencies:** Task Repository, Label Repository (for validation)

**Technology Stack:** Python classes, async methods, Pydantic models for validation

#### Label Service
**Responsibility:** Business logic for label operations including uniqueness and cascade deletion

**Key Interfaces:**
- `create_label(owner_id, name)` - Creates label with uniqueness check
- `get_labels_by_owner(owner_id)` - Retrieves user's labels
- `update_label(label_id, owner_id, name)` - Updates label with uniqueness check
- `delete_label(label_id, owner_id)` - Deletes label and removes from all tasks

**Dependencies:** Label Repository, Task Repository (for cascade deletion)

**Technology Stack:** Python classes, async methods, Pydantic models

#### Database Repositories
**Responsibility:** Abstract MongoDB operations for each collection

**Key Interfaces:**
- User Repository: CRUD operations on users collection
- Task Repository: CRUD operations on tasks collection, ownership filtering
- Label Repository: CRUD operations on labels collection, uniqueness checking

**Dependencies:** MongoDB client (Motor or Beanie)

**Technology Stack:** Motor (async MongoDB driver) or Beanie (ODM), Pydantic models

#### Middleware Layer
**Responsibility:** JWT verification, CORS configuration, request logging

**Key Interfaces:**
- `get_current_user(token)` - FastAPI dependency for protected routes
- CORS middleware for frontend origin
- Error handling middleware for consistent error responses

**Dependencies:** Authentication Service

**Technology Stack:** FastAPI dependencies, Starlette middleware

---

### Component Diagram

```mermaid
graph TB
    subgraph "Frontend (Next.js)"
        Pages[Pages/Routes] --> AuthMod[Auth Module]
        Pages --> TaskMod[Task Module]
        Pages --> LabelMod[Label Module]
        AuthMod --> APIClient[API Client]
        TaskMod --> APIClient
        LabelMod --> APIClient
        AuthMod --> RQ[React Query]
        TaskMod --> RQ
        LabelMod --> RQ
        Pages --> Shadcn[Shadcn Components]
    end
    
    APIClient -->|HTTPS + JWT| Gateway[API Gateway/CORS]
    
    subgraph "Backend (FastAPI)"
        Gateway --> AuthRoutes[Auth Routes]
        Gateway --> TaskRoutes[Task Routes]
        Gateway --> LabelRoutes[Label Routes]
        
        AuthRoutes --> AuthService[Auth Service]
        TaskRoutes --> Middleware[JWT Middleware]
        LabelRoutes --> Middleware
        
        Middleware --> TaskService[Task Service]
        Middleware --> LabelService[Label Service]
        
        AuthService --> UserRepo[User Repository]
        TaskService --> TaskRepo[Task Repository]
        LabelService --> LabelRepo[Label Repository]
        LabelService -.->|Cascade Delete| TaskRepo
        
        UserRepo --> MongoDB[(MongoDB Atlas)]
        TaskRepo --> MongoDB
        LabelRepo --> MongoDB
    end
    
    style AuthMod fill:#3b82f6,color:#fff
    style TaskMod fill:#3b82f6,color:#fff
    style LabelMod fill:#3b82f6,color:#fff
    style AuthService fill:#9333ea,color:#fff
    style TaskService fill:#9333ea,color:#fff
    style LabelService fill:#9333ea,color:#fff
    style MongoDB fill:#13aa52,color:#fff
```

---

## External APIs

**No external APIs are required for the MVP.**

The Todox application is fully self-contained with no third-party integrations. Future enhancements could include:
- Email service (e.g., SendGrid, Resend) for password reset
- Calendar integration (Google Calendar, Outlook) for deadline syncing
- Notification services for task reminders

---

## Core Workflows

### User Registration and First Task Creation

```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend<br/>(Next.js)
    participant BE as Backend<br/>(FastAPI)
    participant DB as MongoDB

    User->>FE: Navigate to /auth/register
    FE->>User: Display registration form
    
    User->>FE: Submit email + password
    FE->>FE: Validate with Zod
    
    FE->>BE: POST /auth/register
    BE->>BE: Validate with Pydantic
    BE->>BE: Hash password (bcrypt)
    BE->>DB: Insert user document
    DB-->>BE: User created
    BE-->>FE: 201 Created (user object)
    
    FE->>FE: Show success toast
    FE->>FE: Redirect to /auth/login
    
    User->>FE: Enter credentials
    FE->>BE: POST /auth/login
    BE->>DB: Find user by email
    DB-->>BE: User document
    BE->>BE: Verify password hash
    BE->>BE: Generate JWT token
    BE-->>FE: 200 OK (access_token, expires_in)
    
    FE->>FE: Store token (localStorage/cookie)
    FE->>FE: Redirect to /tasks (dashboard)
    FE->>BE: GET /tasks (with JWT header)
    BE->>BE: Verify JWT, extract user_id
    BE->>DB: Query tasks where owner_id = user_id
    DB-->>BE: Empty array (new user)
    BE-->>FE: 200 OK ([])
    
    FE->>User: Display empty state + Create Task button
    
    User->>FE: Click "Create Task"
    FE->>User: Display task creation modal
    User->>FE: Fill title, priority, deadline
    
    FE->>BE: POST /tasks (with JWT + task data)
    BE->>BE: Verify JWT, validate data
    BE->>DB: Insert task document with owner_id
    DB-->>BE: Task created
    BE-->>FE: 201 Created (task object)
    
    FE->>FE: Add task to cached list
    FE->>FE: Close modal, show success toast
    FE->>User: Display task in list
```

### Task Update with Label Assignment

```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend
    participant BE as Backend
    participant DB as MongoDB

    User->>FE: Click Edit on task
    FE->>FE: Open edit modal with current data
    
    User->>FE: Modify priority to "High"
    User->>FE: Select labels "Work", "Urgent"
    User->>FE: Click Save
    
    FE->>BE: PATCH /tasks/:id<br/>{priority: "High", label_ids: [...]}
    BE->>BE: Verify JWT → user_id
    BE->>DB: Find task by _id AND owner_id
    
    alt Task not found or not owned
        DB-->>BE: null
        BE-->>FE: 404 Not Found
        FE->>User: Show error toast
    else Task found
        DB-->>BE: Task document
        BE->>DB: Validate label_ids exist for this user
        DB-->>BE: Labels valid
        BE->>DB: Update task with new values + updated_at
        DB-->>BE: Updated task
        BE-->>FE: 200 OK (updated task)
        
        FE->>FE: Update cached task in React Query
        FE->>FE: Close modal
        FE->>User: Show success toast + updated task in list
    end
```

---

## Database Schema

### MongoDB Collections

#### users Collection

```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "hashed_password": "$2b$12$...",
  "created_at": ISODate("2025-01-12T10:00:00Z"),
  "updated_at": ISODate("2025-01-12T10:00:00Z")
}
```

**Indexes:**
- `email`: Unique index for fast lookup and uniqueness constraint
- `_id`: Default primary key index

**Schema Validation:**
```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["email", "hashed_password", "created_at", "updated_at"],
    "properties": {
      "email": {
        "bsonType": "string",
        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
      },
      "hashed_password": {
        "bsonType": "string",
        "minLength": 60,
        "maxLength": 60
      },
      "created_at": { "bsonType": "date" },
      "updated_at": { "bsonType": "date" }
    }
  }
}
```

#### tasks Collection

```json
{
  "_id": ObjectId("..."),
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the architecture",
  "priority": "High",
  "deadline": ISODate("2025-01-15"),
  "status": "open",
  "label_ids": [ObjectId("..."), ObjectId("...")],
  "owner_id": ObjectId("..."),
  "created_at": ISODate("2025-01-12T10:30:00Z"),
  "updated_at": ISODate("2025-01-12T10:30:00Z")
}
```

**Indexes:**
- `owner_id`: Index for efficient querying of user's tasks
- `owner_id + created_at`: Compound index for sorted queries
- `_id`: Default primary key index

**Schema Validation:**
```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["title", "priority", "deadline", "status", "label_ids", "owner_id", "created_at", "updated_at"],
    "properties": {
      "title": {
        "bsonType": "string",
        "minLength": 1,
        "maxLength": 200
      },
      "description": {
        "bsonType": ["string", "null"]
      },
      "priority": {
        "enum": ["High", "Medium", "Low"]
      },
      "deadline": {
        "bsonType": "date"
      },
      "status": {
        "enum": ["open", "done"]
      },
      "label_ids": {
        "bsonType": "array",
        "items": { "bsonType": "objectId" }
      },
      "owner_id": {
        "bsonType": "objectId"
      },
      "created_at": { "bsonType": "date" },
      "updated_at": { "bsonType": "date" }
    }
  }
}
```

#### labels Collection

```json
{
  "_id": ObjectId("..."),
  "name": "Work",
  "owner_id": ObjectId("..."),
  "created_at": ISODate("2025-01-12T10:15:00Z")
}
```

**Indexes:**
- `owner_id + name`: Compound unique index for per-user label name uniqueness
- `owner_id`: Index for efficient querying of user's labels
- `_id`: Default primary key index

**Schema Validation:**
```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["name", "owner_id", "created_at"],
    "properties": {
      "name": {
        "bsonType": "string",
        "minLength": 1,
        "maxLength": 50
      },
      "owner_id": {
        "bsonType": "objectId"
      },
      "created_at": { "bsonType": "date" }
    }
  }
}
```


---

## Frontend Architecture

### Component Architecture

#### Component Organization

```
frontend/
├── src/
│   ├── app/                          # Next.js App Router
│   │   ├── layout.tsx                # Root layout with providers
│   │   ├── page.tsx                  # Landing/redirect page
│   │   ├── auth/
│   │   │   ├── login/
│   │   │   │   └── page.tsx          # Login page
│   │   │   └── register/
│   │   │       └── page.tsx          # Registration page
│   │   ├── tasks/
│   │   │   └── page.tsx              # Task list dashboard
│   │   └── labels/
│   │       └── page.tsx              # Label management page
│   │
│   ├── components/                   # Reusable components
│   │   ├── ui/                       # Shadcn UI primitives
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   ├── select.tsx
│   │   │   ├── badge.tsx
│   │   │   └── ...
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskCreateModal.tsx
│   │   │   ├── TaskEditModal.tsx
│   │   │   └── TaskDeleteConfirm.tsx
│   │   └── labels/
│   │       ├── LabelList.tsx
│   │       ├── LabelCreateModal.tsx
│   │       ├── LabelEditModal.tsx
│   │       └── LabelPicker.tsx
│   │
│   ├── lib/                          # Utility libraries
│   │   ├── api.ts                    # API client setup
│   │   ├── auth.tsx                  # Auth context provider
│   │   ├── utils.ts                  # Helper functions
│   │   └── validations.ts            # Zod schemas
│   │
│   ├── hooks/                        # Custom React hooks
│   │   ├── useAuth.ts                # Auth hook
│   │   ├── useTasks.ts               # Task operations hook
│   │   └── useLabels.ts              # Label operations hook
│   │
│   ├── types/                        # TypeScript types
│   │   ├── api.ts                    # API request/response types
│   │   ├── models.ts                 # Data model types
│   │   └── index.ts                  # Type exports
│   │
│   └── styles/
│       └── globals.css               # Tailwind directives + global styles
│
├── public/                           # Static assets
├── .env.local                        # Local environment variables (gitignored)
├── .env.example                      # Environment variable template
├── next.config.js                    # Next.js configuration
├── tailwind.config.ts                # Tailwind configuration
├── tsconfig.json                     # TypeScript configuration
└── package.json
```

#### Component Template

```typescript
// Standard component structure for Todox
// Example: components/tasks/TaskCard.tsx

import { Task } from '@/types/models';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Pencil, Trash2, Check } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onToggleStatus: (taskId: string, newStatus: 'open' | 'done') => void;
}

export function TaskCard({ task, onEdit, onDelete, onToggleStatus }: TaskCardProps) {
  const priorityColors = {
    High: 'bg-red-500',
    Medium: 'bg-amber-500',
    Low: 'bg-blue-500',
  };

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <input
                type="checkbox"
                checked={task.status === 'done'}
                onChange={() => onToggleStatus(task.id, task.status === 'open' ? 'done' : 'open')}
                className="w-5 h-5"
                aria-label="Toggle task completion"
              />
              <h3 className={`text-lg font-semibold ${task.status === 'done' ? 'line-through text-gray-500' : ''}`}>
                {task.title}
              </h3>
            </div>
            
            {task.description && (
              <p className="text-sm text-gray-600 mb-2">{task.description}</p>
            )}
            
            <div className="flex flex-wrap items-center gap-2">
              <Badge className={priorityColors[task.priority]}>
                {task.priority}
              </Badge>
              <span className="text-sm text-gray-500">
                Due: {new Date(task.deadline).toLocaleDateString()}
              </span>
              {task.label_ids.length > 0 && (
                <span className="text-xs text-gray-400">
                  {task.label_ids.length} label(s)
                </span>
              )}
            </div>
          </div>
          
          <div className="flex gap-2 ml-4">
            <Button
              size="icon"
              variant="ghost"
              onClick={() => onEdit(task)}
              aria-label="Edit task"
            >
              <Pencil className="h-4 w-4" />
            </Button>
            <Button
              size="icon"
              variant="ghost"
              onClick={() => onDelete(task.id)}
              aria-label="Delete task"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

### State Management Architecture

#### State Structure

```typescript
// State management using React Query for server state
// Client state managed with React hooks and Context API

// Auth State (Context API)
interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

// Server State (React Query)
// Tasks
const tasksKeys = {
  all: ['tasks'] as const,
  lists: () => [...tasksKeys.all, 'list'] as const,
  detail: (id: string) => [...tasksKeys.all, 'detail', id] as const,
};

// Labels
const labelsKeys = {
  all: ['labels'] as const,
  lists: () => [...labelsKeys.all, 'list'] as const,
};

// Example React Query hook usage
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useTasks() {
  const queryClient = useQueryClient();
  
  const { data: tasks, isLoading, error } = useQuery({
    queryKey: tasksKeys.lists(),
    queryFn: () => apiClient.get<Task[]>('/tasks'),
  });
  
  const createTask = useMutation({
    mutationFn: (data: CreateTaskRequest) => apiClient.post<Task>('/tasks', data),
    onSuccess: (newTask) => {
      queryClient.setQueryData<Task[]>(tasksKeys.lists(), (old = []) => [newTask, ...old]);
    },
  });
  
  return { tasks, isLoading, error, createTask };
}
```

#### State Management Patterns

- **Server State:** React Query for all API data (tasks, labels, user info)
- **Client State:** React hooks (useState, useReducer) for UI state (modals, forms)
- **Auth State:** Context API for authentication state shared across app
- **Form State:** Controlled components with Zod validation
- **Optimistic Updates:** React Query optimistic updates for status toggles
- **Cache Invalidation:** Automatic refetch on window focus for fresh data

### Routing Architecture

#### Route Organization

```
/ (root)
├── /auth
│   ├── /login              # Public route - Login page
│   └── /register           # Public route - Registration page
├── /tasks                  # Protected - Task dashboard (main view)
└── /labels                 # Protected - Label management

Protected routes automatically redirect to /auth/login if not authenticated
```

#### Protected Route Pattern

```typescript
// lib/auth.tsx - Auth Context and Protected Route wrapper

'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check for stored token on mount
    const token = localStorage.getItem('access_token');
    if (token) {
      // Verify token and fetch user
      fetchCurrentUser(token)
        .then(setUser)
        .catch(() => {
          localStorage.removeItem('access_token');
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const response = await apiClient.post<AuthResponse>('/auth/login', { email, password });
    localStorage.setItem('access_token', response.access_token);
    const user = await fetchCurrentUser(response.access_token);
    setUser(user);
    router.push('/tasks');
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    router.push('/auth/login');
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}

// Protected Route Component
export function ProtectedRoute({ children }: { children: ReactNode }) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/auth/login');
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return <div>Loading...</div>; // Or skeleton loader
  }

  if (!user) {
    return null; // Will redirect via useEffect
  }

  return <>{children}</>;
}
```

### Frontend Services Layer

#### API Client Setup

```typescript
// lib/api.ts - Centralized API client with auth token injection

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = localStorage.getItem('access_token');
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired or invalid
        localStorage.removeItem('access_token');
        window.location.href = '/auth/login';
        throw new Error('Unauthorized');
      }

      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || 'Request failed');
    }

    if (response.status === 204) {
      return {} as T; // No content
    }

    return response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async patch<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new APIClient(API_BASE_URL);
```

#### Service Example

```typescript
// hooks/useTasks.ts - Task service layer using React Query

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '@/types/api';

const tasksKeys = {
  all: ['tasks'] as const,
  lists: () => [...tasksKeys.all, 'list'] as const,
};

export function useTasks() {
  const queryClient = useQueryClient();

  // Fetch all tasks
  const { data: tasks = [], isLoading, error } = useQuery({
    queryKey: tasksKeys.lists(),
    queryFn: () => apiClient.get<Task[]>('/tasks'),
  });

  // Create task mutation
  const createTask = useMutation({
    mutationFn: (data: CreateTaskRequest) => 
      apiClient.post<Task>('/tasks', data),
    onSuccess: (newTask) => {
      queryClient.setQueryData<Task[]>(
        tasksKeys.lists(),
        (old = []) => [newTask, ...old]
      );
    },
  });

  // Update task mutation
  const updateTask = useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateTaskRequest }) =>
      apiClient.patch<Task>(`/tasks/${id}`, data),
    onSuccess: (updatedTask) => {
      queryClient.setQueryData<Task[]>(
        tasksKeys.lists(),
        (old = []) => old.map(t => t.id === updatedTask.id ? updatedTask : t)
      );
    },
  });

  // Delete task mutation
  const deleteTask = useMutation({
    mutationFn: (id: string) => apiClient.delete(`/tasks/${id}`),
    onSuccess: (_, deletedId) => {
      queryClient.setQueryData<Task[]>(
        tasksKeys.lists(),
        (old = []) => old.filter(t => t.id !== deletedId)
      );
    },
  });

  return {
    tasks,
    isLoading,
    error,
    createTask,
    updateTask,
    deleteTask,
  };
}
```


---

## Backend Architecture

### Service Architecture

#### Controller/Route Organization

```
backend/
├── src/
│   ├── main.py                       # FastAPI app initialization and startup
│   ├── core/
│   │   ├── config.py                 # Environment variable configuration
│   │   ├── security.py               # JWT utilities, password hashing
│   │   └── database.py               # MongoDB client and connection
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py               # Auth routes (/auth/*)
│   │       ├── tasks.py              # Task routes (/tasks, /tasks/:id)
│   │       └── labels.py             # Label routes (/labels, /labels/:id)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py           # Auth business logic
│   │   ├── task_service.py           # Task business logic
│   │   └── label_service.py          # Label business logic
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py        # User database operations
│   │   ├── task_repository.py        # Task database operations
│   │   └── label_repository.py       # Label database operations
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                   # User Pydantic model
│   │   ├── task.py                   # Task Pydantic models
│   │   └── label.py                  # Label Pydantic models
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                   # Auth request/response schemas
│   │   ├── task.py                   # Task request/response schemas
│   │   └── label.py                  # Label request/response schemas
│   │
│   └── middleware/
│       ├── __init__.py
│       ├── auth_middleware.py        # JWT verification dependency
│       └── cors_middleware.py        # CORS configuration
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Pytest fixtures
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── test_labels.py
│
├── .env                              # Environment variables (gitignored)
├── .env.example                      # Environment variable template
├── pyproject.toml                    # Poetry configuration
├── requirements.txt                  # Pip dependencies
└── README.md
```

#### Controller Template

```python
# api/v1/tasks.py - Task routes (controller layer)

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId

from src.middleware.auth_middleware import get_current_user
from src.services.task_service import TaskService
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends()
):
    """Get all tasks for the authenticated user."""
    tasks = await task_service.get_tasks_by_owner(current_user.id)
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends()
):
    """Create a new task."""
    task = await task_service.create_task(current_user.id, task_data)
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends()
):
    """Update an existing task."""
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    task = await task_service.update_task(task_id, current_user.id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends()
):
    """Delete a task."""
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    deleted = await task_service.delete_task(task_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return None
```

### Database Architecture

#### Data Access Layer

```python
# repositories/task_repository.py - Task repository pattern

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

from src.models.task import Task, TaskInDB

class TaskRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.tasks

    async def create(self, task_data: dict) -> TaskInDB:
        """Insert a new task document."""
        task_data['created_at'] = datetime.utcnow()
        task_data['updated_at'] = datetime.utcnow()
        
        result = await self.collection.insert_one(task_data)
        task_data['_id'] = result.inserted_id
        
        return TaskInDB(**task_data)

    async def find_by_owner(self, owner_id: ObjectId) -> List[TaskInDB]:
        """Find all tasks belonging to a user, sorted by created_at desc."""
        cursor = self.collection.find(
            {'owner_id': owner_id}
        ).sort('created_at', -1)
        
        tasks = await cursor.to_list(length=None)
        return [TaskInDB(**task) for task in tasks]

    async def find_by_id(self, task_id: ObjectId, owner_id: ObjectId) -> Optional[TaskInDB]:
        """Find a task by ID, ensuring it belongs to the owner."""
        task = await self.collection.find_one({
            '_id': task_id,
            'owner_id': owner_id
        })
        
        return TaskInDB(**task) if task else None

    async def update(self, task_id: ObjectId, owner_id: ObjectId, update_data: dict) -> Optional[TaskInDB]:
        """Update a task's fields."""
        update_data['updated_at'] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {'_id': task_id, 'owner_id': owner_id},
            {'$set': update_data},
            return_document=True
        )
        
        return TaskInDB(**result) if result else None

    async def delete(self, task_id: ObjectId, owner_id: ObjectId) -> bool:
        """Delete a task."""
        result = await self.collection.delete_one({
            '_id': task_id,
            'owner_id': owner_id
        })
        
        return result.deleted_count > 0

    async def remove_label_from_all_tasks(self, label_id: ObjectId, owner_id: ObjectId):
        """Remove a label ID from all tasks (cascade delete)."""
        await self.collection.update_many(
            {'owner_id': owner_id},
            {'$pull': {'label_ids': label_id}}
        )
```

### Authentication and Authorization

#### Auth Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI
    participant Auth as Auth Middleware
    participant Service as Auth Service
    participant DB as MongoDB

    Note over Client,DB: Registration Flow
    Client->>API: POST /auth/register<br/>{email, password}
    API->>Service: register_user()
    Service->>Service: validate_email_format()
    Service->>DB: find user by email
    DB-->>Service: null (unique check)
    Service->>Service: hash_password(password)
    Service->>DB: insert user document
    DB-->>Service: user created
    Service-->>API: User object (no password)
    API-->>Client: 201 Created + User

    Note over Client,DB: Login Flow
    Client->>API: POST /auth/login<br/>{email, password}
    API->>Service: authenticate_user()
    Service->>DB: find user by email
    DB-->>Service: user document
    Service->>Service: verify_password(password, hashed)
    Service->>Service: create_access_token(user.id)
    Service-->>API: {access_token, expires_in}
    API-->>Client: 200 OK + JWT

    Note over Client,DB: Protected Request Flow
    Client->>API: GET /tasks<br/>Authorization: Bearer {token}
    API->>Auth: verify_token(token)
    Auth->>Auth: decode JWT, check expiry
    Auth->>DB: find user by id from token
    DB-->>Auth: user document
    Auth-->>API: current_user (dependency)
    API->>Service: get_tasks_by_owner(user.id)
    Service->>DB: query tasks
    DB-->>Service: task documents
    Service-->>API: tasks list
    API-->>Client: 200 OK + tasks
```

#### Middleware/Guards

```python
# middleware/auth_middleware.py - JWT verification dependency

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt
from datetime import datetime
from bson import ObjectId

from src.core.config import settings
from src.core.database import get_database
from src.repositories.user_repository import UserRepository
from src.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db = Depends(get_database)
) -> User:
    """
    FastAPI dependency that verifies JWT token and returns current user.
    Raises 401 Unauthorized if token is invalid, expired, or user not found.
    """
    token = credentials.credentials
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        exp = payload.get("exp")
        if exp is None or datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
    except JWTError:
        raise credentials_exception
    
    # Fetch user from database
    user_repo = UserRepository(db)
    user = await user_repo.find_by_id(ObjectId(user_id))
    
    if user is None:
        raise credentials_exception
    
    return user

# core/security.py - Password hashing and JWT generation

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(seconds=settings.JWT_EXPIRES_IN)
    
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        "sub": user_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
```


---

## Unified Project Structure

```plaintext
todox/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Lint and test on PR
│       └── deploy.yml                # Deploy on tag (backend) and push (frontend)
│
├── frontend/                         # Next.js application
│   ├── src/
│   │   ├── app/                      # App Router pages
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── auth/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── register/page.tsx
│   │   │   ├── tasks/page.tsx
│   │   │   └── labels/page.tsx
│   │   ├── components/               # React components
│   │   │   ├── ui/                   # Shadcn primitives
│   │   │   ├── auth/
│   │   │   ├── tasks/
│   │   │   └── labels/
│   │   ├── lib/                      # Utilities
│   │   │   ├── api.ts
│   │   │   ├── auth.tsx
│   │   │   └── utils.ts
│   │   ├── hooks/                    # Custom hooks
│   │   ├── types/                    # TypeScript types
│   │   └── styles/
│   │       └── globals.css
│   ├── public/
│   ├── .env.local                    # Local env vars (gitignored)
│   ├── .env.example
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── components.json               # Shadcn config
│   └── package.json
│
├── backend/                          # FastAPI application
│   ├── src/
│   │   ├── main.py                   # App entry point
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── tasks.py
│   │   │       └── labels.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── task_service.py
│   │   │   └── label_service.py
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   ├── task_repository.py
│   │   │   └── label_repository.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── label.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── task.py
│   │   │   └── label.py
│   │   └── middleware/
│   │       ├── auth_middleware.py
│   │       └── cors_middleware.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   │   └── test_labels.py
│   ├── .env                          # Local env vars (gitignored)
│   ├── .env.example
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── README.md
│
├── e2e/                              # Playwright E2E tests
│   ├── tests/
│   │   ├── auth.spec.ts
│   │   ├── tasks.spec.ts
│   │   └── labels.spec.ts
│   ├── playwright.config.ts
│   └── package.json
│
├── docs/                             # Project documentation
│   ├── prd.md
│   ├── front-end-spec.md
│   ├── architecture.md               # This file
│   └── README.md
│
├── .gitignore
├── README.md                         # Root README with setup instructions
└── LICENSE
```

---

## Development Workflow

### Local Development Setup

#### Prerequisites

```bash
# System requirements
node --version    # v18+ required
python --version  # 3.11+ required
npm --version     # 10+ required
pip --version     # 23+ required

# Install MongoDB Compass (optional, for local DB viewing)
# Or use MongoDB MCP in your IDE
```

#### Initial Setup

```bash
# Clone repository
git clone https://github.com/yourusername/todox.git
cd todox

# Frontend setup
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend setup
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set:
# - MONGODB_URI (your MongoDB Atlas connection string)
# - JWT_SECRET (generate with: openssl rand -hex 32)
# - CORS_ORIGINS=http://localhost:3000

# E2E tests setup (optional for initial dev)
cd ../e2e
npm install
```

#### Development Commands

```bash
# Start backend (from backend/ directory)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (from frontend/ directory)
npm run dev
# Opens at http://localhost:3000

# Run backend tests (from backend/)
pytest

# Run E2E tests (from e2e/, requires both servers running)
npx playwright test
npx playwright test --ui  # Interactive mode

# Linting and type checking
# Frontend
npm run lint
npm run type-check

# Backend
mypy src/
ruff check src/
```

### Environment Configuration

#### Required Environment Variables

```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn-here

# Backend (.env)
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/todox?retryWrites=true&w=majority
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=3600
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000

# Optional
SENTRY_DSN=your-sentry-dsn-here
```

---

## Deployment Architecture

### Deployment Strategy

**Frontend Deployment:**
- **Platform:** Vercel
- **Build Command:** `cd frontend && npm run build`
- **Output Directory:** `frontend/.next`
- **CDN/Edge:** Vercel Edge Network (automatic)
- **Automatic Deployments:** Push to `main` branch triggers production deploy, PRs create preview URLs

**Backend Deployment:**
- **Platform:** Railway
- **Build Command:** `pip install -r requirements.txt` (automatic)
- **Deployment Method:** Docker container or Nixpacks (Railway automatic detection)
- **Automatic Deployments:** Git tag push triggers production deploy (e.g., `git tag v1.0.0 && git push origin v1.0.0`)

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml - Continuous Integration

name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  frontend-lint-and-type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci
      - name: Lint
        working-directory: ./frontend
        run: npm run lint
      - name: Type check
        working-directory: ./frontend
        run: npm run type-check
  
  backend-lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        working-directory: ./backend
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Lint with ruff
        working-directory: ./backend
        run: ruff check src/
      - name: Type check with mypy
        working-directory: ./backend
        run: mypy src/
      - name: Run tests
        working-directory: ./backend
        run: pytest
        env:
          MONGODB_URI: ${{ secrets.MONGODB_URI_TEST }}
          JWT_SECRET: test-secret-key

  e2e-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - name: Install Playwright
        working-directory: ./e2e
        run: |
          npm ci
          npx playwright install --with-deps
      - name: Run E2E tests
        working-directory: ./e2e
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: e2e/playwright-report/
```

### Environments

| Environment | Frontend URL | Backend URL | Purpose |
|-------------|--------------|-------------|---------|
| Development | http://localhost:3000 | http://localhost:8000 | Local development |
| Staging | N/A (preview URLs) | N/A (Railway preview) | PR previews (optional) |
| Production | https://todox.vercel.app | https://todox-backend.up.railway.app | Live environment |

---

## Security and Performance

### Security Requirements

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

### Performance Optimization

**Frontend Performance:**
- **Bundle Size Target:** < 200KB initial JS bundle
- **Loading Strategy:** Code splitting by route (Next.js automatic), lazy load modals
- **Caching Strategy:** React Query caches API responses with 5-minute stale time, background refetch on window focus

**Backend Performance:**
- **Response Time Target:** < 500ms for API endpoints (95th percentile)
- **Database Optimization:** MongoDB indexes on `owner_id` fields, compound index on `owner_id + created_at` for tasks
- **Caching Strategy:** No backend caching initially; can add Redis for session caching if needed

---

## Testing Strategy

### Testing Pyramid

```
        E2E Tests (Playwright)
       /                      \
      /   Integration Tests     \
     /    (Backend API tests)     \
    /                              \
   /     Frontend Unit Tests        \
  /    (Vitest) Backend Unit Tests   \
 /              (Pytest)              \
------------------------------------------------
```

### Test Organization

#### Frontend Tests

```
frontend/src/
├── components/
│   └── tasks/
│       ├── TaskCard.tsx
│       └── TaskCard.test.tsx        # Component unit tests
├── lib/
│   └── utils.test.ts                 # Utility function tests
└── hooks/
    └── useTasks.test.ts              # Hook tests (minimal, mostly covered by E2E)
```

#### Backend Tests

```
backend/tests/
├── conftest.py                       # Pytest fixtures (test DB, test client)
├── test_auth.py                      # Auth endpoint integration tests
├── test_tasks.py                     # Task endpoint integration tests
├── test_labels.py                    # Label endpoint integration tests
├── test_repositories.py              # Repository unit tests
└── test_services.py                  # Service layer unit tests
```

#### E2E Tests

```
e2e/tests/
├── auth.spec.ts                      # Registration, login, logout flows
├── tasks.spec.ts                     # Task CRUD operations
└── labels.spec.ts                    # Label management and assignment
```

### Test Examples

#### Frontend Component Test

```typescript
// components/tasks/TaskCard.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from './TaskCard';
import { Task } from '@/types/models';

describe('TaskCard', () => {
  const mockTask: Task = {
    id: '1',
    title: 'Test Task',
    description: 'Test description',
    priority: 'High',
    deadline: '2025-01-15',
    status: 'open',
    label_ids: [],
    owner_id: 'user1',
    created_at: '2025-01-12T10:00:00Z',
    updated_at: '2025-01-12T10:00:00Z',
  };

  it('renders task details correctly', () => {
    render(
      <TaskCard
        task={mockTask}
        onEdit={jest.fn()}
        onDelete={jest.fn()}
        onToggleStatus={jest.fn()}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('High')).toBeInTheDocument();
    expect(screen.getByText(/Due:/)).toBeInTheDocument();
  });

  it('calls onToggleStatus when checkbox is clicked', () => {
    const mockToggle = jest.fn();
    render(
      <TaskCard
        task={mockTask}
        onEdit={jest.fn()}
        onDelete={jest.fn()}
        onToggleStatus={mockToggle}
      />
    );

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    expect(mockToggle).toHaveBeenCalledWith('1', 'done');
  });
});
```

#### Backend API Test

```python
# tests/test_tasks.py

import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_create_task(async_client: AsyncClient, auth_headers: dict):
    """Test creating a new task."""
    task_data = {
        "title": "Test Task",
        "priority": "High",
        "deadline": "2025-01-15",
        "description": "Test description"
    }
    
    response = await async_client.post(
        "/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "High"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_tasks_requires_auth(async_client: AsyncClient):
    """Test that getting tasks requires authentication."""
    response = await async_client.get("/tasks")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_task_not_owned(async_client: AsyncClient, auth_headers: dict, other_user_task_id: str):
    """Test that users cannot update tasks they don't own."""
    response = await async_client.patch(
        f"/tasks/{other_user_task_id}",
        json={"title": "Hacked"},
        headers=auth_headers
    )
    
    assert response.status_code == 404
```

#### E2E Test

```typescript
// e2e/tests/tasks.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Task Management', () => {
  test.beforeEach(async ({ page }) => {
    // Register and login before each test
    await page.goto('/auth/register');
    await page.fill('input[type="email"]', `test-${Date.now()}@example.com`);
    await page.fill('input[type="password"]', 'testpassword123');
    await page.click('button[type="submit"]');
    
    await page.waitForURL('/auth/login');
    await page.fill('input[type="email"]', `test-${Date.now()}@example.com`);
    await page.fill('input[type="password"]', 'testpassword123');
    await page.click('button[type="submit"]');
    
    await page.waitForURL('/tasks');
  });

  test('create a new task', async ({ page }) => {
    // Click Create Task button
    await page.click('text=Create Task');
    
    // Fill in task details
    await page.fill('input[name="title"]', 'Buy groceries');
    await page.selectOption('select[name="priority"]', 'High');
    await page.fill('input[type="date"]', '2025-01-20');
    await page.fill('textarea[name="description"]', 'Milk, eggs, bread');
    
    // Submit form
    await page.click('button:has-text("Create Task")');
    
    // Verify task appears in list
    await expect(page.locator('text=Buy groceries')).toBeVisible();
    await expect(page.locator('text=High')).toBeVisible();
  });

  test('mark task as done', async ({ page }) => {
    // Create a task first
    await page.click('text=Create Task');
    await page.fill('input[name="title"]', 'Test Task');
    await page.selectOption('select[name="priority"]', 'Low');
    await page.fill('input[type="date"]', '2025-01-20');
    await page.click('button:has-text("Create Task")');
    
    // Check the task checkbox
    await page.check('input[type="checkbox"]');
    
    // Verify task title has strikethrough
    const taskTitle = page.locator('h3:has-text("Test Task")');
    await expect(taskTitle).toHaveClass(/line-through/);
  });
});
```

---

## Coding Standards

### Critical Fullstack Rules

- **Type Sharing:** Define shared types in TypeScript interfaces (frontend) and Pydantic models (backend) with consistent naming and structure
- **API Calls:** Always use the centralized `apiClient` (frontend) - never use `fetch()` directly outside of `lib/api.ts`
- **Environment Variables:** Access only through config objects (`process.env` frontend, `settings` backend) - never inline `process.env` or `os.getenv()`
- **Error Handling:** All API routes must use FastAPI's HTTPException with appropriate status codes and clear `detail` messages
- **Authentication:** Always use `get_current_user` dependency for protected routes - never manually parse JWT in route handlers
- **Database Operations:** All database access must go through repository classes - never call MongoDB client directly in services or routes
- **Validation:** Use Pydantic (backend) and Zod (frontend) for all data validation - never trust client input or skip validation
- **State Updates:** Never mutate React state directly - use proper state setters and React Query mutations
- **Password Handling:** Never log, display, or return passwords - always hash with bcrypt before storage

### Naming Conventions

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

## Error Handling Strategy

### Error Flow

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant API as FastAPI
    participant Service
    participant DB as MongoDB

    FE->>API: POST /tasks (invalid data)
    API->>API: Pydantic validation
    API-->>FE: 400 Bad Request<br/>{detail: "Validation error"}
    FE->>FE: Display error toast

    FE->>API: PATCH /tasks/999 (with auth)
    API->>Service: update_task()
    Service->>DB: find task
    DB-->>Service: null
    Service-->>API: None
    API-->>FE: 404 Not Found<br/>{detail: "Task not found"}
    FE->>FE: Display error toast

    FE->>API: GET /tasks (expired token)
    API->>API: JWT verification
    API-->>FE: 401 Unauthorized<br/>{detail: "Token expired"}
    FE->>FE: Clear token, redirect to login
```

### Error Response Format

```typescript
interface ApiError {
  detail: string;
  // Optionally include:
  field?: string;  // For validation errors
  code?: string;   // Error code for programmatic handling
}

// Backend example
raise HTTPException(
    status_code=400,
    detail="Task title cannot be empty"
)

// Frontend error handling
try {
  await apiClient.post('/tasks', data);
} catch (error) {
  toast.error(error.message || 'An error occurred');
}
```

### Frontend Error Handling

```typescript
// lib/api.ts - Centralized error handling

private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${this.baseURL}${endpoint}`, config);

  if (!response.ok) {
    // Handle auth errors
    if (response.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/auth/login';
      throw new Error('Session expired. Please log in again.');
    }

    // Parse error response
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}
```

### Backend Error Handling

```python
# core/exceptions.py - Custom exception handlers

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Validation error", "errors": exc.errors()}
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # Log the exception
        print(f"Unhandled exception: {exc}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )
```

---

## Monitoring and Observability

### Monitoring Stack

- **Frontend Monitoring:** Vercel Analytics (automatic) + optional Sentry for error tracking
- **Backend Monitoring:** Railway metrics (CPU, memory, requests) + optional Sentry for error tracking
- **Error Tracking:** Sentry (optional) - captures frontend and backend errors with stack traces
- **Performance Monitoring:** Vercel Web Vitals for frontend, Railway response time metrics for backend

### Key Metrics

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

## Checklist Results Report

**Architecture Document Completeness Check:**

✅ **Introduction & Project Context**
- Starter template status documented (greenfield project)
- Change log initialized
- Document purpose clearly stated

✅ **High Level Architecture**
- Technical summary covers all tiers and deployment
- Platform choice justified (Railway + Vercel + MongoDB Atlas)
- Repository structure defined (simple monorepo)
- Architecture diagram visualizes complete system
- Architectural patterns documented with rationale

✅ **Tech Stack**
- Comprehensive technology table with versions and rationale
- All categories covered: languages, frameworks, databases, testing, deployment
- Specific version numbers provided where applicable

✅ **Data Models**
- Three core models defined: User, Task, Label
- TypeScript interfaces provided for frontend consumption
- Relationships documented

✅ **API Specification**
- Complete OpenAPI 3.0 spec for REST API
- All endpoints documented with request/response schemas
- Authentication flow included

✅ **Components**
- Frontend and backend components identified
- Responsibilities and interfaces defined
- Component interaction diagram provided

✅ **External APIs**
- Explicitly stated: No external APIs for MVP

✅ **Core Workflows**
- Two critical workflows with sequence diagrams
- Registration, authentication, task creation, task update flows covered

✅ **Database Schema**
- MongoDB collection schemas defined
- Indexes specified for performance
- Schema validation rules included

✅ **Frontend Architecture**
- Component organization and structure
- State management approach (React Query + Context)
- Routing architecture with protected routes
- Complete code examples for components, hooks, API client

✅ **Backend Architecture**
- Service architecture with repository pattern
- Controller/route organization
- Database access layer
- Authentication middleware with JWT verification
- Complete code examples

✅ **Project Structure**
- Unified monorepo structure documented
- Clear separation of frontend, backend, E2E tests, docs

✅ **Development Workflow**
- Local setup instructions
- Required environment variables
- Development commands

✅ **Deployment Architecture**
- Deployment strategy for both tiers
- CI/CD pipeline configuration
- Environment table

✅ **Security & Performance**
- Security requirements for frontend and backend
- Performance optimization strategies and targets

✅ **Testing Strategy**
- Testing pyramid visualization
- Test organization for all test types
- Complete test examples (frontend, backend, E2E)

✅ **Coding Standards**
- Critical fullstack rules defined
- Naming conventions table
- Project-specific conventions documented

✅ **Error Handling**
- Error flow diagram
- Standardized error format
- Frontend and backend error handling patterns

✅ **Monitoring**
- Monitoring stack defined
- Key metrics for frontend and backend

**Overall Assessment:** Full-stack architecture document is comprehensive, detailed, and ready for AI-driven development. All sections complete with appropriate code examples, diagrams, and rationale. The document successfully bridges frontend and backend concerns while maintaining clarity for developers working on either tier.

