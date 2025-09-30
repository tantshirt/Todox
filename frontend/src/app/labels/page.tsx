'use client';

import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/button';

export default function LabelsPage() {
  const { logout } = useAuth();

  return (
    <ProtectedRoute>
      <div className="min-h-screen p-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold">Labels</h1>
            <Button variant="outline" onClick={logout}>
              Logout
            </Button>
          </div>
          <p className="text-slate-600 dark:text-slate-400">
            Label management functionality will be implemented in Epic 3.
          </p>
        </div>
      </div>
    </ProtectedRoute>
  );
}
