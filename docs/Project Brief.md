# project_brief.md

## Executive Summary
Build a full-stack TODO app by **October 13, 2025**. Users register, log in, manage tasks, and organize with labels. Backend is **FastAPI**. Frontend is **Next.js** with **Shadcn** UI. **MongoDB** stores data. **Railway** hosts the backend. **Vercel** hosts the frontend. **Playwright** runs E2E tests. **Context7 MCP** orchestrates structured prompts and guardrails. The brief defines scope, stories, acceptance criteria, tech stack, file layout, workflow, rubric mapping, and risks. Follow it to ship a clean MVP then stretch.

---

## Goals & Scope
**Goals**
- Ship an MVP TODO app that satisfies all required stories and rubric points.
- Keep the codebase modular, testable, and clear.
- Provide a smooth deploy path on Railway and Vercel.
- Prove proficiency with Git hygiene and daily commits.

**In-Scope**
- Auth: sign up, log in, log out.
- Task CRUD with required fields: title, description (optional), priority, deadline.
- Labels: create, assign, list.
- Persistent storage in MongoDB.
- E2E happy-path tests for core flows.
- Basic error states and empty states.

**Out-of-Scope (for MVP)**
- Social login.
- Real-time sync.
- Offline mode.
- Notifications.

---

## User Stories
### Required Stories
1) **Auth**
- As a user, I sign up for an account to have a personal task list.
- As a user, I log in to access my tasks and profile.
- As a user, I log out to protect my data.

2) **Tasks**
- As a user, I create a task.
- As a user, I view all my tasks.
- As a user, I update a task title, description, or status.
- As a user, I delete a task.
- Required fields: title, optional description, priority, deadline.

3) **Labels**
- As a user, I create and manage labels such as Work, Personal, Urgent.
- As a user, I assign one or more labels to a task.

### Stretch Stories
- Filter tasks by label.
- Edit profile details.
- Responsive layout across mobile, tablet, desktop.
- Clear, helpful error messages across the app.

---

## Acceptance Criteria (samples)
Use these patterns to write tests and demo flows.

**Auth**
- Given a new user, when they submit email and strong password, then the system creates an account and starts a session.
- Given an existing user, when they log in with valid credentials, then they reach the dashboard and see their tasks list.
- Given a logged-in user, when they log out, then their session is invalid and protected routes redirect to login.

**Tasks**
- Create: when a user submits title, priority, and deadline, then the task appears at the top of the list.
- Read: when a user loads the dashboard, then tasks render with pagination or a clear empty state.
- Update: when a user edits title or status, then changes persist on refresh.
- Delete: when a user deletes a task, then it disappears and does not reappear on refresh.
- Validation: title required, priority in [High, Medium, Low], deadline is a date.

**Labels**
- Create: when a user adds “Work,” then “Work” appears in the labels list.
- Assign: when a user assigns “Work” to a task, then the task shows a “Work” chip and it persists.

**Stretch**
- Filter: when a user selects “Urgent,” then only tasks with “Urgent” show.
- Profile: when a user edits display name, then the change persists and shows on the header.
- Responsive: layout passes Lighthouse mobile viewport checks.
- Errors: API failures show concise messages with retry guidance.

---

## Technical Stack and MCPs
**Frontend**
- Next.js 14+, TypeScript, Shadcn UI components, React Query or SWR for data fetching, Zod for client validation.

**Backend**
- FastAPI, Pydantic models, Uvicorn, motor or beanie for MongoDB access, PyJWT or authlib for JWT.

**Database**
- MongoDB Atlas. Collections: `users`, `tasks`, `labels`.

**Testing**
- Playwright for E2E. Pytest for API unit tests. Vitest or Jest for small client utilities if needed.

**Deployment**
- Railway for FastAPI. Vercel for Next.js. Environment variables configured in both.

**Observability**
- Optional Sentry DSN on both tiers.

**MCPs**
- **Playwright MCP**. Run E2E suites, record traces, attach to PRs.
- **MongoDB MCP**. Seed data, run safe queries, schema checks.
- **Shadcn MCP**. Generate accessible UI scaffolds aligned with tokens.
- **Vercel MCP**. Preview deployments per PR, promote to prod.
- **Railway MCP**. Provision and deploy backend, surface logs.
- **Context7 MCP**. Provide structured prompts for routines: scaffold, generate tests, check lint, write PR body, and produce release notes.

