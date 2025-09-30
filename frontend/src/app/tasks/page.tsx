'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/lib/auth';
import { useTasks } from '@/hooks/useTasks';
import { useLabels } from '@/hooks/useLabels';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import type { Task, TaskPriority } from '@/types/task';
import { createTaskSchema, type CreateTaskFormData } from '@/lib/validations';

export default function TasksPage() {
  const { user, logout } = useAuth();
  const { tasks, isLoading, createTask, updateTask, deleteTask } = useTasks();
  const { labels } = useLabels();
  
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTaskId, setDeletingTaskId] = useState<string | null>(null);
  
  // Create task form state
  const [formData, setFormData] = useState<CreateTaskFormData>({
    title: '',
    description: '',
    priority: 'Medium',
    deadline: new Date().toISOString().split('T')[0],
  });
  const [selectedLabels, setSelectedLabels] = useState<string[]>([]);
  const [formErrors, setFormErrors] = useState<Partial<Record<keyof CreateTaskFormData, string>>>({});

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFormErrors({});

    const result = createTaskSchema.safeParse(formData);
    if (!result.success) {
      const errors: Partial<Record<keyof CreateTaskFormData, string>> = {};
      result.error.issues.forEach((err) => {
        if (err.path[0]) {
          errors[err.path[0] as keyof CreateTaskFormData] = err.message;
        }
      });
      setFormErrors(errors);
      return;
    }

    createTask({
      title: formData.title,
      description: formData.description || undefined,
      priority: formData.priority as TaskPriority,
      deadline: formData.deadline,
      label_ids: selectedLabels,
    });

    setFormData({ title: '', description: '', priority: 'Medium', deadline: new Date().toISOString().split('T')[0] });
    setSelectedLabels([]);
    setIsCreateOpen(false);
  };

  const handleUpdateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTask) return;

    updateTask({
      taskId: editingTask.id,
      taskData: {
        title: formData.title,
        description: formData.description || undefined,
        priority: formData.priority as TaskPriority,
        deadline: formData.deadline,
        label_ids: selectedLabels,
      },
    });

    setEditingTask(null);
    setSelectedLabels([]);
  };

  const handleStatusToggle = (task: Task) => {
    updateTask({
      taskId: task.id,
      taskData: {
        status: task.status === 'open' ? 'done' : 'open',
      },
    });
  };

  const handleDeleteConfirm = () => {
    if (deletingTaskId) {
      deleteTask(deletingTaskId);
      setDeletingTaskId(null);
    }
  };

  const getPriorityColor = (priority: TaskPriority) => {
    switch (priority) {
      case 'High':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      case 'Medium':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400';
      case 'Low':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen p-4 md:p-8 bg-slate-50 dark:bg-slate-950">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold">Tasks</h1>
              <p className="text-slate-600 dark:text-slate-400 mt-1">
                Welcome, {user?.email}!
              </p>
            </div>
            <div className="flex gap-2">
              <Link href="/labels">
                <Button variant="outline">🏷️ Labels</Button>
              </Link>
              <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
                <DialogTrigger asChild>
                  <Button>+ Create Task</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Create New Task</DialogTitle>
                    <DialogDescription>
                      Add a new task with priority and deadline
                    </DialogDescription>
                  </DialogHeader>
                  <form onSubmit={handleCreateSubmit} className="space-y-4">
                    <div>
                      <Label htmlFor="title">Title</Label>
                      <Input
                        id="title"
                        value={formData.title}
                        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                        placeholder="Task title"
                      />
                      {formErrors.title && <p className="text-sm text-red-600 mt-1">{formErrors.title}</p>}
                    </div>

                    <div>
                      <Label htmlFor="description">Description (optional)</Label>
                      <Textarea
                        id="description"
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        placeholder="Task description"
                        rows={3}
                      />
                    </div>

                    <div>
                      <Label htmlFor="priority">Priority</Label>
                      <Select value={formData.priority} onValueChange={(value) => setFormData({ ...formData, priority: value as TaskPriority })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="High">High</SelectItem>
                          <SelectItem value="Medium">Medium</SelectItem>
                          <SelectItem value="Low">Low</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="deadline">Deadline</Label>
                      <Input
                        id="deadline"
                        type="date"
                        value={formData.deadline}
                        onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
                      />
                      {formErrors.deadline && <p className="text-sm text-red-600 mt-1">{formErrors.deadline}</p>}
                    </div>

                    <div>
                      <Label>Labels (optional)</Label>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {labels.map((label) => (
                          <Badge
                            key={label.id}
                            variant={selectedLabels.includes(label.id) ? "default" : "outline"}
                            className="cursor-pointer"
                            onClick={() => {
                              setSelectedLabels(prev =>
                                prev.includes(label.id)
                                  ? prev.filter(id => id !== label.id)
                                  : [...prev, label.id]
                              );
                            }}
                          >
                            {selectedLabels.includes(label.id) && '✓ '}
                            {label.name}
                          </Badge>
                        ))}
                        {labels.length === 0 && (
                          <p className="text-sm text-slate-500">No labels yet. Create labels first.</p>
                        )}
                      </div>
                    </div>

                    <div className="flex justify-end gap-2">
                      <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)}>
                        Cancel
                      </Button>
                      <Button type="submit">Create Task</Button>
                    </div>
                  </form>
                </DialogContent>
              </Dialog>

              <Button variant="outline" onClick={logout}>
                Logout
              </Button>
            </div>
          </div>

          {/* Loading State */}
          {isLoading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900 dark:border-slate-100 mx-auto"></div>
              <p className="mt-4 text-slate-600 dark:text-slate-400">Loading tasks...</p>
            </div>
          )}

          {/* Empty State */}
          {!isLoading && tasks.length === 0 && (
            <Card className="text-center py-12">
              <CardHeader>
                <CardTitle>No tasks yet</CardTitle>
                <CardDescription>
                  Create your first task to get started!
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button onClick={() => setIsCreateOpen(true)}>+ Create Task</Button>
              </CardContent>
            </Card>
          )}

          {/* Task List */}
          {!isLoading && tasks.length > 0 && (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {tasks.map((task) => (
                <Card key={task.id} className={task.status === 'done' ? 'opacity-60' : ''}>
                  <CardHeader>
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-start gap-2 flex-1">
                        <Checkbox
                          checked={task.status === 'done'}
                          onCheckedChange={() => handleStatusToggle(task)}
                          className="mt-1"
                        />
                        <div className="flex-1">
                          <CardTitle className={`text-lg ${task.status === 'done' ? 'line-through' : ''}`}>
                            {task.title}
                          </CardTitle>
                          {task.description && (
                            <CardDescription className="mt-1">
                              {task.description}
                            </CardDescription>
                          )}
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex flex-wrap gap-2">
                        <Badge className={getPriorityColor(task.priority)}>
                          {task.priority}
                        </Badge>
                        <Badge variant="outline">
                          📅 {new Date(task.deadline).toLocaleDateString()}
                        </Badge>
                        {task.label_ids && task.label_ids.map((labelId) => {
                          const label = labels.find(l => l.id === labelId);
                          return label ? (
                            <Badge key={labelId} variant="secondary">
                              🏷️ {label.name}
                            </Badge>
                          ) : null;
                        })}
                      </div>

                      <div className="flex gap-2 pt-2">
                        <Dialog open={editingTask?.id === task.id} onOpenChange={(open) => !open && setEditingTask(null)}>
                          <Button
                            size="sm"
                            variant="outline"
                            className="flex-1"
                            onClick={() => {
                              setEditingTask(task);
                              setFormData({
                                title: task.title,
                                description: task.description || '',
                                priority: task.priority,
                                deadline: task.deadline,
                              });
                              setSelectedLabels(task.label_ids || []);
                            }}
                          >
                            ✏️ Edit
                          </Button>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>Edit Task</DialogTitle>
                              <DialogDescription>
                                Update task details
                              </DialogDescription>
                            </DialogHeader>
                            <form onSubmit={handleUpdateSubmit} className="space-y-4">
                              <div>
                                <Label htmlFor="edit-title">Title</Label>
                                <Input
                                  id="edit-title"
                                  value={formData.title}
                                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                />
                              </div>

                              <div>
                                <Label htmlFor="edit-description">Description</Label>
                                <Textarea
                                  id="edit-description"
                                  value={formData.description}
                                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                  rows={3}
                                />
                              </div>

                              <div>
                                <Label htmlFor="edit-priority">Priority</Label>
                                <Select value={formData.priority} onValueChange={(value) => setFormData({ ...formData, priority: value as TaskPriority })}>
                                  <SelectTrigger>
                                    <SelectValue />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="High">High</SelectItem>
                                    <SelectItem value="Medium">Medium</SelectItem>
                                    <SelectItem value="Low">Low</SelectItem>
                                  </SelectContent>
                                </Select>
                              </div>

                              <div>
                                <Label htmlFor="edit-deadline">Deadline</Label>
                                <Input
                                  id="edit-deadline"
                                  type="date"
                                  value={formData.deadline}
                                  onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
                                />
                              </div>

                              <div>
                                <Label>Labels</Label>
                                <div className="flex flex-wrap gap-2 mt-2">
                                  {labels.map((label) => (
                                    <Badge
                                      key={label.id}
                                      variant={selectedLabels.includes(label.id) ? "default" : "outline"}
                                      className="cursor-pointer"
                                      onClick={() => {
                                        setSelectedLabels(prev =>
                                          prev.includes(label.id)
                                            ? prev.filter(id => id !== label.id)
                                            : [...prev, label.id]
                                        );
                                      }}
                                    >
                                      {selectedLabels.includes(label.id) && '✓ '}
                                      {label.name}
                                    </Badge>
                                  ))}
                                </div>
                              </div>

                              <div className="flex justify-end gap-2">
                                <Button type="button" variant="outline" onClick={() => setEditingTask(null)}>
                                  Cancel
                                </Button>
                                <Button type="submit">Save Changes</Button>
                              </div>
                            </form>
                          </DialogContent>
                        </Dialog>

                        <Button
                          size="sm"
                          variant="outline"
                          className="flex-1 text-red-600 hover:text-red-700"
                          onClick={() => setDeletingTaskId(task.id)}
                        >
                          🗑️ Delete
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Delete Confirmation Dialog */}
          <AlertDialog open={deletingTaskId !== null} onOpenChange={(open) => !open && setDeletingTaskId(null)}>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Delete Task?</AlertDialogTitle>
                <AlertDialogDescription>
                  This action cannot be undone. The task will be permanently deleted.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction onClick={handleDeleteConfirm} className="bg-red-600 hover:bg-red-700">
                  Delete
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </div>
    </ProtectedRoute>
  );
}