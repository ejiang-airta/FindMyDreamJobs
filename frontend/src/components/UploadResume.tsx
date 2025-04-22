//✅ File: frontend/src/components/UploadResume.tsx
// This component is for uploading resumes.
'use client'

import React, { useState, useEffect, useRef } from 'react'
import { useSession } from 'next-auth/react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { BACKEND_BASE_URL } from '@/lib/env'
import { useUserId } from '@/hooks/useUserId'
import { toast } from 'sonner'
import { AppButton } from '@/components/ui/AppButton'

interface Props {
  onSuccess?: () => void
  isWizard?: boolean
}

const UploadResume: React.FC<Props> = ({ onSuccess, isWizard }) => {
  const userId = useUserId()
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const { data: session, status } = useSession()

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  const resetUploadState = () => {
    setFile(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const handleUpload = async () => {
    if (!file) return setError("Please choose a file before uploading.")
    if (!userId) return setError("User not found in session. Please log in again.")

    setIsUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append("file", file)
    formData.append("user_id", userId)

    try {
      const response = await fetch(`${BACKEND_BASE_URL}/upload-resume`, {
        method: "POST",
        body: formData,
      })

      let data: any = {}
      try {
        data = await response.json()
      } catch (err) {
        data = { detail: await response.text() }
      }

      if (data.status === "duplicate") {
        toast(
          `You've already uploaded "${data.resume_name} previously".`,
          {
            description: "Do you want to upload a newer version?",
            icon: "⚠️",
            duration: Infinity, // ✅ stays on screen
            action: {
              label: "Yes",
              onClick: async () => {
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
                const newFilename = `${file.name.replace(/\.[^/.]+$/, "")}_${timestamp}${file.name.slice(file.name.lastIndexOf("."))}`
        
                const retryFormData = new FormData()
                retryFormData.append("file", file)
                retryFormData.append("user_id", userId)
                retryFormData.append("resume_name", newFilename)
        
                const retryRes = await fetch(`${BACKEND_BASE_URL}/upload-resume`, {
                  method: "POST",
                  body: retryFormData,
                })
        
                const retryData = await retryRes.json()
        
                if (!retryRes.ok) {
                  setError(retryData.detail || "Upload failed.")
                  setIsUploading(false)
                  return
                }
        
                toast.success(`✅ Resume uploaded as "${newFilename}"`, { icon: null })
                if (!isWizard) resetUploadState()
                onSuccess?.()
                setIsUploading(false)
              },
            },
            cancel: {
              label: "No",
              onClick: () => {
                if (!isWizard) resetUploadState()
                setIsUploading(false)
                toast.info("Upload canceled.", { icon: "⚠️" })
              },
            },
          }
        )

        setIsUploading(false)
        return
      }

      // Normal upload success
      if (!response.ok) {
        setError(data.detail || "Upload failed.")
      } else {
        toast.success('Resume uploaded successfully!', { icon: "✅ " })
        if (!isWizard) resetUploadState()
        onSuccess?.()
      }
    } catch (err) {
      setError("❌ Upload failed. Please try again.")
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow space-y-4">
      <h2 className="text-2xl font-semibold">Upload Your Resume</h2>
      <label className="font-bold" htmlFor="resume-upload">Select a file:</label>
      <Input
        id="resume-upload"
        ref={fileInputRef}
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={handleFileChange}
        className="cursor-pointer"
      />

      {!file && !isWizard && (
        <p className="text-sm text-muted-foreground">📎 Click above to choose a resume file (.pdf,.docx,.txt)</p>
      )}

      {file && !isWizard && (
        <p className="text-sm text-green-700">✅ Selected: {file.name}</p>
      )}

      <AppButton onClick={handleUpload} disabled={isUploading}>
        {isUploading ? 'Uploading...' : 'Upload Resume'}
      </AppButton>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  )
}

export default UploadResume
