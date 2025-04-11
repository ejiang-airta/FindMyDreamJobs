// ✅ File: src/app/optimize/page.tsx
'use client'

import { useSession } from 'next-auth/react'
import OptimizeResume from '@/components/OptimizeResume'

export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  const userId = localStorage.getItem('user_id')
  if (!userId) return <p>❌ No user ID found in localStorage</p>

  return <OptimizeResume userId={userId} />
}
