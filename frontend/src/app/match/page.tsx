// File: src/app/match/page.tsx
// This page is for comparing resumes with job descriptions to calculate match and ATS scores.
// It fetches the resumes and jobs from the backend and allows the user to select a resume and a job to compare.
//
'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useSession } from "next-auth/react"
//import MatchPage from "./MatchPage"


export default function MatchPageProtected() {
  const { data: session, status } = useSession()

  if (status === "loading") return <p>Loading...</p>
  if (!session?.user) return <p>Unauthorized</p>

  const user = session.user // no TypeScript warning now!

  const userId = typeof window !== "undefined" ? localStorage.getItem("user_id") : ""
  return <MatchPage userId={userId} />

}

function MatchPage({ userId }: { userId: string }) {
  const [resumeId, setResumeId] = useState('')
  const [jobId, setJobId] = useState('')
  const [resumes, setResumes] = useState<any[]>([])
  const [jobs, setJobs] = useState<any[]>([])
  const [matchScore, setMatchScore] = useState<number | null>(null)
  const [atsScore, setAtsScore] = useState<number | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    const userId = localStorage.getItem("user_id")
    if (!userId) return
  
    const fetchData = async () => {
      try {
        const res1 = await fetch(`http://127.0.0.1:8000/resumes/by-user/${userId}`)
        const res2 = await fetch(`http://127.0.0.1:8000/jobs/all`) // <-- we fixed this earlier
        if (res1.ok) setResumes(await res1.json())
        if (res2.ok) setJobs(await res2.json())
      } catch (err) {
        console.error('Failed to load dropdown data:', err)
      }
    }
  
    fetchData()
  }, [])
  
  

  const handleMatch = async () => {
    setError('')
    setMatchScore(null)
    setAtsScore(null)

    if (!resumeId || !jobId) {
      setError('Please select both resume and job.')
      return
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/match-score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_id: parseInt(resumeId), job_id: parseInt(jobId) })
      })

      const data = await response.json()
      if (response.ok) {
        setMatchScore(data.match_score || data.match_score_initial)
        setAtsScore(data.ats_score || data.ats_score_initial)
      } else {
        setError(data.detail || 'Match failed.')
      }
    } catch (err) {
      setError('Unexpected error occurred.')
      console.error(err)
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto px-4 sm:px-6 md:px-8 mt-10 space-y-6">
      <h1 className="text-2xl font-bold">📊 Resume/Job Match</h1>
      <p className="text-muted-foreground text-sm">Compare your resume with a job description to calculate match & ATS scores.</p>

      <Card>
         <CardContent className="space-y-6 p-4 sm:p-6">
          <div>
            <Label>Select Resume</Label>
            <Select onValueChange={setResumeId}>
              <SelectTrigger>
                <SelectValue placeholder="Choose your resume" />
              </SelectTrigger>
              <SelectContent>
                {resumes.map(r => (
                  <SelectItem key={r.id} value={String(r.id)}>
                    {`Resume #${r.id}`} - {r.resume_name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label>Select Job</Label>
            <Select onValueChange={setJobId}>
              <SelectTrigger>
                <SelectValue placeholder="Choose a job description" />
              </SelectTrigger>
              <SelectContent>
                {jobs.map(j => (
                  <SelectItem key={j.id} value={String(j.id)}>
                    {`Job #${j.id}`} – {j.company_name ? `${j.job_title} - ${j.company_name || 'Unknown'}` : 'Unknown'}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <Button onClick={handleMatch} className="w-full">✨ Run Match</Button>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {(matchScore !== null || atsScore !== null) && (
            <Alert>
              <AlertDescription className="space-y-1 text-sm">
                {matchScore !== null && (
                  <div>
                    ✅ <strong>Match Score:</strong> {matchScore.toFixed(2)}%
                  </div>
                )}
                {atsScore !== null && (
                  <div>
                    ✅ <strong>ATS Score:</strong> {atsScore.toFixed(2)}%
                  </div>
                )}
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
