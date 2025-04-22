//✅ File: frontend/src/app/dashboard/page.tsx
// This file is the main dashboard page for the user.
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { AppButton } from '@/components/ui/AppButton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import Link from 'next/link'
import { useSession } from 'next-auth/react'
import { useUserId } from '@/hooks/useUserId'
import { BACKEND_BASE_URL }  from '@/lib/env'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please log in.</p>

  return <DashboardPage />
}

// This component is the main page for the user dashboard.
// It displays the user's resumes, job matches, and applications:
function DashboardPage() {
  const userId = useUserId()
  const [resumes, setResumes] = useState([])
  const [matches, setMatches] = useState([])
  const [applications, setApplications] = useState([])
  const [error, setError] = useState('')
 
  // ✅ Wait for localStorage hydration + validate session user email
  useEffect(() => {
    if (!userId) return

    Promise.all([
      fetch(`${BACKEND_BASE_URL}/resumes/by-user/${userId}`),
      fetch(`${BACKEND_BASE_URL}/matches/${userId}`),
      fetch(`${BACKEND_BASE_URL}/applications/${userId}`)
    ])
      .then(async ([resumeRes, matchRes, appRes]) => {
        const resumeData = resumeRes.ok ? await resumeRes.json() : []
        const matchData = matchRes.ok ? await matchRes.json() : []
        const appData = appRes.ok ? await appRes.json() : []

        setResumes(resumeData)
        setMatches(matchData)
        setApplications(appData)


        if (
          resumeData.length === 0 &&
          matchData.length === 0 &&
          appData.length === 0
        ) {
          setError("No data available yet — upload your first resume to get started.")
        }
      })
      .catch((err) => {
        console.error("Error fetching data:", err)
        setError("❌ Error fetching dashboard data.")
      })
  }, [userId])

  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h1 className="text-3xl font-bold">📊 Dashboard</h1>
      {error && (
        <Alert variant="default">
          <AlertDescription>
          ℹ️ {error}
          </AlertDescription>
        </Alert>
      )}

      {/* Display resumes, matches, applications */}
      {/* ✅ Resumes */}
      <Card>
        <CardHeader><h2 className="text-xl font-bold">📄 Your Resumes</h2></CardHeader>
        <CardContent className="space-y-4">
          {resumes.length > 0 ? (
            resumes.map((r: any) => (
              <div key={r.id} className="border p-3 rounded-md">
                <p><strong>Resume #{r.id}:</strong> {r.resume_name}</p>
                <p><strong>Uploaded:</strong> {new Date(r.created_at).toLocaleString()}</p>
                {r.ats_score_initial != null && (r.ats_score_final == null || r.ats_score_final === 0) && (
                  <p><strong>ATS Score:</strong> {r.ats_score_initial}% (initial)</p>
                )}

                {r.ats_score_initial != null && r.ats_score_final != null && r.ats_score_final > 0 && (
                  <p>
                    <strong>ATS Score:</strong> {r.ats_score_initial}% (initial) → {r.ats_score_final}% (latest)
                  </p>
                )}
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No resumes uploaded yet. Click on Resume tab to get started.</p>
          )}
          <Link href="/upload"><AppButton>📤 Upload New Resume</AppButton></Link>
        </CardContent>
      </Card>

      {/* ✅ Matches */}
      <Card>
        <CardHeader><h2 className="text-xl font-bold">🔍 Job Matches</h2></CardHeader>
        <CardContent className="space-y-4">
          {matches.length > 0 ? (
            matches.map((match: any) => (
              <div key={`match-${match.job_id}-${match.resume_id}`} className="border p-3 rounded-md">
                <p><strong>Job #{match.job_id}:</strong> {match.job_title} - {match.company_name}</p>
                <p><strong>Match Score:</strong> {match.match_score_final ?? match.match_score_initial ?? '--'}%</p>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No job matches found yet.</p>
          )}
        </CardContent>
      </Card>

      {/* ✅ Applications */}
      <Card>
        <CardHeader><h2 className="text-xl font-bold">📋 Tracked Applications</h2></CardHeader>
        <CardContent className="space-y-4">
          {applications.length > 0 ? (
            applications.map((app: any) => (
              <div key={`app-${app.application_id}`} className="border p-3 rounded-md">
                <p><strong>Job #{app.application_id}:</strong> {app.job_title} @ {app.company_name}</p>
                <p><strong>Status:</strong> {app.application_status}</p>
                <p><strong>Resume #{app.resume_id}:</strong> {app.resume_name || 'Unnamed'}</p>
                <p><strong>Applied On:</strong> {new Date(app.applied_date).toLocaleString()}</p>
                <a href={app.application_url} target="_blank" className="text-blue-600 underline text-sm">🔗 View Application</a>
                <AppButton variant="outline" onClick={() => window.open(`${BACKEND_BASE_URL}/download-resume/${app.resume_id}`, '_blank')}>
                  ⬇️ Download Resume
                </AppButton>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No applications tracked yet.</p>
          )}
        </CardContent>
      </Card>

      {/* ✅ Quick Links */}
      <div className="flex space-x-4">
        <Link href="/upload"><AppButton>📤 Upload Resume</AppButton></Link>
        <Link href="/analyze"><AppButton>📑 Analyze Job</AppButton></Link>
        <Link href="/match"><AppButton>🔍 View Matches</AppButton></Link>
      </div>
    </div>
  )
}