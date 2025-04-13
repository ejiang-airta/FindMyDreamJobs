// ✅ File: src/app/optimize/page.tsx
'use client'
import React, { useEffect, useState } from 'react'
import { useSession } from 'next-auth/react'
import OptimizeResume from '@/components/OptimizeResume'

export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  const [userId, setUserId] = useState<string | null>(null)

  useEffect(() => {
    // Only runs in the browser
    const id = localStorage.getItem('user_id')
    setUserId(id)
  }, [])
  if (!userId) return <p>❌ No user ID found in localStorage</p>

  return <OptimizeResume userId={userId} />
}
