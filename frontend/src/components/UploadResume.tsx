//✅ Resume Upload UI
'use client'

import React, { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'

const UploadResume: React.FC = () => {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<string | null>(null)

  const handleUpload = async () => {
    if (!file) {
      setStatus('Please select a file to upload.')
      return
    }

    const formData = new FormData()
    formData.append("file", file) // ✅ MUST use "file"
    formData.append("user_id", "1")  // 👈 Add this line!


    try {
      const response = await fetch('http://localhost:8000/upload-resume', {
        method: 'POST',
        body: formData,
      })

      const result = await response.json()

      if (response.ok) {
        setStatus(`✅ Upload successful! Resume ID: ${result.resume_id}`)
      } else {
        setStatus(`❌ Upload failed: ${result.detail || 'Unknown error.'}`)
      }
    } catch (err: any) {
      const message = err?.response?.data?.error || err.message || "Unexpected error occurred."
      console.error("Upload error:", err)
      setError(message)
    }
  }

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md space-y-4">
      <h2 className="text-2xl font-semibold">Upload Resume</h2>

      <div className="space-y-2">
        <Label htmlFor="resumeFile">Select Resume File</Label>
        <Input
          id="resumeFile"
          type="file"
          accept=".pdf,.doc,.docx,.txt"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
      </div>

      <Button className="w-full mt-4" onClick={handleUpload}>
        Upload Resume
      </Button>

      {status && (
        <Alert variant="destructive">
          <AlertDescription>{status}</AlertDescription>
        </Alert>
      )}
    </div>
  )
}

export default UploadResume
