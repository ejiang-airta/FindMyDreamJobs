// ✅ File: frontend/src/app/jobs/page.tsx
// This page is for displaying matched jobs:
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import Link from 'next/link'
import { useSession } from 'next-auth/react'


// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <JobsPage />
}

// This component is the main page for displaying matched jobs.
// It fetches the matched jobs from the backend and allows the user to optimize and apply for each job.
function JobsPage() {
  const [matches, setMatches] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    fetchMatches()
  }, [])

  const fetchMatches = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/matches")
      const data = await res.json()

      if (!res.ok) throw new Error(data.detail || 'Failed to fetch matches')
      setMatches(data)
    } catch (err) {
      console.error(err)
      setError('❌ Failed to load job matches.')
    }
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">🧳 Matched Jobs</h1>
      <p className="text-muted-foreground text-sm">
        Here are the jobs we matched your resume with. You can optimize and apply from here.
      </p>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <h2 className="text-xl font-bold">🎯 Matches</h2>
        </CardHeader>
        <CardContent className="space-y-4">
          {matches.length > 0 ? (
            matches.map((match: any) => (
              <div key={match.id} className="border p-4 rounded-md">
                <p><strong>🏢 Job ID:</strong> {match.job_id}</p>
                <p><strong>📄 Resume ID:</strong> {match.resume_id}</p>
                <p><strong>✅ Match Score:</strong> {match.match_score_final ?? match.match_score_initial}%</p>
                <p><strong>🧠 ATS Score:</strong> {match.ats_score_final ?? match.ats_score_initial}%</p>
                <div className="flex space-x-4 mt-2">
                  <Link href="/optimize">
                    <Button size="sm">✨ Optimize</Button>
                  </Link>
                  <Link href="/apply">
                    <Button variant="outline" size="sm">📩 Apply</Button>
                  </Link>
                </div>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No matched jobs found.</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
