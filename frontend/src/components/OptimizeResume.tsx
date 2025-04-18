// ✅ File:  frontend/src/components/OptimizeResume.tsx
// This component is for optimizing resumes based on job requirements.
// It allows users to select a resume and a job, and then optimize the resume based on the job's emphasized skills.
// It also provides a preview of the optimized resume and allows users to approve or download it.
//
'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'
import { toast } from "sonner"
import { motion } from "framer-motion"
import { BACKEND_BASE_URL }  from '@/lib/env'

interface OptimizeProps {
  userId: string
  isWizard?: boolean
  onSuccess?: () => void
}

const OptimizeResume: React.FC<OptimizeProps> = ({ userId, isWizard = false, onSuccess }) => {
  const [resumeId, setResumeId] = useState('')
  const [jobId, setJobId] = useState('')
  const [resumes, setResumes] = useState<any[]>([])
  const [jobs, setJobs] = useState<any[]>([])
  const [emphasized, setEmphasized] = useState('')
  const [missing, setMissing] = useState('')
  const [justification, setJustification] = useState('')
  const [response, setResponse] = useState<any>(null)
  const [error, setError] = useState('')
  const [optimizedText, setOptimizedText] = useState<string | null>(null)
  const [isOptimizing, setIsOptimizing] = useState(false)

  useEffect(() => {
    const fetchDropdowns = async () => {
      try {
        const [res1, res2] = await Promise.all([
          fetch(`${BACKEND_BASE_URL}/resumes/by-user/${userId}`),
          fetch(`${BACKEND_BASE_URL}/jobs/all`)
        ])

        setResumes(await res1.json())
        setJobs(await res2.json())
      } catch (err) {
        console.error('❌ Failed to fetch dropdowns', err)
      }
    }

    fetchDropdowns()
  }, [userId])

  useEffect(() => {
    if (resumeId && jobId) ensureMatchData()
  }, [resumeId, jobId])

  useEffect(() => {
    if (jobId) fetchEmphasized()
  }, [jobId])

  const ensureMatchData = async () => {
    try {
      const matchRes = await fetch(`${BACKEND_BASE_URL}/match-score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: parseInt(resumeId),
          job_id: parseInt(jobId)
        })
      })

      const matchData = await matchRes.json()
      setMissing(matchData.missing_skills?.join(', ') || '')

      if (!emphasized.trim()) {
        setEmphasized(matchData.matched_skills?.join(', ') || '')
      }
    } catch (err) {
      console.error("❌ Error ensuring match data:", err)
      setError("Failed to prepare matching info.")
    }
  }

  const fetchEmphasized = async () => {
    try {
      const jobRes = await fetch(`${BACKEND_BASE_URL}/jobs/${jobId}`)
      if (!jobRes.ok) return
      const jobData = await jobRes.json()
      const skills = jobData?.emphasized_skills || []
      setEmphasized(skills.join(', '))
    } catch (err) {
      console.error("❌ Failed to fetch emphasized skills:", err)
    }
  }

  const handleOptimize = async () => {
    setError('')
    setResponse(null)

    if (!resumeId || !jobId) {
      setError('Please enter both Resume ID and Job ID.')
      return
    }

    setIsOptimizing(true)

    try {
      const res = await fetch(`${BACKEND_BASE_URL}/optimize-resume`, {
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
      toast.success("🎉 Resume optimized successfully!")

      if (isWizard && typeof onSuccess === 'function') {
        onSuccess()
      }
    } catch (err) {
      setError('❌ Failed to optimize resume.')
      console.error(err)
    }
    finally {
      setIsOptimizing(false)
    }
  }

  const handleApprove = async () => {
    try {
      const response = await fetch(`${BACKEND_BASE_URL}/approve-resume`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_id: resumeId })
      })

      const data = await response.json()
      if (response.ok) {
        toast.success(data.message || "✅ Resume approved!")
      } else {
        alert(data.detail || "❌ Failed to approve resume.")
      }
    } catch (err) {
      alert("❌ Network error approving resume.")
      console.error(err)
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto px-4 sm:px-6 md:px-8 mt-10 space-y-6">
      <h1 className="text-2xl font-bold">🛠 Optimize Resume</h1>
      <p className="text-muted-foreground text-sm">
        Enhance your resume using job-specific skills. Choose a resume and a job to begin.
      </p>

      <Card>
        <CardContent className="space-y-6 p-4 sm:p-6">
          <Label>Select Resume</Label>
          <Select onValueChange={setResumeId}>
            <SelectTrigger>
              <SelectValue placeholder="Choose your resume" />
            </SelectTrigger>
            <SelectContent>
              {resumes.map(r => (
                <SelectItem key={r.id} value={String(r.id)}>
                  {`Resume #${r.id}`} - {r.resume_name}
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
                  {`Job #${j.id}`} – {j.job_title} @ {j.company_name || 'Unknown'}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Label>🧠 Emphasized Skills</Label>
          <Textarea
            rows={2}
            value={emphasized}
            onChange={e => setEmphasized(e.target.value)}
            placeholder="e.g., Python, FastAPI, AWS"
          />

          {emphasized && missing && (
            <div className="bg-yellow-50 border border-yellow-300 p-3 rounded text-sm">
              <strong>📌 Suggested Missing Skills:</strong>
              <p className="mt-1 text-gray-700">
                Please explain any missing skills from the job requirements in your justification.
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

          <Button
            className="w-full"
            onClick={handleOptimize}
            disabled={isOptimizing || !resumeId || !jobId}           >
            {isOptimizing ? "Optimizing..." : "✨ Run Optimization"}
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
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mt-6 space-y-4"
            >
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
                      window.open(`${BACKEND_BASE_URL}/download-resume/${resumeId}`, "_blank")
                    }}
                  >
                    📥 Download Resume
                  </Button>
                </div>
              </div>
            </motion.div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default OptimizeResume