---

## File Structure
```
repo-root/
  README.md
  LICENSE
  .editorconfig
  .gitignore
  .github/
    workflows/
      ci.yml                 # lint, type-check, tests, Playwright
      e2e.yml                # optional split job for E2E
    pull_request_template.md
  docs/
    architecture.md          # generated later by BMAD
    api-contract.md          # OpenAPI link + examples
    rubric-mapping.md        # exported table from this brief
  backend/
    app/
      api/
        v1/
          routes_auth.py
          routes_tasks.py
          routes_labels.py
      core/
        config.py
        security.py          # JWT, password hashing
        deps.py              # fastapi.Depends providers
      db/
        client.py            # Mongo connection
        repositories/
          users_repo.py
          tasks_repo.py
          labels_repo.py
      models/
        user.py              # Pydantic
        task.py
        label.py
      services/
        auth_service.py
        task_service.py
        label_service.py
      main.py                # FastAPI app
    tests/
      unit/
        test_auth.py
        test_tasks.py
      e2e/                   # optional API smoke via httpx
    pyproject.toml
    requirements.txt
    .env.example
  frontend/
    app/
      layout.tsx
      page.tsx               # dashboard or landing
      auth/
        login/page.tsx
        register/page.tsx
      tasks/
        page.tsx
        [id]/page.tsx
      labels/
        page.tsx
    components/
      ui/                    # Shadcn generated
      TaskForm.tsx
      TaskList.tsx
      LabelPicker.tsx
      EmptyState.tsx
      ErrorState.tsx
    lib/
      api.ts                 # fetch wrappers
      auth.ts                # token helpers
      validators.ts          # zod schemas
    styles/
      globals.css
    tests/
      e2e/
        auth.spec.ts
        tasks.spec.ts
        labels.spec.ts
    next.config.mjs
    package.json
    .env.local.example
```

---

## API Contract (high level)
- `POST /auth/register` → 201, `{id, email}`
- `POST /auth/login` → 200, `{access_token, expires_in}`
- `POST /auth/logout` → 204
- `GET /tasks` → 200, `Task[]`
- `POST /tasks` → 201, `Task`
- `PATCH /tasks/:id` → 200, `Task`
- `DELETE /tasks/:id` → 204
- `GET /labels` → 200, `Label[]`
- `POST /labels` → 201, `Label`
- `PATCH /labels/:id` → 200, `Label`
- `DELETE /labels/:id` → 204

**Task**
```
{
  id: string,
  title: string,
  description?: string,
  priority: "High" | "Medium" | "Low",
  deadline: string,      // ISO date
  status: "open" | "done",
  labelIds: string[],
  ownerId: string,
  createdAt: string,
  updatedAt: string
}
```

---

## Environment Configuration
**Shared**
- `MONGODB_URI`
- `JWT_SECRET`
- `JWT_EXPIRES_IN` (e.g., 3600)
- `NODE_ENV` and `ENV` for tier flags

**Backend (Railway)**
- `PORT` set by Railway
- `CORS_ORIGINS` includes the Vercel URL
- `SENTRY_DSN` optional

**Frontend (Vercel)**
- `NEXT_PUBLIC_API_URL` points at Railway URL
- `NEXT_PUBLIC_SENTRY_DSN` optional

---

## Git & GitHub Workflow
**Branching**
- `main`: production.
- `dev`: integration branch.
- Feature branches: `feat/<area>-<short-desc>`.

**Commit Messages**
- Conventional commits:
  - `feat: add task creation`
  - `fix: correct deadline parsing`
  - `test: add playwright login flow`

**Pull Requests**
- Target `dev`. One reviewer.
- CI must pass: type-check, lint, unit tests, Playwright smoke, build.
- PR template includes:
  - Problem, solution, screenshots, test plan, risk, rollout.

**Daily Rhythm**
- Push at least one meaningful commit per day.
- Keep PRs small. Merge once green.
- Auto-deploy previews on Vercel. Railway deploys on tag.

---

