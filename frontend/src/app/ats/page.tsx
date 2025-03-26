'use client'

import React, { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Label } from '@/components/ui/label'

export default function ATSPage() {
  const [resumeId, setResumeId] = useState("")
  const [scoreData, setScoreData] = useState<null | {
    ats_score_before: number
    ats_score_after: number
    message: string
  }>(null)
  const [error, setError] = useState("")

  const handleCheckScore = async () => {
    setError("")
    setScoreData(null)

    if (!resumeId || isNaN(Number(resumeId)) || Number(resumeId) < 1) {
      setError("⚠️ Please enter a valid Resume ID (positive number).")
      return
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/ats-score?resume_id=${resumeId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      })
      
      if (parseInt(resumeId) < 1) {
        setError('Please enter a valid Resume ID (positive integer).');
        return;
      }
      
      if (!response.ok) {
        const errorData = await response.json()
        setError(`❌ Error: ${errorData.detail || 'Failed to fetch ATS score.'}`)
        return
      }

      const data = await response.json()
      setScoreData(data)
    } catch (err: any) {
        if (err.response && err.response.data && err.response.data.error) {
          setError(err.response.data.error)
        } else {
          setError("❌ Network error. Please try again.")
        }
        console.error("API error:", err)
      }
  }

  return (
    <div className="max-w-xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold"> ATS Compliance Checker</h1>
      <p className="text-muted-foreground text-sm">
        Enter your resume ID to check its ATS optimization score before and after enhancement.
      </p>

      <Card>
        <CardContent className="p-6 space-y-4">
          <Label htmlFor="resumeId">Resume ID</Label>
          <Input
            id="resumeId"
            type="number"
            value={resumeId}
            onChange={(e) => setResumeId(e.target.value)}
            placeholder="e.g., 1"
          />

          <Button onClick={handleCheckScore}>
            Check ATS Score
          </Button>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {scoreData && (
            <Alert variant="default">
              <AlertDescription>
                ✅ <strong>Before:</strong> {scoreData.ats_score_before}% &nbsp;
                🔧 <strong>After:</strong> {scoreData.ats_score_after}% <br />
                <span className="text-muted-foreground text-xs">{scoreData.message}</span>
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
