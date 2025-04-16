// ✅ File: frontend/src/app/finalize/page.tsx
// Lets users approve & download, and submit the application
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Label } from '@/components/ui/label'
import { useSession } from 'next-auth/react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { BACKEND_BASE_URL }  from '@/lib/env'
import { useUserId } from '@/hooks/useUserId'


// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()
  
    if (status === "loading") return <p>Loading...</p>
    if (!session?.user) return <p>Unauthorized</p>
  
    const userId = useUserId()
    if (!userId) return <p>❌ No user ID found</p>

  return <FinalizePage userId={String(userId)} />
}

// This component is the main page for finalizing resumes and submitting applications:
// It allows users to input a resume ID, fetch its optimized text, approve it, and log the job application.
function FinalizePage({ userId }: { userId: string }) {
  const [resumes, setResumes] = useState<any[]>([])
  const [jobs, setJobs] = useState<any[]>([])
  const [resumeId, setResumeId] = useState('')
  const [jobId, setJobId] = useState('')
  const [optimizedText, setOptimizedText] = useState('')
  const [applicationUrl, setApplicationUrl] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  // Fetch resumes and jobs for the dropdowns:
  useEffect(() => {
    const fetchDropdowns = async () => {
      try {
        const [res1, res2] = await Promise.all([
          fetch(`${BACKEND_BASE_URL}/resumes/by-user/${userId}`),
          fetch(`${BACKEND_BASE_URL}/jobs/all`)
        ])
        if (res1.ok) setResumes(await res1.json())
        if (res2.ok) setJobs(await res2.json())
      } catch (err) {
        console.error("❌ Error loading options:", err)
      }
    }

    fetchDropdowns()
  }, [userId])

  const handleFetch = async () => {
  
    if (!resumeId) {
      setError('⚠️ Resume is required.')
      return
    }
  
    try {
      const response = await fetch(`${BACKEND_BASE_URL}/resumes/${resumeId}`)  // Adjust this route as needed
      const data = await response.json()
  
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to fetch resume')
      }
  
      setOptimizedText(data.optimized_text || 'No optimized text found.')
      setMessage('')
      setError('')
    } catch (err) {
      console.error('Fetch Error:', err)
      setError('❌ Could not fetch optimized resume')
    }
  }  

  const handleApprove = async () => {
    try {
      const res = await fetch(`${BACKEND_BASE_URL}/approve-resume`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_id: parseInt(resumeId) })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Approval failed')
      setMessage('✅ Resume approved!')
      setError('')
    } catch (err) {
      setError('❌ Approval failed')
    }
  }

  const handleSubmit = async () => {
    if (!resumeId || !jobId || !applicationUrl) {
      setError('⚠️ All fields are required to submit.')
      return
    }

    try {
      const res = await fetch(`${BACKEND_BASE_URL}/submit-application`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: parseInt(resumeId),
          job_id: parseInt(jobId),
          application_url: applicationUrl
        })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Application failed')
      setMessage('🚀 Application logged successfully!')
      setError('')
    } catch (err) {
      setError('❌ Application failed')
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">🧾 Final Resume Review</h1>
      <p className="text-muted-foreground text-sm">
        Check your optimized resume below, approve it, and log the job application.
      </p>

      <Card>
        <CardContent className="p-6 space-y-4">
        <Label>Select Resume</Label>
          <Select onValueChange={setResumeId}>
            <SelectTrigger>
              <SelectValue placeholder="Choose your resume" />
            </SelectTrigger>
            <SelectContent>
              {resumes.map(r => (
                <SelectItem key={r.id} value={String(r.id)}>
                  Resume #{r.id} – {r.resume_name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Label>Select Job</Label>
          <Select onValueChange={setJobId}>
            <SelectTrigger>
              <SelectValue placeholder="Choose a job" />
            </SelectTrigger>
            <SelectContent>
              {jobs.map(j => (
                <SelectItem key={j.id} value={String(j.id)}>
                  Job #{j.id} – {j.job_title} @ {j.company_name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Button onClick={handleFetch}>📄 Load Optimized Resume</Button>

          {optimizedText && (
            <pre className="bg-muted p-4 rounded whitespace-pre-wrap max-h-96 overflow-auto text-sm">
              {optimizedText}
            </pre>
          )}

          <Button onClick={handleApprove} variant="secondary">
            ✅ Approve Resume
          </Button>

          <Label>Application URL</Label>
          <Input
            type="url"
            value={applicationUrl}
            onChange={(e) => setApplicationUrl(e.target.value)}
            placeholder="https://company.com/job/apply"
          />

          <Button onClick={handleSubmit}>📩 Submit Application</Button>

          {message && (
            <Alert variant="default">
              <AlertDescription>{message}</AlertDescription>
            </Alert>
          )}

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
