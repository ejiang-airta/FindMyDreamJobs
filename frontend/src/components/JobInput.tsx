// File: /frontend/src/components/JobInput.tsx
//🟡 JD input

'use client'

import React, { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'

const JobInput: React.FC = () => {
  const [jobLink, setJobLink] = useState<string>('')
  const [jobDescription, setJobDescription] = useState<string>('')
  const [parsedData, setParsedData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const userId = localStorage.getItem("user_id")  // ✅ this must exist

  const handleSubmit = async () => {
    if (!jobLink && !jobDescription) {
      setError('Please provide a job link or paste a job description.')
      return
    }

    setError(null)

    try {
      const response = await fetch('http://localhost:8000/parse-job-description', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_link: jobLink,
          job_description: jobDescription,
          user_id: parseInt(userId || "0"),  // ✅ required!
        }),
      })

      const result = await response.json()

      if (response.ok) {
        setParsedData(result)
      } else {
        setError(`❌ Error: ${result.detail || 'Failed to parse job description'}`)
      }
    } catch (err) {
      setError('❌ Network error. Please try again.')
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-md space-y-4">
      <h2 className="text-2xl font-semibold">Job Description Input</h2>

      <div className="space-y-2">
        <label className="block text-sm font-medium">Paste Job URL (Optional)</label>
        <Input
          type="text"
          placeholder="https://example.com/job-posting"
          value={jobLink}
          onChange={(e) => setJobLink(e.target.value)}
        />
      </div>

      <div className="space-y-2">
        <label className="block text-sm font-medium">Paste Job Description</label>
        <Textarea
          placeholder="Copy and paste job description here..."
          rows={10}
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          className="w-full md:w-[90%] lg:w-[95%] resize-y"
        />
      </div>

      <Button className="w-full mt-4" onClick={handleSubmit}>
        Analyze Job Description
      </Button>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {parsedData && (
        <div className="mt-4 p-4 bg-gray-100 rounded-md">
          <h3 className="text-lg font-semibold">Extracted Job Details:</h3>
          <p><strong>Title:</strong> {parsedData.title || 'N/A'}</p>
          <p><strong>Company:</strong> {parsedData.company || 'N/A'}</p>
          <p><strong>Location:</strong> {parsedData.location || 'N/A'}</p>
          <p><strong>Skills:</strong> 
            {parsedData.skills && Array.isArray(parsedData.skills)
              ? parsedData.skills.map((s: any, idx: number) => (
                  <span key={idx}>
                    {s.skill} ({s.frequency}){idx < parsedData.skills.length - 1 ? ', ' : ''}
                  </span>
                ))
              : 'N/A'}
          </p>
          <p><strong>Experience:</strong> {parsedData.experience || 'N/A'}</p>
        </div>
      )}
    </div>
  )
}

export default JobInput
