// File: /frontend/src/components/JobInput.tsx
//🟡 JD input

'use client'

import React, { useState, useEffect } from 'react'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { BACKEND_BASE_URL }  from '@/lib/env'

interface JobInputProps {
  onAnalysisComplete?: () => void
}

const JobInput: React.FC<JobInputProps> = ({ onAnalysisComplete }) => {
  const [jobLink, setJobLink] = useState<string>('')
  const [jobDescription, setJobDescription] = useState<string>('')
  const [parsedData, setParsedData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [userId, setUserId] = useState<string | null>(null)
    
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
          user_id: parseInt(userId || "0"),  // ✅ required!
        }),
      })

      const result = await response.json()

      if (response.ok) {
        setParsedData(result)

        // ✅ Notify wizard that analysis is complete
        if (onAnalysisComplete) onAnalysisComplete()
          
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
        <label className="block text-sm font-medium">Job Description:</label>
        <Textarea
          placeholder="Please copy and paste job description here..."
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
          <p><strong>Experience:</strong> {parsedData.experience || 'N/A'}</p>
          <p><strong>Emphasized Skills:</strong></p>
          <ul className="list-disc pl-5">
            {(parsedData.skills?.emphasized_skills || []).length > 0
              ? parsedData.skills.emphasized_skills.map((skill: string, idx: number) => (
                  <li key={idx}>{skill}</li>
                ))
              : <li>N/A</li>}
          </ul>
          <p><strong>Complete list of Skills:</strong></p>
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

export default JobInput
