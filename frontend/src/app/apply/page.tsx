// ✅ File: frontend/src/app/apply/page.tsx
'use client'
import React, { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import ApplyJob from '@/components/ApplyJob'

export default function ProtectedPage() {
  const { data: session, status } = useSession()
  const isWizard = typeof window !== 'undefined' && window.location.pathname.startsWith('/wizard')

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  const [userId, setUserId] = useState<string | null>(null)
  
  useEffect(() => {
    // Only runs in the browser
    const id = localStorage.getItem('user_id')
    setUserId(id)
  }, [])
  if (!userId) return <p>❌ No user ID found in localStorage</p>

  return <ApplyJob userId={userId} isWizard={isWizard} />
}