// ✅ File: frontend/src/app/upload/page.tsx
// This page is for uploading resumes.

'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Alert, AlertDescription } from '@/components/ui/alert'

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)

  const userId = localStorage.getItem("user_id")

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError("Please choose a file before uploading.")
      return
    }
    if (!userId) {
      setError("User not found in session. Please log in again.")
      return
    }

    setIsUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append("file", file)
    formData.append("user_id", userId)

    try {
      const response = await fetch("http://localhost:8000/upload-resume", {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.detail || "Upload failed.")
      } else {
        alert("✅ Resume uploaded successfully!")
        setFile(null)
      }
    } catch (err) {
      setError("❌ Upload failed. Please try again.")
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-6 px-4">
      <h1 className="text-2xl font-bold">📤 Upload Your Resume</h1>
      <div className="bg-white shadow-md rounded p-6 space-y-4">
        <Input type="file" accept=".pdf,.docx,.txt" onChange={handleFileChange} />
        <Button className="w-full" onClick={handleUpload} disabled={isUploading}>
          {isUploading ? 'Uploading...' : 'Upload Resume'}
        </Button>
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  )
}
