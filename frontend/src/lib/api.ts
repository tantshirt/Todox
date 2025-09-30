/**
 * API client for backend communication
 */
import type { AuthResponse, UserResponse } from "@/types/auth";
import type { Task, TaskCreate, TaskUpdate } from "@/types/task";
import type { Label, LabelCreate, LabelUpdate } from "@/types/label";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
}

export async function register(email: string, password: string): Promise<UserResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Registration failed');
  }

  return response.json();
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  return response.json();
}

// Task API functions
export async function getTasks(): Promise<Task[]> {
  const response = await fetch(`${API_BASE_URL}/tasks`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch tasks');
  }

  return response.json();
}

export async function createTask(taskData: TaskCreate): Promise<Task> {
  const response = await fetch(`${API_BASE_URL}/tasks`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create task');
  }

  return response.json();
}

export async function updateTask(taskId: string, taskData: TaskUpdate): Promise<Task> {
  const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update task');
  }

  return response.json();
}

export async function deleteTask(taskId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete task');
  }
}

// Label API functions
export async function getLabels(): Promise<Label[]> {
  const response = await fetch(`${API_BASE_URL}/labels`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch labels');
  }

  return response.json();
}

export async function createLabel(labelData: LabelCreate): Promise<Label> {
  const response = await fetch(`${API_BASE_URL}/labels`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(labelData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create label');
  }

  return response.json();
}

export async function updateLabel(labelId: string, labelData: LabelUpdate): Promise<Label> {
  const response = await fetch(`${API_BASE_URL}/labels/${labelId}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify(labelData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update label');
  }

  return response.json();
}

export async function deleteLabel(labelId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/labels/${labelId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete label');
  }
}
