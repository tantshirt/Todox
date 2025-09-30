'use client';

import { useState } from 'react';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/lib/auth';
import { useLabels } from '@/hooks/useLabels';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label as UILabel } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import type { Label } from '@/types/label';
import Link from 'next/link';

export default function LabelsPage() {
  const { logout } = useAuth();
  const { labels, isLoading, createLabel, updateLabel, deleteLabel } = useLabels();
  
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [editingLabel, setEditingLabel] = useState<Label | null>(null);
  const [deletingLabelId, setDeletingLabelId] = useState<string | null>(null);
  const [labelName, setLabelName] = useState('');

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!labelName.trim()) return;
    
    createLabel({ name: labelName.trim() });
    setLabelName('');
    setIsCreateOpen(false);
  };

  const handleUpdate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingLabel || !labelName.trim()) return;
    
    updateLabel({
      labelId: editingLabel.id,
      labelData: { name: labelName.trim() },
    });
    setEditingLabel(null);
    setLabelName('');
  };

  const handleDeleteConfirm = () => {
    if (deletingLabelId) {
      deleteLabel(deletingLabelId);
      setDeletingLabelId(null);
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen p-4 md:p-8 bg-slate-50 dark:bg-slate-950">
        <div className="max-w-5xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold">Labels</h1>
              <p className="text-slate-600 dark:text-slate-400 mt-1">
                Manage your custom labels for task organization
              </p>
            </div>
            <div className="flex gap-2">
              <Link href="/tasks">
                <Button variant="outline">← Tasks</Button>
              </Link>
              <Button variant="outline" onClick={logout}>
                Logout
              </Button>
            </div>
          </div>

          {/* Create Label Button */}
          <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
            <DialogTrigger asChild>
              <Button className="mb-6">+ Create Label</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create New Label</DialogTitle>
                <DialogDescription>
                  Add a new label for organizing your tasks
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleCreate} className="space-y-4">
                <div>
                  <UILabel htmlFor="label-name">Label Name</UILabel>
                  <Input
                    id="label-name"
                    value={labelName}
                    onChange={(e) => setLabelName(e.target.value)}
                    placeholder="e.g., Work, Personal, Urgent"
                    maxLength={50}
                    required
                  />
                </div>
                <div className="flex justify-end gap-2">
                  <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Create</Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>

          {/* Loading State */}
          {isLoading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900 dark:border-slate-100 mx-auto"></div>
              <p className="mt-4 text-slate-600 dark:text-slate-400">Loading labels...</p>
            </div>
          )}

          {/* Empty State */}
          {!isLoading && labels.length === 0 && (
            <Card className="text-center py-12">
              <CardHeader>
                <CardTitle>No labels yet</CardTitle>
                <CardDescription>
                  Create your first label to organize your tasks!
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button onClick={() => setIsCreateOpen(true)}>+ Create Label</Button>
              </CardContent>
            </Card>
          )}

          {/* Labels List */}
          {!isLoading && labels.length > 0 && (
            <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
              {labels.map((label) => (
                <Card key={label.id}>
                  <CardHeader className="pb-3">
                    <CardTitle className="text-lg flex items-center justify-between">
                      <Badge variant="secondary" className="text-base font-normal px-3 py-1">
                        🏷️ {label.name}
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex gap-2">
                      <Dialog 
                        open={editingLabel?.id === label.id} 
                        onOpenChange={(open) => {
                          if (!open) {
                            setEditingLabel(null);
                            setLabelName('');
                          }
                        }}
                      >
                        <Button
                          size="sm"
                          variant="outline"
                          className="flex-1"
                          onClick={() => {
                            setEditingLabel(label);
                            setLabelName(label.name);
                          }}
                        >
                          ✏️ Edit
                        </Button>
                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>Edit Label</DialogTitle>
                            <DialogDescription>
                              Update label name
                            </DialogDescription>
                          </DialogHeader>
                          <form onSubmit={handleUpdate} className="space-y-4">
                            <div>
                              <UILabel htmlFor="edit-label-name">Label Name</UILabel>
                              <Input
                                id="edit-label-name"
                                value={labelName}
                                onChange={(e) => setLabelName(e.target.value)}
                                maxLength={50}
                                required
                              />
                            </div>
                            <div className="flex justify-end gap-2">
                              <Button type="button" variant="outline" onClick={() => setEditingLabel(null)}>
                                Cancel
                              </Button>
                              <Button type="submit">Save</Button>
                            </div>
                          </form>
                        </DialogContent>
                      </Dialog>

                      <Button
                        size="sm"
                        variant="outline"
                        className="flex-1 text-red-600 hover:text-red-700"
                        onClick={() => setDeletingLabelId(label.id)}
                      >
                        🗑️ Delete
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Delete Confirmation */}
          <AlertDialog open={deletingLabelId !== null} onOpenChange={(open) => !open && setDeletingLabelId(null)}>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Delete Label?</AlertDialogTitle>
                <AlertDialogDescription>
                  This will remove the label from all tasks. This action cannot be undone.
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