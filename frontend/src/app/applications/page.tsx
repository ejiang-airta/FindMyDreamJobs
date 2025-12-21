//✅ File: /frontend/src/app/applications/page.tsx
// This page is for displaying all the job applications made by the user.
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { AppButton } from '@/components/ui/AppButton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Input } from '@/components/ui/input'
import { useUserId } from '@/hooks/useUserId'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { BACKEND_BASE_URL }  from '@/lib/env'
import { Protected } from '@/components/Protected'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

// Predefined status options for the dropdown
const STATUS_OPTIONS = [
  "In Progress",
  "Application Submitted",
  "Under Review",
  "Rejected",
  "Interview",
  "Offered",
  "Other"
];

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  return (
    <Protected>
      <ApplicationsPage />
    </Protected>
  )
}

// This component is the main page for displaying all the job applications made by the user:
// It fetches the applications from the backend and allows the user to update the status of each application.
function ApplicationsPage() {
  const [applications, setApplications] = useState([])
  const [error, setError] = useState('')
  const [updateStatus, setUpdateStatus] = useState<{ [key: number]: string }>({})
  const [selectedStatus, setSelectedStatus] = useState<{ [key: number]: string }>({})
  const [customStatus, setCustomStatus] = useState<{ [key: number]: string }>({})
  const [isLoading, setIsLoading] = useState(false)
  const [updatingStatus, setUpdatingStatus] = useState<{ [key: number]: boolean }>({})

  const userId = useUserId()

  useEffect(() => {
    if (!userId) {
      console.warn('❌ No valid user ID found.')
      return
    }
    fetchApplications()
  }, [userId])


  const fetchApplications = async () => {
    setIsLoading(true)
    try {
      const res = await fetch(`${BACKEND_BASE_URL}/applications/${userId}`)
      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Failed to fetch applications.')
      }

      setApplications(data)
    } catch (err) {
        setError('❌ Failed to load applications. Please try again later.')
    } finally {
        setIsLoading(false)
    }
  }

  const handleStatusChange = (applicationId: number, status: string) => {
    setSelectedStatus(prev => ({ ...prev, [applicationId]: status }));
    
    // If status is not "Other", update the status value directly
    if (status !== "Other") {
      setUpdateStatus(prev => ({ ...prev, [applicationId]: status }));
    } else {
      // If "Other" is selected, use the custom status if available, or empty string
      setUpdateStatus(prev => ({ 
        ...prev, 
        [applicationId]: customStatus[applicationId] || '' 
      }));
    }
  };

  const handleCustomStatusChange = (applicationId: number, value: string) => {
    setCustomStatus(prev => ({ ...prev, [applicationId]: value }));
    setUpdateStatus(prev => ({ ...prev, [applicationId]: value }));
  };
  
  const handleStatusUpdate = async (applicationId: number) => {
    const newStatus = updateStatus[applicationId];
  
    if (!newStatus || newStatus.trim() === '') {
      alert("⚠️ Please enter a status before updating.");
      return;
    }
  
    setUpdatingStatus(prev => ({ ...prev, [applicationId]: true }));
    
    try {
      const response = await fetch(`${BACKEND_BASE_URL}/update-application-status?application_id=${applicationId}&status=${encodeURIComponent(newStatus.trim())}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          application_id: applicationId,
          status: newStatus.trim()
        })
      });
  
      const result = await response.json();
  
      if (!response.ok) {
        alert(`❌ ${result.detail || "Failed to update status."}`);
        return;
      }
  
      alert("✅ Status updated successfully!");
      // Optional: Refresh list
      fetchApplications();
      
      // Reset states for this application
      setSelectedStatus(prev => ({ ...prev, [applicationId]: "" }));
      setCustomStatus(prev => ({ ...prev, [applicationId]: "" }));
    } catch (err) {
      console.error("❌ Network error:", err);
      alert("❌ Network error occurred.");
    } finally {
      setUpdatingStatus(prev => ({ ...prev, [applicationId]: false }));
    }
  };
  
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
        {isLoading ? (
            <Skeleton className="h-10 w-full" />
          ) : applications.length > 0 ? (
            applications.map((app: any) => (
              <div key={app.application_id} className="border p-4 rounded-md">
                <p><strong>📄 Job #:</strong>{app.job_id}: {app.job_title}</p>
                <p><strong>🏢 Company:</strong> {app.company_name}{/* Add a few non-breaking spaces here */}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>📍 Location:</strong> {app.location}</p>
                <p><strong>💰 Salary Range:</strong> {app.salary ?? 'Unknown'}</p>
                <p><strong>👥 # of Applicants:</strong> {app.applicants_count ?? "Unknown"}</p>
                <p><strong>📄 Resume #:</strong> {app.resume_id}: {app.resume_name || 'Unnamed'}
                <Button
                    className="ml-8"  // <-- adds left margin (space)
                    variant="outline"
                    size="sm"
                    onClick={async () => {
                        try {
                        const res = await fetch(`${BACKEND_BASE_URL}/download-resume/${app.resume_id}`)
                        
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
                <div className="mt-2">
                  <div className="mt-2">
                    <p className="mt-2">
                      <strong>📈 Scores:</strong>{" "}
                      <Badge className="ml-2">
                        Match: {app.match_score ?? "—"}%
                      </Badge>
                      <Badge className="ml-2">
                        ATS: {app.ats_score ?? "—"}%
                      </Badge>
                    </p>
                                        <p>
                      <strong>📊 Status:</strong> <Badge>{app.application_status}</Badge>
                    </p>
                    <div className="space-y-2 mt-2">
                      <Select
                        value={selectedStatus[app.application_id] || ""}
                        onValueChange={(value) => handleStatusChange(app.application_id, value)}
                      >
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Select new status" />
                        </SelectTrigger>
                        <SelectContent>
                          {STATUS_OPTIONS.map((status) => (
                            <SelectItem key={status} value={status}>
                              {status}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      
                      {selectedStatus[app.application_id] === "Other" && (
                        <Input
                          type="text"
                          placeholder="Enter custom status"
                          value={customStatus[app.application_id] || ''}
                          onChange={(e) => handleCustomStatusChange(app.application_id, e.target.value)}
                        />
                      )}
                      
                      <AppButton
                        size="sm"
                        className="mt-2"
                        disabled={updatingStatus[app.application_id] || !updateStatus[app.application_id]}
                        onClick={() => handleStatusUpdate(app.application_id)}
                      >
                        {updatingStatus[app.application_id] ? "Updating..." : "🔄 Update"}
                      </AppButton>
                    </div>
                  </div>
                </div>
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