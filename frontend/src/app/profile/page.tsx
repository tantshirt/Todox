'use client';

import { useState } from 'react';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import * as api from '@/lib/api';

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    email: user?.email || '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validate passwords match if changing password
    if (formData.newPassword) {
      if (formData.newPassword.length < 8) {
        setErrors({ newPassword: 'Password must be at least 8 characters' });
        return;
      }
      if (formData.newPassword !== formData.confirmPassword) {
        setErrors({ confirmPassword: 'Passwords do not match' });
        return;
      }
      if (!formData.currentPassword) {
        setErrors({ currentPassword: 'Current password is required to change password' });
        return;
      }

      try {
        await api.updatePassword(formData.currentPassword, formData.newPassword);
        toast.success('Password updated successfully!');
        setIsEditing(false);
        setFormData({ ...formData, currentPassword: '', newPassword: '', confirmPassword: '' });
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to update password';
        toast.error(errorMessage);
        if (errorMessage.includes('incorrect')) {
          setErrors({ currentPassword: 'Current password is incorrect' });
        }
      }
    } else {
      // No password change, just close edit mode
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setFormData({
      email: user?.email || '',
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
    });
    setErrors({});
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen p-4 md:p-8 bg-slate-50 dark:bg-slate-950">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold">Profile</h1>
              <p className="text-slate-600 dark:text-slate-400 mt-1">
                Manage your account settings
              </p>
            </div>
            <Button variant="outline" onClick={() => router.push('/tasks')}>
              ← Back to Tasks
            </Button>
          </div>

          {/* Profile Information Card */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Account Information</CardTitle>
              <CardDescription>
                View and update your profile details
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Email (Read-only for now) */}
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    disabled={!isEditing}
                    className="bg-slate-100 dark:bg-slate-900"
                    title="Email cannot be changed"
                  />
                  <p className="text-xs text-slate-500 mt-1">
                    Email address cannot be changed
                  </p>
                </div>

                {/* User ID Display */}
                <div>
                  <Label>User ID</Label>
                  <Input
                    value={user?.id || 'Loading...'}
                    disabled
                    className="bg-slate-100 dark:bg-slate-900 font-mono text-sm"
                  />
                </div>

                {/* Account Created */}
                <div>
                  <Label>Member Since</Label>
                  <Input
                    value={user?.created_at ? new Date(user.created_at).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    }) : 'Loading...'}
                    disabled
                    className="bg-slate-100 dark:bg-slate-900"
                  />
                </div>

                {/* Password Change Section */}
                {isEditing && (
                  <>
                    <div className="border-t pt-4 mt-4">
                      <h3 className="text-lg font-semibold mb-4">Change Password</h3>
                      
                      <div className="space-y-4">
                        <div>
                          <Label htmlFor="currentPassword">Current Password</Label>
                          <Input
                            id="currentPassword"
                            type="password"
                            value={formData.currentPassword}
                            onChange={(e) => setFormData({ ...formData, currentPassword: e.target.value })}
                            placeholder="Enter current password"
                          />
                          {errors.currentPassword && (
                            <p className="text-sm text-red-600 mt-1">{errors.currentPassword}</p>
                          )}
                        </div>

                        <div>
                          <Label htmlFor="newPassword">New Password</Label>
                          <Input
                            id="newPassword"
                            type="password"
                            value={formData.newPassword}
                            onChange={(e) => setFormData({ ...formData, newPassword: e.target.value })}
                            placeholder="At least 8 characters"
                          />
                          {errors.newPassword && (
                            <p className="text-sm text-red-600 mt-1">{errors.newPassword}</p>
                          )}
                          <p className="text-xs text-slate-500 mt-1">
                            Leave blank to keep current password
                          </p>
                        </div>

                        <div>
                          <Label htmlFor="confirmPassword">Confirm New Password</Label>
                          <Input
                            id="confirmPassword"
                            type="password"
                            value={formData.confirmPassword}
                            onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                            placeholder="Re-enter new password"
                          />
                          {errors.confirmPassword && (
                            <p className="text-sm text-red-600 mt-1">{errors.confirmPassword}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </>
                )}

                {/* Action Buttons */}
                <div className="flex justify-end gap-2 pt-4">
                  {!isEditing ? (
                    <Button type="button" onClick={() => setIsEditing(true)}>
                      Edit Profile
                    </Button>
                  ) : (
                    <>
                      <Button type="button" variant="outline" onClick={handleCancel}>
                        Cancel
                      </Button>
                      <Button type="submit">
                        Save Changes
                      </Button>
                    </>
                  )}
                </div>
              </form>
            </CardContent>
          </Card>

          {/* Danger Zone */}
          <Card className="border-red-200 dark:border-red-900">
            <CardHeader>
              <CardTitle className="text-red-600 dark:text-red-400">Danger Zone</CardTitle>
              <CardDescription>
                Irreversible account actions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-semibold">Logout from all devices</p>
                  <p className="text-sm text-slate-500">Clear your session and return to login</p>
                </div>
                <Button variant="destructive" onClick={logout}>
                  Logout
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </ProtectedRoute>
  );
}

