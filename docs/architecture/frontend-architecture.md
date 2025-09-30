# Frontend Architecture

## Component Architecture

### Component Organization

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

### Component Template

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

## State Management Architecture

### State Structure

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

### State Management Patterns

- **Server State:** React Query for all API data (tasks, labels, user info)
- **Client State:** React hooks (useState, useReducer) for UI state (modals, forms)
- **Auth State:** Context API for authentication state shared across app
- **Form State:** Controlled components with Zod validation
- **Optimistic Updates:** React Query optimistic updates for status toggles
- **Cache Invalidation:** Automatic refetch on window focus for fresh data

## Routing Architecture

### Route Organization

```
/ (root)
├── /auth
│   ├── /login              # Public route - Login page
│   └── /register           # Public route - Registration page
├── /tasks                  # Protected - Task dashboard (main view)
└── /labels                 # Protected - Label management

Protected routes automatically redirect to /auth/login if not authenticated
```

### Protected Route Pattern

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

## Frontend Services Layer

### API Client Setup

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

### Service Example

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
