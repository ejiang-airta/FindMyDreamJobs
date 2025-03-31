// ✅ File: frontend/src/app/match/page.tsx
// This page is for displaying the job match score for a specific resume-to-job match score (usually used during matching a JD and Resume)..
'use client'

import MatchScore from '@/components/MatchScore'
import { useSession } from 'next-auth/react'
import React from 'react'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <MatchPage />
}

// This component is the main page for displaying the job match score.
// It uses the MatchScore component to show the score based on the user's resume and job description:
function MatchPage() {
  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold">🔍 Job Match Score</h1>
      <MatchScore />
    </div>
  )
}
