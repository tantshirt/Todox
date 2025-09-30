# Epic 2: Task Management Core

**Epic Goal:** Implement complete task management functionality allowing users to create, view, update, and delete tasks with all required fields (title, description, priority, deadline). This epic delivers the core value proposition of the TODO application by enabling users to effectively manage their personal task lists.

## Story 2.1: Task Model & Repository

As a developer,
I want Task data model and database repository,
so that we can persist and query task data efficiently.

**Acceptance Criteria:**

1. Task Pydantic model defined with fields: id, title, description (optional), priority (enum: High/Medium/Low), deadline (ISO date string), status (enum: open/done), label_ids (array), owner_id (user reference), created_at, updated_at
2. Task repository class (`db/repositories/tasks_repo.py`) implements methods: create_task, find_by_owner, find_by_id, update_task, delete_task
3. MongoDB collection `tasks` properly indexes owner_id for efficient queries
4. Task model validation ensures: title required, priority is valid enum value, deadline is valid date format
5. Unit tests verify Task model validation and all repository methods using test database

## Story 2.2: Create Task API

As a user,
I want to create a new task with title, priority, and deadline,
so that I can track my todos with proper organization.

**Acceptance Criteria:**

1. API endpoint `POST /tasks` accepts JSON body with: title (required), description (optional), priority (required, enum), deadline (required, ISO date)
2. Endpoint requires authentication and associates task with authenticated user's owner_id
3. New task defaults to status "open" and empty label_ids array
4. Successful creation returns 201 status with complete Task object
5. Validation errors return 400 with clear messages for: missing title, invalid priority, invalid deadline format
6. Unit tests cover: successful creation, validation errors, authentication requirement
7. Task service module (`services/task_service.py`) implements business logic for task creation

## Story 2.3: List Tasks API

As a user,
I want to retrieve all my tasks,
so that I can see my complete task list.

**Acceptance Criteria:**

1. API endpoint `GET /tasks` returns array of Task objects belonging to authenticated user
2. Tasks are sorted by created_at descending (newest first)
3. Endpoint requires authentication and only returns tasks where owner_id matches authenticated user
4. Empty array returned if user has no tasks (not an error)
5. Response includes all task fields including label_ids
6. Successful response returns 200 status
7. Unit tests and integration tests verify: authenticated access, owner filtering, empty list handling

## Story 2.4: Update Task API

As a user,
I want to update a task's properties,
so that I can modify title, description, status, priority, or deadline as my needs change.

**Acceptance Criteria:**

1. API endpoint `PATCH /tasks/:id` accepts JSON body with any subset of: title, description, priority, deadline, status
2. Endpoint requires authentication and verifies task belongs to authenticated user (return 404 if not found or unauthorized)
3. Only provided fields are updated; omitted fields remain unchanged
4. updated_at timestamp is set to current time on update
5. Successful update returns 200 status with complete updated Task object
6. Validation errors return 400 with clear messages for invalid field values
7. Unit tests cover: partial updates, field validation, ownership verification, non-existent task handling

## Story 2.5: Delete Task API

As a user,
I want to delete a task,
so that I can remove completed or irrelevant tasks from my list.

**Acceptance Criteria:**

1. API endpoint `DELETE /tasks/:id` removes the specified task
2. Endpoint requires authentication and verifies task belongs to authenticated user (return 404 if not found or unauthorized)
3. Successful deletion returns 204 No Content status
4. Deleted task is permanently removed from database
5. Attempting to access deleted task returns 404
6. Unit tests cover: successful deletion, ownership verification, non-existent task handling

## Story 2.6: Frontend Task List View

As a user,
I want to view all my tasks in a clean, organized list,
so that I can see my todos at a glance.

**Acceptance Criteria:**

1. Dashboard/Task List page created at `/tasks` showing all user tasks
2. Page requires authentication (redirect to login if not authenticated)
3. Tasks fetched from `GET /tasks` API and displayed in list format using Shadcn components
4. Each task card/row shows: title, priority (with visual indicator), deadline, status, and action buttons
5. Tasks are sorted newest first by default
6. Empty state component displays helpful message and "Create Task" CTA when no tasks exist
7. Loading state shows skeleton loaders or spinner during initial data fetch
8. API errors display toast notification with retry option
9. Page is responsive and renders properly on mobile, tablet, and desktop viewports

## Story 2.7: Frontend Create Task Form

As a user,
I want a form to create new tasks,
so that I can quickly add todos to my list.

**Acceptance Criteria:**

1. Task creation form accessible via button on task list page (opens modal or navigates to `/tasks/new`)
2. Form includes fields: title (text input), description (textarea, optional), priority (select dropdown: High/Medium/Low), deadline (date picker)
3. Client-side validation using Zod ensures: title required, priority selected, valid deadline date before submission
4. Form submission calls `POST /tasks` API with form data
5. Successful creation shows success toast, clears form, closes modal/returns to list, and displays new task at top of list
6. Validation errors display inline with clear, actionable messages
7. API errors display toast with retry option
8. Loading state during submission (disabled submit button, spinner)
9. Form uses Shadcn UI components with proper accessibility

## Story 2.8: Frontend Update & Delete Task Actions

As a user,
I want to edit or delete tasks directly from the task list,
so that I can quickly manage my todos without extra navigation.

**Acceptance Criteria:**

1. Each task in the list has Edit and Delete action buttons
2. Edit button opens form (modal or dedicated page) pre-filled with current task data
3. Edit form allows updating: title, description, priority, deadline, status (toggle open/done)
4. Edit form submission calls `PATCH /tasks/:id` and updates task in list on success
5. Delete button shows confirmation dialog before deletion
6. Confirmed deletion calls `DELETE /tasks/:id` and removes task from list on success
7. Status toggle (checkbox or switch) directly updates task status between open/done via `PATCH /tasks/:id`
8. All actions show loading states during API calls
9. Success/error feedback provided via toasts
10. Changes persist across page refresh (verified by refetching task list)

---
