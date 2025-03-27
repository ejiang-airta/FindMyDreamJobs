/* ATSScore component features:
Fetch ATS score from /ats-score
Display before & after scores
*/
'use client'
import React, { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'

export default function ATSScore() {
  const [resumeId, setResumeId] = useState('')
  const [atsBefore, setAtsBefore] = useState<number | null>(null)
  const [atsAfter, setAtsAfter] = useState<number | null>(null)
  const [error, setError] = useState<string | null>(null)

  const fetchATSScore = async () => {
    if (!resumeId) {
      setError('⚠️ Please enter a Resume ID.')
      return
    }
    setError(null)

    try {
      const response = await fetch(`http://localhost:8000/ats-score?resume_id=${resumeId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })

      const result = await response.json()

      if (response.ok) {
        setAtsBefore(result.ats_score_initial)
        setAtsAfter(result.ats_score_final)
      } else {
        setError(`❌ Error: ${result.detail || 'Failed to fetch ATS score'}`)
      }
    } catch (err) {
      setError('❌ Network error. Please try again.')
    }
  }

  return (
    <Card className="p-6 space-y-4">
      <CardContent>
        <h2 className="text-lg font-bold">📊 Resume ATS Score</h2>

        <Label htmlFor="resumeId">Resume ID</Label>
        <Input id="resumeId" value={resumeId} onChange={(e) => setResumeId(e.target.value)} />

        <Button className="mt-4 w-full" onClick={fetchATSScore}>
          Check ATS Score
        </Button>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {atsBefore !== null && atsAfter !== null && (
          <div className="mt-4">
            <p className="text-lg">📌 **Before Optimization:** <strong>{atsBefore}%</strong></p>
            <p className="text-lg">✅ **After Optimization:** <strong>{atsAfter}%</strong></p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
