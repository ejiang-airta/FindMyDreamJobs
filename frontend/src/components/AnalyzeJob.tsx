// ✅ File: /frontend/src/components/AnalyzeJob.tsx
// This component is for analyzing job descriptions.
'use client'

import React, { useEffect, useState } from 'react'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { toast } from 'sonner'
import { BACKEND_BASE_URL } from '@/lib/env'
import { useWizardState } from '@/context/WizardContext'

interface AnalyzeJobProps {
  isWizard?: boolean
  onSuccess?: () => void
}

type SkillItem = { skill: string; frequency?: number }

type ParsedJobResponse = {
  job_id?: number
  title?: string
  company?: string
  location?: string
  job_link: string
  salary?: string
  experience?: string
  skills?: {
    emphasized_skills?: string[]
    skills?: SkillItem[]
  }
}

type JobDraft = {
  job_id?: number
  job_title: string
  company_name: string
  location: string
  job_link: string
  salary: string
  applicants_count: string // ✅ string like "100+"
}

const AnalyzeJob: React.FC<AnalyzeJobProps> = ({ isWizard = false, onSuccess }) => {
  const [parsedData, setParsedData] = useState<ParsedJobResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [userId, setUserId] = useState<string | null>(null)

  const [jobLink, setJobLink] = useState('')
  const [jobDescriptionLocal, setJobDescriptionLocal] = useState('')

  // editable draft fields (filled after parse)
  const [jobDraft, setJobDraft] = useState<JobDraft>({
    job_id: undefined,
    job_title: '',
    company_name: '',
    location: '',
    job_link: '',
    salary: '',
    applicants_count: '',
  })

  const [isSaving, setIsSaving] = useState(false)

  // Wizard support
  let jobDescription = jobDescriptionLocal
  let setJobDescription = setJobDescriptionLocal

  if (isWizard) {
    const wizardState = useWizardState()
    jobDescription = wizardState.jobDescription
    setJobDescription = wizardState.setJobDescription
  }

  useEffect(() => {
      // Only runs in the browser
    const id = localStorage.getItem('user_id')
    setUserId(id)
  }, [])

  const handleSubmit = async () => {
    if (!userId) {
      setError('Please sign in again — user_id not found.')
      return
    }

    if (!jobLink && !jobDescription) {
      setError('Please provide a job link or paste a job description.')
      return
    }

    setError(null)

    try {
      const response = await fetch(`${BACKEND_BASE_URL}/parse-job-description`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_link: jobLink,
          job_description: jobDescription,
          user_id: parseInt(userId, 10),
        }),
      })

      const result: ParsedJobResponse = await response.json()

      if (!response.ok) {
        setError(`❌ Error: ${(result as any)?.detail || 'Failed to parse job description'}`)
        return
      }

      setParsedData(result)

      // Pre-fill editable fields from parsed output
      setJobDraft((prev) => ({
        ...prev,
        job_id: result.job_id,
        job_title: result.title ?? '',
        company_name: result.company ?? '',
        job_link: result.job_link,
        location: result.location ?? '',
        salary: result.salary ?? '',
        // applicants_count is user input; keep whatever user typed previously
      }))

      toast.success('Job description parsed successfully!', { icon: '✅' })
      if (onSuccess) onSuccess()
    } catch {
      setError('❌ Network error. Please try again.')
    }
  }

  const handleSave = async () => {
    if (!jobDraft.job_id) {
      toast.error('Missing job_id from parse response. Please update backend to return job_id.')
      return
    }

    setIsSaving(true)
    setError(null)

    try {
      const response = await fetch(`${BACKEND_BASE_URL}/jobs/${jobDraft.job_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_title: jobDraft.job_title,
          company_name: jobDraft.company_name,
          location: jobDraft.location,
          job_link: jobDraft.job_link,
          salary: jobDraft.salary,
          applicants_count: jobDraft.applicants_count,
        }),
      })

      const result = await response.json()

      if (!response.ok) {
        setError(`❌ Error: ${result.detail || 'Failed to save job details'}`)
        return
      }

      toast.success('Job details saved to database!', { icon: '💾' })
    } catch {
      setError('❌ Network error while saving. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="space-y-10 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold">📄 Analyze Job Description</h2>

      <div className="space-y-2">
        <label className="text-sm font-medium">Job Description:</label>
        <Textarea
          placeholder="Please copy and paste job description here..."
          rows={10}
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          className="resize-y"
        />
      </div>

      <Button className="bg-blue-500 text-white hover:bg-blue-600" onClick={handleSubmit}>
        Analyze Job Description
      </Button>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Editable draft fields (after parse) */}
      {parsedData && (
        <div className="p-4 bg-gray-100 rounded-md space-y-4">
          <h3 className="text-lg font-semibold">Review & Edit Job Details (then Save):</h3>

          <div className="grid gap-3">
            <div>
              <label className="text-sm font-medium">Job Title</label>
              <Input
                value={jobDraft.job_title}
                onChange={(e) => setJobDraft({ ...jobDraft, job_title: e.target.value })}
                placeholder="e.g., Senior Director, Engineering"
              />
            </div>

            <div>
              <label className="text-sm font-medium">Company</label>
              <Input
                value={jobDraft.company_name}
                onChange={(e) => setJobDraft({ ...jobDraft, company_name: e.target.value })}
                placeholder="e.g., Arctic Wolf"
              />
            </div>

            <div>
              <label className="text-sm font-medium">Salary Range</label>
              <Input
                value={jobDraft.salary}
                onChange={(e) => setJobDraft({ ...jobDraft, salary: e.target.value })}
                placeholder="e.g., 180k–220k CAD"
              />
            </div>

            <div>
              <label className="text-sm font-medium">Location</label>
              <Input
                value={jobDraft.location}
                onChange={(e) => setJobDraft({ ...jobDraft, location: e.target.value })}
                placeholder="e.g., Vancouver, BC / Remote (Canada)"
              />
            </div>

            <div>
              <label className="text-sm font-medium">Job Link URL</label>
              <Input
                value={jobDraft.job_link}
                onChange={(e) => setJobDraft({ ...jobDraft, job_link: e.target.value })}
                placeholder='e.g., "https://www.linkedin.com/jobs/view/4336963628/"'
              />
            </div>
            <div>
              <label className="text-sm font-medium"># of Applicants</label>
              <Input
                value={jobDraft.applicants_count}
                onChange={(e) => setJobDraft({ ...jobDraft,applicants_count: e.target.value })}
                placeholder='e.g., "100+"'
              />
            </div>
          </div>
          <Button
            className="bg-green-600 text-white hover:bg-green-700"
            onClick={handleSave}
            disabled={isSaving}
          >
            {isSaving ? 'Saving...' : 'Save Job Details'}
          </Button>

          <div className="pt-2 space-y-2">
            <p><strong>Experience:</strong> {parsedData.experience || 'N/A'}</p>

            <p className="font-semibold">Emphasized Skills:</p>
            <ul className="list-disc pl-5">
              {(parsedData.skills?.emphasized_skills || []).length > 0
                ? (parsedData.skills?.emphasized_skills || []).map((skill: string, idx: number) => (
                    <li key={idx}>{skill}</li>
                  ))
                : <li>N/A</li>}
            </ul>

            <p className="font-semibold">All Skills:</p>
            <ul className="list-disc pl-5">
              {Array.isArray(parsedData.skills?.skills) && (parsedData.skills?.skills || []).length > 0
                ? (parsedData.skills?.skills || []).map((item: any, idx: number) => (
                    <li key={idx}>{item.skill}</li>
                  ))
                : <li>N/A</li>}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}

export default AnalyzeJob
