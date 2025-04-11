// ✅ File: frontend/src/app/apply/page.tsx
'use client'

import { useSession } from 'next-auth/react'
import ApplyJob from '@/components/ApplyJob'

export default function ProtectedPage() {
  const { data: session, status } = useSession()
  const isWizard = typeof window !== 'undefined' && window.location.pathname.startsWith('/wizard')

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  const userId = localStorage.getItem('user_id')
  if (!userId) return <p>❌ No user ID found in localStorage</p>

  return <ApplyJob userId={userId} isWizard={isWizard} />
}