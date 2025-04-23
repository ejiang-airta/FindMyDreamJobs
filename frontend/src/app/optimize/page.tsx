// ✅ File: src/app/optimize/page.tsx
'use client'
import React, { useEffect, useState } from 'react'
import { useSession } from 'next-auth/react'
import OptimizeResume from '@/components/OptimizeResume'
import { useUserId } from '@/hooks/useUserId'
import { Protected } from '@/components/Protected'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  return (
    <Protected>
      <OptimizePage />
    </Protected>
  )
}


function OptimizePage() {
  const userId = useUserId()
    if (!userId) return <p>❌ No user ID found</p>

  if (!userId) return <p>❌ No user ID found in localStorage</p>

  return <OptimizeResume userId={String(userId)} />
}
