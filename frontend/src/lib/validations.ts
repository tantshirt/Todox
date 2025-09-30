/**
 * Validation schemas using Zod
 */
import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("Invalid email format"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

export const registerSchema = z.object({
  email: z.string().email("Invalid email format"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;

export const createTaskSchema = z.object({
  title: z.string().min(1, "Title is required").max(200, "Title must be less than 200 characters"),
  description: z.string().optional(),
  priority: z.enum(['High', 'Medium', 'Low']),
  deadline: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Deadline must be in YYYY-MM-DD format"),
});

export type CreateTaskFormData = z.infer<typeof createTaskSchema>;
