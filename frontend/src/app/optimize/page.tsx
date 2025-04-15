// ✅ File: src/app/optimize/page.tsx
'use client'
import React, { useEffect, useState } from 'react'
import { useSession } from 'next-auth/react'
import OptimizeResume from '@/components/OptimizeResume'
import { getUserId } from '@/lib/auth'

export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  const userId = getUserId()
    if (!userId) return <p>❌ No user ID found</p>

  if (!userId) return <p>❌ No user ID found in localStorage</p>

  return <OptimizeResume userId={String(userId)} />
}
