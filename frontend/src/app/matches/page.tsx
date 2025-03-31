// ✅ File: frontend/src/app/matches/page.tsx
// this page is for viewing job matches for a user:
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useSession } from 'next-auth/react'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <MatchesPage />
}

// This component is the main page for viewing job matches.
// It fetches the matches from the backend and displays them in a card format:
function MatchesPage() {
  const [matches, setMatches] = useState([])
  const [error, setError] = useState('')
  const userId = 1 // 🔐 Hardcoded until auth is added

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/matches/${userId}`)
        const data = await res.json()

        if (!res.ok) {
          throw new Error(data.detail || 'Failed to fetch matches')
        }

        setMatches(data)
      } catch (err) {
        setError('❌ Failed to load matches.')
      }
    }

    fetchMatches()
  }, [])

  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">🔍 Job Matches</h1>
      <p className="text-sm text-muted-foreground">
        View your resume-to-job matches and decide whether to optimize/apply.
      </p>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <h2 className="text-xl font-semibold">Matched Jobs</h2>
        </CardHeader>
        <CardContent className="space-y-4">
          {matches.length > 0 ? (
            matches.map((match: any) => (
              <div key={match.id} className="border p-4 rounded-md">
                <p><strong>Job ID:</strong> {match.job_id}</p>
                <p><strong>Resume ID:</strong> {match.resume_id}</p>
                <p><strong>🔢 Match Score:</strong> {match.match_score_final ?? match.match_score_initial}%</p>
                <p><strong>✅ ATS Score:</strong> {match.ats_score_final ?? match.ats_score_initial}%</p>
                <p><strong>🧠 Matched Skills:</strong> {match.matched_skills || '--'}</p>
                <p><strong>📌 Missing Skills:</strong> {match.missing_skills || '--'}</p>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No job matches found.</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
