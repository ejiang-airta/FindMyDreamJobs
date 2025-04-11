//✅ File: frontend/src/components/UploadResume.tsx
// This component is for uploading resumes.
import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Alert, AlertDescription } from '@/components/ui/alert'

interface Props {
  onSuccess?: () => void
  isWizard?: boolean // ✅ Accept wizard prop (optional)
}

const UploadResume: React.FC<Props> = ({ onSuccess, isWizard }) => {
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
  )
}

export default UploadResume
