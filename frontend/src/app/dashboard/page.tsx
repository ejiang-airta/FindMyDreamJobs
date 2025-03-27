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
  const [error, setError] = useState("")

  useEffect(() => {
    fetchResumes()
    fetchMatches()
  }, [])

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

  const fetchMatches = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/matches")
      if (!response.ok) throw new Error("Failed to fetch matches.")
      const data = await response.json()
      setMatches(data)
    } catch (err) {
      setError("❌ Error fetching matches.")
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
                <p><strong>Match Score:</strong> {match.match_score}%</p>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No job matches found yet.</p>
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
