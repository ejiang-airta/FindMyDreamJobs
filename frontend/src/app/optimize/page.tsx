// ✅ File: frontend/src/app/optimize/page.tsx
// This page is for optimizing resumes based on job descriptions.

'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useSession } from 'next-auth/react'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <OptimizeResumePage />
}

// This component is the main page for optimizing resumes.
// It allows users to input a resume ID, job ID, and skills to emphasize or justify:
function OptimizeResumePage() {
  const [resumeId, setResumeId] = useState('')
  const [jobId, setJobId] = useState('')
  const [emphasized, setEmphasized] = useState('')
  const [missing, setMissing] = useState('')
  const [response, setResponse] = useState<any>(null)
  const [error, setError] = useState('')
  const [optimizedText, setOptimizedText] = useState<string | null>(null)


  const handleOptimize = async () => {
    setError('')
    setResponse(null)

    if (!resumeId) {
      setError('Please enter a valid Resume ID.')
      return
    }

    if (!jobId) {
      setError('Please enter a valid Job ID.')
      return
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/optimize-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: parseInt(resumeId),
          job_id: parseInt(jobId),
          emphasized_skills: emphasized.split(',').map(s => s.trim()),
          missing_skills: missing.split(',').map(s => s.trim()),
          justification: missing.trim()  // ✅ This line fixes 422 Unprocessable Entity!
        }),
      })

      const data = await res.json()
      setOptimizedText(data.optimized_text)  // ✅ Store it for preview
      if (!res.ok) {
        setError(data.detail || 'Failed to optimize resume.')
        return
      }

      setResponse(data)
    } catch (err) {
      console.error(err)
      setError('Unexpected error occurred.')
    }
  }

  return (
    <div className="max-w-xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">🛠 Optimize Resume</h1>
      <p className="text-muted-foreground text-sm">
        Enhance your resume by emphasizing and justifying skills. You must provide a valid resume ID.
      </p>

      <Card>
        <CardContent className="space-y-4 p-6">
          <Label>Resume ID</Label>
          <Input
            type="number"
            value={resumeId}
            onChange={e => setResumeId(e.target.value)}
            placeholder="e.g., 6"
          />
          <Label>Job ID</Label>
          <Input
            type="number"
            value={jobId}
            onChange={e => setJobId(e.target.value)}
            placeholder="e.g., 1"
          />
          <Label>🧠 Emphasized Skills (from JD)</Label>
          <Textarea
            rows={2}
            value={emphasized}
            onChange={e => setEmphasized(e.target.value)}
            placeholder="e.g., python, fastapi, aws"
          />

          <Label>📌 Missing Skills Justification</Label>
          <Textarea
            rows={2}
            value={missing}
            onChange={e => setMissing(e.target.value)}
            placeholder="e.g., Familiar with Docker through side projects"
          />

          <Button onClick={handleOptimize}>✨ Run Optimization</Button>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>
                {typeof error === 'string'
                  ? error
                  : JSON.stringify(error, null, 2)}
              </AlertDescription>
            </Alert>
          )}


          {response && (
            <Alert>
              <AlertDescription>
                ✅ Optimization Complete! Match Score: <strong>{response.match_score_final}%</strong>, ATS Score:{' '}
                <strong>{response.ats_score_final}%</strong>
              </AlertDescription>
            </Alert>
          )}
          
          {optimizedText && (
            <div className="space-y-4 mt-6">
              <h3 className="text-lg font-semibold">✅ Optimized Resume Preview</h3>
              <pre className="bg-muted p-4 rounded whitespace-pre-wrap max-h-96 overflow-auto text-sm">
                {optimizedText}
              </pre>

              <Button
                variant="default"  // ✅ Replace "success" with a valid variant
                onClick={async () => {
                  try {
                    const response = await fetch("http://127.0.0.1:8000/approve-resume", {
                      method: "POST",
                      headers: {
                        "Content-Type": "application/json"
                      },
                      body: JSON.stringify({ resume_id: resumeId })
                    })

                    const data = await response.json()
                    if (response.ok) {
                      alert(data.message || "✅ Resume approved!")
                    } else {
                      alert(data.detail || "❌ Failed to approve resume.")
                    }
                  } catch (err) {
                    alert("❌ Network error approving resume.")
                    console.error(err)
                  }
                }}
              >
                🚀 Approve Resume
              </Button>
              <Button
                variant="secondary"
                onClick={() => {
                  window.open(`http://127.0.0.1:8000/download-resume/${resumeId}`, "_blank")
                }}
              >
                📥 Download Resume
              </Button>
            </div>
          )}

        </CardContent>
      </Card>
    </div>
  )
}
