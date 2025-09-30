# Requirements

## Functional Requirements

- **FR1:** Users can sign up for an account with email and password to have a personal task list
- **FR2:** Users can log in with valid credentials to access their tasks and profile
- **FR3:** Users can log out to protect their data and invalidate their session
- **FR4:** Users can create a task with required fields: title, priority (High/Medium/Low), and deadline
- **FR5:** Users can optionally add a description to tasks
- **FR6:** Users can view all their tasks in a list or dashboard view
- **FR7:** Users can update a task's title, description, status, priority, or deadline
- **FR8:** Users can mark tasks as done by updating their status
- **FR9:** Users can delete tasks from their list
- **FR10:** Users can create custom labels (e.g., Work, Personal, Urgent)
- **FR11:** Users can assign one or more labels to a task
- **FR12:** Users can view the list of all their labels
- **FR13:** The system validates that task title is required before creation
- **FR14:** The system validates that priority must be one of: High, Medium, or Low
- **FR15:** The system validates that deadline is a valid date format
- **FR16:** The system persists all data so changes survive page refresh
- **FR17:** The system provides clear empty states when no tasks or labels exist
- **FR18:** The system provides loading indicators during data operations
- **FR19:** The system displays concise error messages with actionable guidance on failures

## Non-Functional Requirements

- **NFR1:** Passwords must be hashed with bcrypt before storage
- **NFR2:** JWT tokens must be signed with a strong secret and include expiry time
- **NFR3:** CORS must be configured to only allow requests from known frontend origins
- **NFR4:** All user inputs must be validated using Pydantic (backend) and Zod (frontend)
- **NFR5:** API response time should be under 500ms for standard CRUD operations
- **NFR6:** The application must handle concurrent users safely with proper session management
- **NFR7:** The system must provide appropriate HTTP status codes for all API responses
- **NFR8:** MongoDB Atlas connection must use connection pooling for efficiency
- **NFR9:** No secrets or environment variables should be committed to the repository
- **NFR10:** The codebase must pass type checking (TypeScript/mypy) and linting without errors
- **NFR11:** Core user flows must have Playwright E2E test coverage
- **NFR12:** The application should be deployable to Railway (backend) and Vercel (frontend) with minimal configuration

---
