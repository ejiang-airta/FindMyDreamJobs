'use client'

import React, { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Label } from '@/components/ui/label'

export default function ApplyPage() {
  const [resumeId, setResumeId] = useState('')
  const [jobId, setJobId] = useState('')
  const [applicationUrl, setApplicationUrl] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  console.log({
    resumeId,
    jobId,
    applicationUrl
  })

  const handleSubmit = async () => {
    setMessage('')
    setError('')

    if (!resumeId || !jobId || !applicationUrl) {
      setError('⚠️ All fields are required.')
      return
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/submit-application', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: parseInt(resumeId),
          job_id: parseInt(jobId),
          application_url: applicationUrl.trim()
        }),
      })

      const data = await response.json()
      if (!response.ok) {
        const errorMessage = data.detail || data.message || JSON.stringify(data)
        setError(`❌ ${errorMessage}`)
        return
      }

        setMessage(data.status || '✅ Application submitted successfully!')
        setResumeId('')
        setJobId('')
        setApplicationUrl('')
      }
      catch (err: any) {
        console.error("❌ Network error:", err)
        setError('❌ Network error occurred. Please try again.')
    }
  }
  
  
  return (
    <div className="max-w-xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">📩 Submit Job Application</h1>
      <p className="text-muted-foreground text-sm">
        Enter your Resume ID, Job ID, and the application URL where you applied.
      </p>

      <Card>
        <CardContent className="p-6 space-y-4">
          <div>
            <Label htmlFor="resumeId">Resume ID</Label>
            <Input
              id="resumeId"
              type="number"
              value={resumeId}
              onChange={(e) => setResumeId(e.target.value)}
              placeholder="e.g. 6"
            />
          </div>

          <div>
            <Label htmlFor="jobId">Job ID</Label>
            <Input
              id="jobId"
              type="number"
              value={jobId}
              onChange={(e) => setJobId(e.target.value)}
              placeholder="e.g. 3"
            />
          </div>

          <div>
            <Label htmlFor="applicationUrl">Application URL</Label>
            <Input
              id="applicationUrl"
              type="url"
              value={applicationUrl}
              onChange={(e) => setApplicationUrl(e.target.value)}
              placeholder="https://company.com/job/apply"
            />
          </div>

          <Button onClick={handleSubmit}>Submit Application</Button>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          {message && (
            <Alert variant="default">
              <AlertDescription>{message}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
