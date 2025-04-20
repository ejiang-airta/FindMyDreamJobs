//✅ File: frontend/src/components/UploadResume.tsx
// This component is for uploading resumes.
'use client'

import React, { useState, useEffect, useRef  } from 'react'
import { useSession } from 'next-auth/react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { BACKEND_BASE_URL }  from '@/lib/env'
import { toast } from 'sonner'


interface Props {
  onSuccess?: () => void
  isWizard?: boolean // ✅ Accept wizard prop (optional)
}

const UploadResume: React.FC<Props> = ({ onSuccess, isWizard }) => {
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [userId, setUserId] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const { data: session, status } = useSession() as { data: { status?: string; resume_name?: string } | null; status: string }

  useEffect(() => {
    // Only runs in the browser
    const id = localStorage.getItem('user_id')
    setUserId(id)
  }, [])

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
      const response = await fetch(`${BACKEND_BASE_URL}/upload-resume`, {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

   // ✅ Check for duplicate resume from backend response:
   if (data.status === "duplicate") {
    toast.warning(`You've already uploaded "${data.resume_name}".`)
    const confirmUpload = window.confirm("The resume already exists. Do you want to upload a new version of this resume?")
    if (!confirmUpload) return

    // Append timestamp to filename and retry
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
      return
    }

    toast.success(`✅ Resume uploaded successfully as ${newFilename} (new version)!`)
    if (onSuccess) onSuccess()
    return
  }

  // Normal upload path
      if (!response.ok) {
        setError(data.detail || "Upload failed.")
      } else {
        // notify the successfully upload:
        toast.success('✅ Resume uploaded successfully!')
        // if it's in Top Nav, we allow user to upload multiple times:
        if (!isWizard) {
          setFile(null)
          if (fileInputRef.current) fileInputRef.current.value = ''
        }

        // ✅ Success: notify parent if in wizard mode
        if (onSuccess) onSuccess()
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
      <Button className="w-full" onClick={handleUpload} disabled={isUploading} >
        {isUploading ? 'Uploading...' : 'Upload Resume'}
      </Button>
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}      
    </div>
  )
}

export default UploadResume
