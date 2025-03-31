//✅ File: frontend/src/app/analyze/page.tsx
// This page is for analyzing job descriptions and resumes.
'use client'
import JobInput from '@/components/JobInput'
import { useSession } from 'next-auth/react'
import React from 'react'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <AnalyzePage />
}

// This component is the main page for analyzing job descriptions and resumes.
function AnalyzePage() {
  return (
    <main className="flex justify-center items-center h-screen">
      <JobInput />
    </main>
  )
}
