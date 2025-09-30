/**
 * Task types
 */

export type TaskPriority = 'High' | 'Medium' | 'Low';
export type TaskStatus = 'open' | 'done';

export interface Task {
  id: string;
  title: string;
  description: string | null;
  priority: TaskPriority;
  deadline: string; // ISO 8601 date
  status: TaskStatus;
  label_ids: string[];
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority: TaskPriority;
  deadline: string;
  label_ids?: string[];
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  priority?: TaskPriority;
  deadline?: string;
  status?: TaskStatus;
  label_ids?: string[];
}
