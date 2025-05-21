// ✅ File: frontend/src/app/login/reset-password/page.tsx
// ✅ This page allows users to set a new password after clicking the link in their email
'use client'

import { Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { toast } from 'sonner'
import { BACKEND_BASE_URL } from '@/lib/env'
//import { PasswordInput } from '@/components/ui/PasswordInput'


// ✅ Page must be default export
export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ResetPasswordForm />
    </Suspense>
  )
}

// ✅ Actual logic moved here
function ResetPasswordForm() {
  const searchParams = useSearchParams()
  const token = searchParams?.get('token') ?? ''
  const router = useRouter()
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleReset = async () => {
    if (!token) return toast.error('Missing reset token.', { icon: '❌' })
    if (password.length < 8) return toast.error('Password must be at least 8 characters.', { icon: '❌' })
    if (password !== confirm) return toast.error("Passwords don't match.", { icon: '❌' })

    setIsSubmitting(true)
    try {
      const res = await fetch(`${BACKEND_BASE_URL}/auth/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: password }),
      })

      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Something went wrong.')

      toast.success('Password reset successful!', { icon: '✅' })
      router.push('/login')
    } catch (err: any) {
      toast.error(err.message, { icon: '❌' })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-20 space-y-4">
      <h1 className="text-2xl font-bold text-center">Set a New Password</h1>
      
      {/*<PasswordInput placeholder="New password" name="password" required /> */}
      <Input
        type="password"
        placeholder="New password"
        name="password" 
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Input
        type="password"
        placeholder="Confirm password"
        name="password" 
        value={confirm}
        onChange={(e) => setConfirm(e.target.value)}
      />
      <Button className="w-full" onClick={handleReset} disabled={isSubmitting}>
        {isSubmitting ? 'Resetting...' : 'Reset Password'}
      </Button>
    </div>
  )
}
