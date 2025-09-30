# Epic 3: Labeling System

**Epic Goal:** Build a flexible labeling system that allows users to create custom labels and assign multiple labels to tasks, enabling better task organization and future filtering capabilities. This epic extends the core task management with powerful categorization features.

## Story 3.1: Label Model & Repository

As a developer,
I want Label data model and database repository,
so that we can persist and query label data efficiently.

**Acceptance Criteria:**

1. Label Pydantic model defined with fields: id, name, owner_id (user reference), created_at
2. Label repository class (`db/repositories/labels_repo.py`) implements methods: create_label, find_by_owner, find_by_id, update_label, delete_label
3. MongoDB collection `labels` properly indexes owner_id for efficient queries
4. Label names must be unique per user (validation prevents duplicate names for same owner)
5. Unit tests verify Label model validation and all repository methods using test database

## Story 3.2: Label CRUD APIs

As a user,
I want to create, view, update, and delete labels,
so that I can manage my custom categories for task organization.

**Acceptance Criteria:**

1. API endpoint `GET /labels` returns array of Label objects belonging to authenticated user, sorted alphabetically by name
2. API endpoint `POST /labels` accepts JSON body with name (required) and creates new label associated with authenticated user
3. Label creation enforces unique name per user (return 409 Conflict if duplicate)
4. API endpoint `PATCH /labels/:id` allows updating label name (with uniqueness validation)
5. API endpoint `DELETE /labels/:id` removes label and also removes its ID from label_ids array of all tasks
6. All endpoints require authentication and enforce ownership (return 404 for labels not owned by user)
7. Successful operations return appropriate status codes: 200 (get/update), 201 (create), 204 (delete)
8. Unit tests cover: CRUD operations, uniqueness validation, ownership verification, cascade deletion from tasks

## Story 3.3: Frontend Label Management

As a user,
I want to create and manage my labels through the UI,
so that I can set up custom categories for my tasks.

**Acceptance Criteria:**

1. Labels page created at `/labels` showing list of all user labels
2. Page requires authentication and fetches labels from `GET /labels` API
3. "Create Label" button opens form/modal with name input field
4. Label creation form calls `POST /labels` and adds new label to list on success
5. Each label in list has Edit and Delete action buttons
6. Edit button opens form pre-filled with current label name, submission calls `PATCH /labels/:id`
7. Delete button shows confirmation dialog, confirmed deletion calls `DELETE /labels/:id`
8. Empty state displays helpful message when no labels exist
9. Form validation ensures label name is required
10. Duplicate name errors display clear message
11. All actions provide loading states and success/error feedback via toasts

## Story 3.4: Assign Labels to Tasks

As a user,
I want to assign multiple labels to a task,
so that I can categorize my todos for better organization.

**Acceptance Criteria:**

1. Task edit form includes label picker component (multi-select dropdown or checkbox list)
2. Label picker fetches available labels from `GET /labels` API
3. Label picker displays current task's assigned labels as selected
4. User can select/deselect multiple labels
5. Saving task form includes updated label_ids array in `PATCH /tasks/:id` request
6. Task list view displays assigned labels as chips/badges on each task card
7. Labels are visually distinguishable (e.g., colored badges with label name)
8. Task creation form also includes label picker for assigning labels at creation time
9. Changes to task labels persist and are reflected immediately in UI

---
