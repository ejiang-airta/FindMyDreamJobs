 //✅ Resume Upload UI
'use client'

import React, { useState } from 'react'
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"

export default function ResumeUploadForm() {
  const [file, setFile] = useState<File | null>(null)
  const [uploadStatus, setUploadStatus] = useState<"idle" | "uploading" | "success" | "error">("idle")

  const handleUpload = async () => {
    if (!file) return

    setUploadStatus("uploading")

    const formData = new FormData()
    formData.append("resume", file)

    try {
      const res = await fetch("http://127.0.0.1:8000/upload-resume", {
        method: "POST",
        body: formData,
      })

      if (res.ok) {
        setUploadStatus("success")
      } else {
        setUploadStatus("error")
      }
    } catch (error) {
      console.error("Upload failed:", error)
      setUploadStatus("error")
    }
  }

  return (
    <Card className="p-6">
      <CardContent className="space-y-4">
        <Label htmlFor="resume">Upload Resume</Label>
        <Input
          type="file"
          id="resume"
          accept=".pdf,.doc,.docx,.txt"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />

        <Button onClick={handleUpload} disabled={!file || uploadStatus === "uploading"}>
          {uploadStatus === "uploading" ? "Uploading..." : "Upload"}
        </Button>

        {uploadStatus === "success" && (
          <Alert variant="default">
            <AlertDescription>✅ Resume uploaded successfully!</AlertDescription>
          </Alert>
        )}
        {uploadStatus === "error" && (
          <Alert variant="destructive">
            <AlertDescription>❌ Upload failed. Please try again.</AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  )
}
