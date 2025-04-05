'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useSession } from 'next-auth/react'

export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <OptimizeResumePage />
}

function OptimizeResumePage() {
  const [resumeId, setResumeId] = useState('')
  const [jobId, setJobId] = useState('')
  const [emphasized, setEmphasized] = useState('')
  const [missing, setMissing] = useState('')
  const [justification, setJustification] = useState('')
  const [response, setResponse] = useState<any>(null)
  const [error, setError] = useState('')
  const [optimizedText, setOptimizedText] = useState<string | null>(null)

  // 🧠 Helper to call /match-score if needed, then fetch skills
  const ensureMatchData = async () => {
    if (!resumeId || !jobId) return

    try {
      const matchRes = await fetch(`http://127.0.0.1:8000/match-score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: parseInt(resumeId),
          job_id: parseInt(jobId)
        })
      })

      if (!matchRes.ok) {
        throw new Error("Failed to compute match score")
      }

      const matchData = await matchRes.json()

      // ✅ Set missing skills directly
      setMissing(matchData.missing_skills?.join(', ') || '')

          // ✅ Optionally preload matched skills as emphasized
      if (!emphasized.trim()) {
        setEmphasized(matchData.matched_skills?.join(', ') || '')
      }
    } catch (err) {
      console.error("❌ Error ensuring match data:", err)
      setError("Failed to prepare matching info.")
    }
  }
  
  
  // 🚀 Auto-fetch emphasized_skills from DB when jobId is entered
  // ✅ Extract emphasized_skills from backend
  const fetchEmphasized = async () => {
    if (!jobId) return

    try {
      const jobRes = await fetch(`http://127.0.0.1:8000/jobs/${jobId}`)
      if (!jobRes.ok) return
      const jobData = await jobRes.json()
      const skills = jobData?.emphasized_skills || []
      setEmphasized(skills.join(', '))
    } catch (err) {
      console.error("❌ Failed to fetch emphasized skills:", err)
    }
  }
  useEffect(() => {
    if (resumeId && jobId) {
      ensureMatchData()
      fetchEmphasized()
    }
  }, [resumeId, jobId])
  const handleOptimize = async () => {
    setError('')
    setResponse(null)

    if (!resumeId || !jobId) {
      setError('Please enter both Resume ID and Job ID.')
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
          justification: justification.trim()
        }),
      })

      const data = await res.json()
      setOptimizedText(data.optimized_text)

      if (!res.ok) {
        setError(data.detail || 'Failed to optimize resume.')
        return
      }

      setResponse(data)
    } catch (err) {
      setError('Unexpected error occurred.')
      console.error(err)
    }
  }

    // 🔁 Approve resume
    const handleApprove = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/approve-resume", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
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
    }
  

  return (
    <div className="max-w-2xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">🛠 Optimize Resume</h1>
      <p className="text-muted-foreground text-sm">
      Enhance your resume using job-specific skills. Provide Resume & Job ID to continue.
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
          <div className="flex space-x-2">
            <Input
              type="number"
              value={jobId}
              onChange={e => setJobId(e.target.value)}
              placeholder="e.g., 1"
            />
          </div>

          <Label>🧠 Emphasized Skills</Label>
          <Textarea
            rows={2}
            value={emphasized}
            onChange={e => setEmphasized(e.target.value)}
            placeholder="e.g., Python, FastAPI, AWS"
          />
          {emphasized && missing &&  (
            <div className="bg-yellow-50 border border-yellow-300 p-3 rounded text-sm">
              <strong>📌 Suggested Missing Skills:</strong>
              <p className="mt-1 text-gray-700">
                Please explain any missing skills from the job requirements in your justification. Example: 
                <em>“Familiar with Docker through side projects.”</em>
              </p>
              <p className="mt-1 text-blue-700">
                🧠 You’re missing: <strong>{missing}</strong>
              </p>
            </div>
          )}

          <Label>📌 Justification for Missing Skills</Label>
          <Textarea
            rows={2}
            value={justification}
            onChange={e => setJustification(e.target.value)}
            placeholder="e.g., Familiar with Docker through open-source projects"
          />

          <Button onClick={handleOptimize} className="w-full">
            ✨ Run Optimization
          </Button>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {response && (
            <Alert>
              <AlertDescription>
                ✅ Optimization Complete! <br />
                <strong>Match Score:</strong> {response.match_score_final}% <strong>ATS Score:</strong> {response.ats_score_final}%
              </AlertDescription>
            </Alert>
          )}

          {optimizedText && (
            <div className="mt-6 space-y-4">
              <h3 className="text-lg font-semibold">📝 Optimized Resume Preview</h3>
              <pre className="bg-muted p-4 rounded whitespace-pre-wrap max-h-96 overflow-auto text-sm">
                {optimizedText}
              </pre>
              {response?.changes_summary && (
                <div className="bg-gray-50 p-4 rounded border">
                  <h4 className="font-semibold text-sm mb-2">🔍 Summary of Optimizations</h4>
                  <ul className="list-disc list-inside text-sm text-gray-700">
                    {response.changes_summary.map((line: string, index: number) => (
                      <li key={index}>{line}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="flex gap-3">
                <Button variant="default" onClick={handleApprove}>
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
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
