// ✅ File: frontend/src/app/finalize/page.tsx
// Lets users approve & download, and submit the application
'use client'

import React, { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Label } from '@/components/ui/label'

export default function FinalizePage() {
  const [resumeId, setResumeId] = useState('')
  const [jobId, setJobId] = useState('')
  const [optimizedText, setOptimizedText] = useState('')
  const [applicationUrl, setApplicationUrl] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleFetch = async () => {
    setError('')
    setOptimizedText('')
  
    if (!resumeId) {
      setError('⚠️ Resume ID is required.')
      return
    }
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/resumes/${resumeId}`)  // Adjust this route as needed
      const data = await response.json()
  
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to fetch resume')
      }
  
      setOptimizedText(data.optimized_text || 'No optimized text found.')
    } catch (err) {
      console.error('Fetch Error:', err)
      setError('❌ Could not fetch optimized resume')
    }
  }  

  const handleApprove = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/approve-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_id: parseInt(resumeId) })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Approval failed')
      setMessage('✅ Resume approved!')
    } catch (err) {
      setError('❌ Approval failed')
    }
  }

  const handleSubmit = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/submit-application', {
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
          <Label>Resume ID</Label>
          <Input
            type="number"
            value={resumeId}
            onChange={(e) => setResumeId(e.target.value)}
            placeholder="e.g., 6"
          />

          <Label>Job ID</Label>
          <Input
            type="number"
            value={jobId}
            onChange={(e) => setJobId(e.target.value)}
            placeholder="e.g., 2"
          />

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
