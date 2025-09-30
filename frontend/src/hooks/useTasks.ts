/**
 * Task management hook using React Query
 */
'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import type { TaskCreate, TaskUpdate } from '@/types/task';
import * as api from '@/lib/api';

export function useTasks() {
  const queryClient = useQueryClient();

  // Fetch all tasks
  const { data: tasks = [], isLoading, error } = useQuery({
    queryKey: ['tasks'],
    queryFn: api.getTasks,
  });

  // Create task mutation
  const createTask = useMutation({
    mutationFn: (taskData: TaskCreate) => api.createTask(taskData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      toast.success('Task created successfully!');
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to create task');
    },
  });

  // Update task mutation
  const updateTask = useMutation({
    mutationFn: ({ taskId, taskData }: { taskId: string; taskData: TaskUpdate }) =>
      api.updateTask(taskId, taskData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      toast.success('Task updated successfully!');
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to update task');
    },
  });

  // Delete task mutation
  const deleteTask = useMutation({
    mutationFn: (taskId: string) => api.deleteTask(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      toast.success('Task deleted successfully!');
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to delete task');
    },
  });

  return {
    tasks,
    isLoading,
    error,
    createTask: createTask.mutate,
    updateTask: updateTask.mutate,
    deleteTask: deleteTask.mutate,
    isCreating: createTask.isPending,
    isUpdating: updateTask.isPending,
    isDeleting: deleteTask.isPending,
  };
}
