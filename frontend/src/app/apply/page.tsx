// ✅ File: frontend/src/app/apply/page.tsx
'use client'
import React from 'react'
import ApplyJob from '@/components/ApplyJob'
import { useUserId } from '@/hooks/useUserId'
import { Protected } from '@/components/Protected'


// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  return (
    <Protected>
      <ApplyPage />
    </Protected>
  )
}

function ApplyPage() {
  const userId = useUserId()
  const isWizard = typeof window !== 'undefined' && window.location.pathname.startsWith('/wizard')
  
  if (!userId) return <p>❌ No user ID found in localStorage</p>

  return <ApplyJob userId={userId} isWizard={isWizard} />
}