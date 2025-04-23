// ✅ File: /frontend/src/components/AnalyzeJob.tsx
// This component is for analyzing job descriptions.
'use client'

import React, { useEffect, useState } from 'react'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { toast } from 'sonner'
import { BACKEND_BASE_URL }  from '@/lib/env'
import { useWizardState } from '@/context/WizardContext'

interface AnalyzeJobProps {
  isWizard?: boolean
  onSuccess?: () => void
}

const AnalyzeJob: React.FC<AnalyzeJobProps> = ({ isWizard = false, onSuccess }) => {
  const [parsedData, setParsedData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [userId, setUserId] = useState<string | null>(null)
  const [isDirty, setIsDirty] = useState(false)
  const [jobLink, setJobLink] = useState('')
  const [jobDescriptionLocal, setJobDescriptionLocal] = useState('')

  // If isWizard is true, use the wizard state for job description
  // Otherwise, use local state
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
          user_id: parseInt(userId || "0"),
        }),
      })

      const result = await response.json()

      if (response.ok) {
        setParsedData(result)
        toast.success("Job description parsed successfully!", { icon: "✅" } )
        if (onSuccess) onSuccess()
      } else {
        setError(`❌ Error: ${result.detail || 'Failed to parse job description'}`)
      }
    } catch (err) {
      setError('❌ Network error. Please try again.')
    }
  }

  return (
    <div className="space-y-10 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold">📄 Analyze Job Description</h2>

      {/* <div className="space-y-2">
        <label className="text-sm font-medium">Paste Job URL (Optional)</label>
        <Input
          type="text"
          placeholder="https://example.com/job-posting"
          value={jobLink}
          onChange={(e) => setJobLink(e.target.value)}
        />
      </div> */}

      <div className="space-y-2">
        <label className="text-sm font-medium">Job Description:</label>
        <Textarea
          placeholder="Please copy and paste job description here..."
          rows={10}
          value={jobDescription}
          onChange={(e) => {
            setJobDescription(e.target.value)
            setIsDirty(true)
            }            
          }
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

      {parsedData && (
        <div className="p-4 bg-gray-100 rounded-md space-y-2">
          <h3 className="text-lg font-semibold">Extracted Job Details:</h3>
          <p><strong>Title:</strong> {parsedData.title || 'N/A'}</p>
          <p><strong>Company:</strong> {parsedData.company || 'N/A'}</p>
          <p><strong>Location:</strong> {parsedData.location || 'N/A'}</p>
          <p><strong>Experience:</strong> {parsedData.experience || 'N/A'}</p>
          <p><strong>Emphasized Skills:</strong></p>
          <ul className="list-disc pl-5">
            {(parsedData.skills?.emphasized_skills || []).length > 0
              ? parsedData.skills.emphasized_skills.map((skill: string, idx: number) => (
                <li key={idx}>{skill}</li>
              ))
              : <li>N/A</li>}
          </ul>
          <p><strong>All Skills:</strong></p>
          <ul className="list-disc pl-5">
            {Array.isArray(parsedData.skills?.skills)
              ? [...parsedData.skills.skills]
                .sort((a: any, b: any) => b.frequency - a.frequency)
                .map((item: any, idx: number) => (
                  <li key={idx}>{item.skill}</li>
                ))
              : <li>N/A</li>}
          </ul>
        </div>
      )}
    </div>
  )
}

export default AnalyzeJob
