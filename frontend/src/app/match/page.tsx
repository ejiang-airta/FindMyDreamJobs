// File: src/app/match/page.tsx
// This page is for comparing resumes with job descriptions to calculate match and ATS scores.
// It fetches the resumes and jobs from the backend and allows the user to select a resume and a job to compare.
//
// ✅ File: frontend/src/app/match/page.tsx
'use client'

import MatchScore from '@/components/MatchScore'
import { useSession } from 'next-auth/react'
import { useUserId } from '@/hooks/useUserId'
import { useEffect } from 'react'

export default function MatchPageProtected() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session?.user) return <p>Unauthorized. Please log in.</p>

  return <MatchPage />
}

function MatchPage() {
  const userId = useUserId()

  useEffect(() => {
    if (!userId) return  // wait for hydration
  }, [userId])

  return (
    <div className="max-w-3xl mx-auto mt-10 px-4">
      <h1 className="text-2xl font-bold mb-4">📊 Match Score</h1>
      <MatchScore isWizard={false} userId={userId} />
    </div>
  )
}
