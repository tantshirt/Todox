/**
 * Label management hook using React Query
 */
'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import type { LabelCreate, LabelUpdate } from '@/types/label';
import * as api from '@/lib/api';

export function useLabels() {
  const queryClient = useQueryClient();

  const { data: labels = [], isLoading } = useQuery({
    queryKey: ['labels'],
    queryFn: api.getLabels,
  });

  const createLabel = useMutation({
    mutationFn: (labelData: LabelCreate) => api.createLabel(labelData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labels'] });
      toast.success('Label created successfully!');
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to create label');
    },
  });

  const updateLabel = useMutation({
    mutationFn: ({ labelId, labelData }: { labelId: string; labelData: LabelUpdate }) =>
      api.updateLabel(labelId, labelData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labels'] });
      toast.success('Label updated successfully!');
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to update label');
    },
  });

  const deleteLabel = useMutation({
    mutationFn: (labelId: string) => api.deleteLabel(labelId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['labels'] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] }); // Refresh tasks too
      toast.success('Label deleted successfully!');
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to delete label');
    },
  });

  return {
    labels,
    isLoading,
    createLabel: createLabel.mutate,
    updateLabel: updateLabel.mutate,
    deleteLabel: deleteLabel.mutate,
  };
}
