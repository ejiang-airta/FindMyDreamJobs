// ✅ File: frontend/src/app/matches/page.tsx
// this page is for viewing job matches for a user:
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useUserId } from '@/hooks/useUserId'
import { BACKEND_BASE_URL }  from '@/lib/env'
import { Protected } from '@/components/Protected'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  return (
    <Protected>
      <MatchesPage />
    </Protected>
  )
}

// This component is the main page for viewing job matches.
// It fetches the matches from the backend and displays them in a card format:
function MatchesPage() {
  const [matchData, setMatchData] = useState([])
  const [error, setError] = useState('')
  
  // This function retrieves the user ID from local storage:   
  const userId = useUserId()
  if (!userId) {
    console.warn("❌ No valid user ID found.")
    setError("⚠️ You're not logged in. Please sign in.")
  return
  }
  console.log("🧠 Using global user ID:", userId)

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        const res = await fetch(`${BACKEND_BASE_URL}/matches/${userId}`)
        const data = await res.json()
  
        setMatchData(data)  // ← No transformation here
      } catch (err) {
        console.error('❌ Failed to load matches', err)
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
          {matchData.length > 0 ? (
            matchData.map((match: any) => (
              <div key={`${match.job_id}-${match.resume_id}`} className="border p-4 rounded-md">
                <p><strong>Job ID:</strong> {match.job_id}</p>
                <p><strong>Resume ID:</strong> {match.resume_id}</p>
                <p><strong>🔢 Match Score:</strong> {match.match_score_final ?? match.match_score_initial}%</p>
                <p><strong>✅ ATS Score:</strong> {match.ats_score_final ?? match.ats_score_initial}%</p>
                <p><strong>🧠 Matched Skills:</strong> {match.matched_skills || '--'}</p>
                <p><strong>📌 Missing Skills:</strong> {match.missing_skills || '--'}</p>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div className="bg-green-500 h-2.5 rounded-full" style={{ width: `${match.match_score_final || match.match_score_initial}%` }} />
              </div>
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