## Evaluation Rubric Mapping
| User Story / Area | Rubric Category | Points Impact | Evidence in Demo / Repo |
|---|---|---:|---|
| Sign up, Login, Logout | User Management | 15 | Auth screens, JWT flow, Playwright `auth.spec.ts` |
| Task CRUD + fields | Task Management | 25 | API routes, UI forms, Playwright `tasks.spec.ts` |
| Create + assign labels | Labeling System | 10 | Label UI, persistence, demo of assign flow |
| FastAPI + MongoDB | Backend & Database | 10 | Repo structure, models, services, connection health |
| Next.js + Shadcn | Frontend & UI | 10 | UI components, accessible forms, error states |
| Clear file layout | File Structure & Org | 5 | Matches structure in this brief |
| Public repo + README | Repo & README | 5 | README with setup, run, tech list, features |
| Daily commits | Commit History | 10 | Git log shows steady progress |
| Readable code | Code Readability | 5 | Naming, formatting, comments sparingly used |
| Modular code | Modularity & Efficiency | 5 | Services, repos, components, no duplication |
| Label filtering | Bonus Stretch | +2.5 | Filter UI, query param handling |
| Profile edit | Bonus Stretch | +2.5 | Profile page, PATCH user |
| Responsive design | Bonus Stretch | +2.5 | Mobile screenshots, Lighthouse |
| Error handling UX | Bonus Stretch | +2.5 | Toasts, inline errors, retry paths |

---

## Checklists
**Definition of Done**
- [ ] Story acceptance criteria pass locally.
- [ ] Unit tests added where logic branches exist.
- [ ] Playwright E2E added or updated.
- [ ] Types and lint pass.
- [ ] CI green on PR.
- [ ] Story listed in README feature list.

**Security**
- [ ] Passwords hashed with bcrypt.
- [ ] JWT signed with strong secret and expiry.
- [ ] CORS locked to known origins.
- [ ] Input validated with Pydantic/Zod.
- [ ] No secrets committed. `.env*` in `.gitignore`.

**Deploy**
- [ ] Railway URL gathered and stable.
- [ ] Vercel `NEXT_PUBLIC_API_URL` set to Railway URL.
- [ ] Health routes return 200.
- [ ] Sentry DSN set if used.

**UX**
- [ ] Empty states present.
- [ ] Loading indicators present.
- [ ] Form errors concise and actionable.
- [ ] Keyboard and screen reader checks on key flows.

---

## Testing Plan
**Playwright E2E**
- `auth.spec.ts`
  - register → redirect → dashboard
  - login → protected route access
  - logout → protected route blocked
- `tasks.spec.ts`
  - create task with required fields
  - edit title and status to done
  - delete task and assert absence
- `labels.spec.ts`
  - create label
  - assign to task
  - filter by label (stretch)

**API Unit (pytest)**
- Auth service: hash, verify, token create/verify.
- Task service: validate priority, deadlines, ownership.
- Label service: unique per user.

---

## Risks & Assumptions
**Risks**
- Mongo schema drift leads to query bugs. Mitigate with Pydantic models and repository layer tests.
- CORS and token issues break prod logins. Mitigate with explicit envs and E2E against preview URLs.
- Time crunch before 10/13. Mitigate with a strict MVP first, then stretch.

**Assumptions**
- Single-tenant per user. No orgs.
- JWT stateless sessions.
- No PII beyond email and password.
- Atlas cluster and platform accounts are provisioned.

---

## Implementation Milestones
**Week 1**
- Repo init, CI, file scaffolds, auth API, Mongo connect, basic pages.
**Week 2**
- Task CRUD end to end, labels, polishing, Playwright coverage, deploy, README and demo video.

---

## Demo Script (for the video)
1. Register and land on dashboard.
2. Create three tasks with mixed priorities and deadlines.
3. Create labels and assign to tasks.
4. Update a task status to done. Refresh to show persistence.
5. Delete a task. Refresh to confirm.
6. Log out and show protected route redirect.
7. Stretch: filter by label and show responsive layout on mobile viewport.

---

## Next Step
Clone the repo, set env files from the templates, scaffold auth and tasks, wire Playwright, and push a working MVP to Vercel and Railway. Use Context7 to keep prompts, test plans, and PR bodies consistent.
