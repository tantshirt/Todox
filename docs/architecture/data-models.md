# Data Models

## User

**Purpose:** Represents an authenticated user account with credentials and metadata

**Key Attributes:**
- `id`: ObjectId - Unique MongoDB identifier (auto-generated)
- `email`: string - User's email address (unique, required)
- `hashed_password`: string - bcrypt hashed password (required, never exposed in responses)
- `created_at`: datetime - Account creation timestamp
- `updated_at`: datetime - Last modification timestamp

### TypeScript Interface

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

### Relationships
- One-to-many with Task (one user owns many tasks)
- One-to-many with Label (one user owns many labels)

---

## Task

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

### TypeScript Interface

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

### Relationships
- Many-to-one with User (task belongs to one user)
- Many-to-many with Label (task can have multiple labels, labels can apply to multiple tasks)

---

## Label

**Purpose:** Represents a custom category/tag for organizing tasks

**Key Attributes:**
- `id`: ObjectId - Unique MongoDB identifier
- `name`: string - Label name (required, max 50 chars, unique per user)
- `owner_id`: ObjectId - Reference to User who owns this label (required)
- `created_at`: datetime - Creation timestamp

### TypeScript Interface

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

### Relationships
- Many-to-one with User (label belongs to one user)
- Many-to-many with Task (label can apply to multiple tasks)

---
