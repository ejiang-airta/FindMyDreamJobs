// main user dashboard page:
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import Link from 'next/link'

export default function DashboardPage() {
  const [resumes, setResumes] = useState([])
  const [matches, setMatches] = useState([])
  const [applications, setApplications] = useState([])
  const [error, setError] = useState("")

  useEffect(() => {
    fetchResumes()
    fetchMatches()
    fetchApplications()
  }, [])

  // Fetch data from the backend
  // Fetch resumes
  const fetchResumes = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/resumes")
      if (!response.ok) throw new Error("Failed to fetch resumes.")
      const data = await response.json()
      setResumes(data)
    } catch (err) {
      setError("❌ Error fetching resumes.")
    }
  }

  // Fetch matches
  const fetchMatches = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/matches")
      if (!response.ok) throw new Error("Failed to fetch matches.")
      const data = await response.json()
      setMatches(data)
    } catch (err) {
      setError("❌ Error fetching matches.")
    } finally {
      console.log("📦 Match data:", matches)
    }
  }

  // Fetch applications
  const fetchApplications = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/applications/1")
      if (!response.ok) throw new Error("Failed to fetch applications.")
      const data = await response.json()
      setApplications(data)
    } catch (err) {
      setError("❌ Error fetching applications.")
    }
  }
 
  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h1 className="text-3xl font-bold">📊 Dashboard</h1>
      <p className="text-muted-foreground text-sm">
        Manage your resumes, job matches, and applications.
      </p>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Resume Section */}
      <Card>
        <CardHeader>
          <h2 className="text-xl font-bold">📄 Your Resumes</h2>
        </CardHeader>
        <CardContent className="space-y-4">
          {resumes.length > 0 ? (
            resumes.map((resume: any) => (
              <div key={resume.id} className="border p-3 rounded-md">
                <p><strong>ID:</strong> {resume.id}</p>
                <p><strong>Uploaded:</strong> {new Date(resume.created_at).toLocaleString()}</p>
                <p><strong>ATS Score:</strong> 
                {resume.ats_score_initial !== null ? `${resume.ats_score_initial}%` : '—'} → 
                {resume.ats_score_final !== null ? `${resume.ats_score_final}%` : '—'}
                </p>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No resumes uploaded yet.</p>
          )}
          <Link href="/upload">
            <Button>📤 Upload New Resume</Button>
          </Link>
        </CardContent>
      </Card>

      {/* Job Matches Section */}
      <Card>
        <CardHeader>
          <h2 className="text-xl font-bold">🔍 Job Matches</h2>
        </CardHeader>
        <CardContent className="space-y-4">
          {matches.length > 0 ? (
            matches.map((match: any) => (
              <div key={match.id} className="border p-3 rounded-md">
                <p><strong>Job ID:</strong> {match.job_id}</p>
                <p><strong>Match Score:</strong> {match.match_score_final ?? match.match_score_initial ?? '--'}%</p>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No job matches found yet.</p>
          )}
        </CardContent>
      </Card>

      {/* Applications Tracking Section */}
      <Card>
        <CardHeader>
          <h2 className="text-xl font-bold">📋 Tracked Applications</h2>
        </CardHeader>
        <CardContent className="space-y-4">
          {applications.length > 0 ? (
            applications.map((app: any) => (
              <div key={app.application_id} className="border p-3 rounded-md">
                <p><strong>Job:</strong> {app.job_title} @ {app.company_name}</p>
                <p><strong>Status:</strong> {app.application_status}</p>
                <p><strong>Resume ID:</strong> {app.resume_id}</p>
                <p><strong>Applied On:</strong> {new Date(app.applied_date).toLocaleString()}</p>
                <a
                  href={app.application_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 underline text-sm"
                >
                  🔗 View Application
                </a>
                <Button
                  variant="outline"
                  onClick={() => {
                    const downloadUrl = `http://127.0.0.1:8000/download-resume/${app.resume_id}`
                    window.open(downloadUrl, '_blank')  // ✅ Trigger browser download
                  }}
                >
                  ⬇️ Download Resume
                </Button>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No applications tracked yet.</p>
          )}
        </CardContent>
      </Card>


      {/* Quick Actions */}
      <div className="flex space-x-4">
        <Link href="/upload">
          <Button>📤 Upload Resume</Button>
        </Link>
        <Link href="/analyze">
          <Button>📑 Analyze Job</Button>
        </Link>
        <Link href="/match">
          <Button>🔍 View Matches</Button>
        </Link>
      </div>
    </div>
  )
}
