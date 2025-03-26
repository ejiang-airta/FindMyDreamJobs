//Fetch match score from /match-score
//Display match score percentage & keywords matched

'use client'
import React, { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'

export default function MatchScore() {
  const [resumeId, setResumeId] = useState('')
  const [jobId, setJobId] = useState('')
  const [matchScore, setMatchScore] = useState<number | null>(null)
  const [matchedKeywords, setMatchedKeywords] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleMatchScore = async () => {
    if (!resumeId || !jobId) {
      setError('⚠️ Please enter both Resume ID and Job ID.')
      return
    }
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/match-score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: parseInt(resumeId, 10),
          job_id: parseInt(jobId, 10),
        }),
      })

      const result = await response.json()

      if (response.ok) {
        setMatchScore(result.match_score)
        setMatchedKeywords(result.keywords_matched || [])
      } else {
        setError(`❌ Error: ${result.detail || 'Failed to fetch match score'}`)
      }
    } catch (err) {
      setError('❌ Network error. Please try again.')
    }
  }

  return (
    <Card className="p-6 space-y-4">
      <CardContent>
        <h2 className="text-lg font-bold">🔍 Resume & Job Match Score</h2>

        <Label htmlFor="resumeId">Resume ID</Label>
        <Input id="resumeId" value={resumeId} onChange={(e) => setResumeId(e.target.value)} />

        <Label htmlFor="jobId">Job ID</Label>
        <Input id="jobId" value={jobId} onChange={(e) => setJobId(e.target.value)} />

        <Button className="mt-4 w-full" onClick={handleMatchScore}>
          Calculate Match Score
        </Button>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {matchScore !== null && (
          <div className="mt-4">
            <p className="text-lg">✅ Match Score: <strong>{matchScore}%</strong></p>
            <p className="text-sm">🔹 Matched Keywords: {matchedKeywords.length > 0 ? matchedKeywords.join(', ') : 'None'}</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

