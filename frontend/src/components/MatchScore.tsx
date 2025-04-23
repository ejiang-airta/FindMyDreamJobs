// ✅ File: /frontend/src/components/MatchScore.tsx
//Display match score percentage & keywords matched

'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { AppButton } from '@/components/ui/AppButton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { BACKEND_BASE_URL }  from '@/lib/env'
import { useWizardState } from '@/context/WizardContext'

interface MatchScoreProps {
  isWizard?: boolean
  onSuccess?: () => void
  userId?: string | null  // <-- new
}

const MatchScore: React.FC<MatchScoreProps> = ({ isWizard = false, onSuccess, userId }) => {
  const [resumes, setResumes] = useState<any[]>([])
  const [jobs, setJobs] = useState<any[]>([])
  const [matchScore, setMatchScore] = useState<number | null>(null)
  const [keywords, setKeywords] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)
  const [resumeIdLocal, setResumeIdLocal] = useState('')
  const [jobIdLocal, setJobIdLocal] = useState('')

  // If isWizard is true, use the wizard state for job description:
  let resumeId = resumeIdLocal
  let setResumeId = setResumeIdLocal
  let jobId = jobIdLocal
  let setJobId = setJobIdLocal

  // Override with wizard state if applicable
  if (isWizard) {
    const wizardState = useWizardState()
    resumeId = wizardState.resumeId
    setResumeId = wizardState.setResumeId
    jobId = wizardState.jobId
    setJobId = wizardState.setJobId
  }

  useEffect(() => {
    if (!userId) return  // 🛑 Don't fetch unless userId is available

    const fetchDropdowns = async () => {
      try {
        const [res1, res2] = await Promise.all([
          fetch(`${BACKEND_BASE_URL}/resumes/by-user/${userId}`),
          fetch(`${BACKEND_BASE_URL}/jobs/by-user/${userId}`),
        ])
        const resumesData = await res1.json()
        const jobsData = await res2.json()
    
        setResumes(Array.isArray(resumesData) ? resumesData : [])
        setJobs(Array.isArray(jobsData) ? jobsData : [])  // ✅ this line prevents crash
      } catch (err) {
        console.error('❌ Error loading dropdowns:', err)
      }
    }
    

    fetchDropdowns()
  }, [userId])

  const handleMatchScore = async () => {
    if (!resumeId || !jobId) {
      setError('⚠️ Please select both Resume and Job.')
      return
    }

    try {
      const response = await fetch(`${BACKEND_BASE_URL}/match-score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: parseInt(resumeId),
          job_id: parseInt(jobId)
        })
      })
      const data = await response.json()

      if (!response.ok) {
        setError(data.detail || 'Failed to calculate match score.')
        return
      }

      setMatchScore(data.match_score)
      setKeywords(data.matched_skills || [])
      setError(null)

      if (isWizard && typeof onSuccess === 'function') {
        onSuccess()
      }

    } catch (err) {
      setError('❌ Network error. Please try again.')
    }
  }

  return (
    <Card className="p-6 space-y-4">
      <CardContent>
        <h2 className="text-lg font-bold">🔍 Resume & Job Match Score</h2>

        <Label>Select Resume</Label>
        <Select value={resumeId} onValueChange={setResumeId}>
          <SelectTrigger>
            <SelectValue placeholder="Choose your resume" />
          </SelectTrigger>
          <SelectContent>
          {Array.isArray(resumes) ? resumes.map(r => (
            <SelectItem key={r.id} value={String(r.id)}>
              {`Resume #${r.id}`} – {r.resume_name}
            </SelectItem>
          )) : (
            <div className="text-red-500 text-sm mt-2">❌ No resumes found</div>
          )}
          </SelectContent>
        </Select>

        <Label className="mt-4">Select Job</Label>
        <Select value={jobId} onValueChange={setJobId}>
          <SelectTrigger>
            <SelectValue placeholder="Choose a job" />
          </SelectTrigger>
          <SelectContent>
            {jobs.map((j) => (
              <SelectItem key={j.id} value={String(j.id)}>
                {`Job #${j.id}`} – {j.job_title} @ {j.company_name || 'Unknown'}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <AppButton className="mt-4 w-full" onClick={handleMatchScore}>
          Calculate Match Score
        </AppButton>

        {error && (
          <Alert variant="destructive" className="mt-3">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {matchScore !== null && (
          <div className="mt-4 space-y-2">
            <p className="text-lg">✅ Match Score: <strong>{matchScore}%</strong></p>
            <p className="text-sm">🔹 Matched Skills: {keywords.length > 0 ? keywords.join(', ') : 'None'}</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default MatchScore
