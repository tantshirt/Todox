/**
 * Task utility functions
 */
import type { Task } from '@/types/task';

export type DeadlineStatus = 'overdue' | 'today' | 'ok';

export function getDeadlineStatus(task: Task): DeadlineStatus {
  if (task.status === 'done') return 'ok';
  
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const deadline = new Date(task.deadline);
  deadline.setHours(0, 0, 0, 0);
  
  if (deadline < today) return 'overdue';
  if (deadline.getTime() === today.getTime()) return 'today';
  return 'ok';
}

export function getDeadlineMessage(task: Task): string {
  const status = getDeadlineStatus(task);
  
  if (status === 'overdue') {
    const today = new Date();
    const deadline = new Date(task.deadline);
    const daysOverdue = Math.floor((today.getTime() - deadline.getTime()) / (1000 * 60 * 60 * 24));
    return daysOverdue === 1 ? 'Overdue by 1 day' : `Overdue by ${daysOverdue} days`;
  }
  
  if (status === 'today') return 'Due today!';
  return '';
}
