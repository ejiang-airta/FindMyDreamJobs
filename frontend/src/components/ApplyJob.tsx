// ✅ File: frontend/src/components/ApplyJob.tsx
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { AppButton } from '@/components/ui/AppButton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { toast } from 'sonner'
import { BACKEND_BASE_URL }  from '@/lib/env'

interface ApplyJobProps {
  userId: string
  isWizard?: boolean
  onSuccess?: () => void
}

const ApplyJob: React.FC<ApplyJobProps> = ({ userId, isWizard = false, onSuccess }) => {
  const [resumeId, setResumeId] = useState('')
  const [resumes, setResumes] = useState<any[]>([])
  const [jobs, setJobs] = useState<any[]>([])
  const [jobId, setJobId] = useState('')
  const [applicationUrl, setApplicationUrl] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [res1, res2] = await Promise.all([
          fetch(`${BACKEND_BASE_URL}/resumes/by-user/${userId}`),
          fetch(`${BACKEND_BASE_URL}/jobs/by-user/${userId}`),
        ])
        if (res1.ok) setResumes(await res1.json())
        if (res2.ok) setJobs(await res2.json())
      } catch (err) {
        console.error('❌ Failed to load resumes or jobs:', err)
      }
    }
    fetchData()
  }, [userId])

  const handleSubmit = async () => {
    setMessage('')
    setError('')

    if (!resumeId || !jobId || !applicationUrl) {
      setError('⚠️ All fields are required.')
      return
    }

    try {
      const response = await fetch(`${BACKEND_BASE_URL}/submit-application`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: parseInt(resumeId),
          job_id: parseInt(jobId),
          application_url: applicationUrl.trim(),
        }),
      })

      const data = await response.json()
      if (!response.ok) {
        setError(data.detail || data.message || JSON.stringify(data))
        return
      }

      setMessage(data.status || '✅ Application submitted successfully!')
      setResumeId('')
      setJobId('')
      setApplicationUrl('')
      toast.success('🎉 Application submitted!')

      if (isWizard && typeof onSuccess === 'function') {
        onSuccess()
      }
    } catch (err: any) {
      console.error('❌ Network error:', err)
      setError('❌ Network error occurred. Please try again.')
    }
  }

  return (
    <div className="max-w-xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">📩 Submit Job Application</h1>
      <p className="text-muted-foreground text-sm">
        Please select your resume, job, and enter application URL. They all required for applying the job.
      </p>

      <Card>
        <CardContent className="p-6 space-y-4">
          <div>
            <Label htmlFor="resumeId">Resume</Label>
            <Select value={resumeId} onValueChange={setResumeId}>
              <SelectTrigger>
                <SelectValue placeholder="Select resume" />
              </SelectTrigger>
              <SelectContent>
                {resumes.map((resume) => (
                  <SelectItem key={resume.id} value={String(resume.id)}>
                    Resume #{resume.id} – {resume.resume_name || 'Unnamed'}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label htmlFor="jobId">Job</Label>
            <Select value={jobId} onValueChange={setJobId}>
              <SelectTrigger>
                <SelectValue placeholder="Select job" />
              </SelectTrigger>
              <SelectContent>
                {jobs.map((job) => (
                  <SelectItem key={job.id} value={String(job.id)}>
                    Job #{job.id} – {job.job_title} - {job.company_name || 'Unknown'}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
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

          <AppButton onClick={handleSubmit}>Submit Application</AppButton>

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

export default ApplyJob
