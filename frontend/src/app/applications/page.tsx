//frontend/src/app/applications/page.tsx
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

export default function ApplicationsPage() {
  const [applications, setApplications] = useState([])
  const [error, setError] = useState('')
  const [updateStatus, setUpdateStatus] = useState<{ [key: number]: string }>({})


  const userId = 1 // 🔐 Hardcoded for now until auth is added

  useEffect(() => {
    fetchApplications()
  }, [])

  const fetchApplications = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/applications/${userId}`)
      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Failed to fetch applications.')
      }

      setApplications(data)
    } catch (err) {
      setError('❌ Failed to load applications. Please try again later.')
    }
  }
  const handleStatusUpdate = async (applicationId: number) => {
    const newStatus = updateStatus[applicationId]
  
    if (!newStatus || newStatus.trim() === '') {
      alert("⚠️ Please enter a status before updating.")
      return
    }
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/update-application-status?application_id=${applicationId}&status=${encodeURIComponent(newStatus.trim())}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          application_id: applicationId,
          status: newStatus.trim()
        })
      })
  
      const result = await response.json()
  
      if (!response.ok) {
        alert(`❌ ${result.detail || "Failed to update status."}`)
        return
      }
  
      alert("✅ Status updated successfully!")
      // Optional: Refresh list
      fetchApplications()
    } catch (err) {
      console.error("❌ Network error:", err)
      alert("❌ Network error occurred.")
    }
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">📌 Your Job Applications</h1>
      <p className="text-muted-foreground text-sm">
        A list of jobs you've applied to, including the job title, company, and application status.
      </p>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <h2 className="text-xl font-bold">🧾 Application History</h2>
        </CardHeader>
        <CardContent className="space-y-4">
          {applications.length > 0 ? (
            applications.map((app: any) => (
              <div key={app.application_id} className="border p-4 rounded-md">
                <p><strong>📄 Job Title:</strong> {app.job_title}</p>
                <p><strong>🏢 Company:</strong> {app.company_name}</p>
                <p><strong>📝 Resume ID:</strong> {app.resume_id}     
                <Button
                    className="ml-8"  // <-- adds left margin (space)
                    variant="outline"
                    size="sm"
                    onClick={async () => {
                        try {
                        const res = await fetch(`http://127.0.0.1:8000/download-resume/${app.resume_id}`)
                        const blob = await res.blob()
                        const url = window.URL.createObjectURL(blob)
                        const a = document.createElement('a')
                        a.href = url
                        a.download = `resume_${app.resume_id}.txt`
                        a.click()
                        window.URL.revokeObjectURL(url)
                        } catch (err) {
                        alert("❌ Failed to download resume.")
                        console.error(err)
                        }
                    }}
                    >
                    ⬇️ Download 
                    </Button>
                </p>
                <p><strong>🔗 URL:</strong> <a href={app.application_url} target="_blank" className="text-blue-600 underline">{app.application_url}</a></p>
                <p><strong>📅 Date Applied:</strong> {new Date(app.applied_date).toLocaleDateString()}</p>
                <p>
                  <strong>📊 Status:</strong> {app.application_status}
                  <Input
                    className="mt-2"
                    type="text"
                    placeholder="Update status (e.g., Offered)"
                    value={updateStatus[app.application_id] || ''}
                    onChange={(e) => setUpdateStatus(prev => ({ ...prev, [app.application_id]: e.target.value }))}
                  />
                  <Button
                    size="sm"
                    className="mt-2"
                    onClick={() => {
                      console.log("Updating status for:", app.application_id, "New status:", updateStatus[app.application_id])
                      handleStatusUpdate(app.application_id)
                  }}
                  >
                    🔄 Update
                  </Button>
                </p>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No applications found.</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
