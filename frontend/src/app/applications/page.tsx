//✅ File: /frontend/src/app/applications/page.tsx
// This page is for displaying all the job applications made by the user.
'use client'

import React, { useEffect, useState, useCallback } from 'react' 
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { AppButton } from '@/components/ui/AppButton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Input } from '@/components/ui/input'
import { useUserId } from '@/hooks/useUserId'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { BACKEND_BASE_URL }  from '@/lib/env'
import { Protected } from '@/components/Protected'
import { ChevronDown } from "lucide-react" // Use lucide icon
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
  "Others"
];

// ✅ MOVE FilterDropdown OUTSIDE the ApplicationsPage component
function FilterDropdown({
  options,
  selected,
  appliedSelected,
  onChange,
  open,
  onOpenChange,
  onApply,
}: {
  options: string[]
  selected: string[]
  appliedSelected: string[]
  onChange: (v: string[]) => void
  open: boolean
  onOpenChange: (v: boolean) => void
  onApply: () => void
}) {
  const allSelected = selected.length === options.length

  const toggleAll = useCallback(() => {
    onChange(allSelected ? [] : [...options])
  }, [allSelected, options, onChange])
  
  const toggleOne = useCallback((s: string) => {
    onChange(selected.includes(s) ? selected.filter(x => x !== s) : [...selected, s])
  }, [selected, onChange])
  
  const appliedCount = appliedSelected.length
  const label =
    appliedCount === 0
      ? "Filter (0)"
      : appliedCount === options.length
      ? "Filter (All)"
      : `Filter (${appliedCount})`
  
  const handleCheckboxClick = useCallback((e: React.MouseEvent) => {
    e.stopPropagation()
  }, [])

  return (
    <Popover open={open} onOpenChange={onOpenChange}>
      <PopoverTrigger asChild>
        <Button variant="outline" className="w-[240px] justify-between">
          <span>{label}</span>
          <ChevronDown className="h-4 w-4 opacity-60" />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-64 space-y-3"
        onMouseLeave={() => onOpenChange(false)}   // ✅ close when mouse leaves dropdown
        onInteractOutside={() => onOpenChange(false)} // ✅ close when click outside
      >
        <div className="font-semibold">Status</div>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={allSelected}
            onClick={handleCheckboxClick}
            onChange={toggleAll}
          />
          <span>ALL</span>
        </label>
        <div className="space-y-2">
          {options.map((s) => (
            <label key={s} className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={selected.includes(s)}
                onClick={handleCheckboxClick}
                onChange={() => toggleOne(s)}
              />
              <span>{s}</span>
            </label>
          ))}
        </div>
        <p className="text-xs text-muted-foreground">Multiple selections allowed</p>
        <div className="flex justify-end gap-2 pt-2 border-t">
          <Button variant="outline" size="sm" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <AppButton size="sm" onClick={onApply}>
            Apply
          </AppButton>
        </div>
      </PopoverContent>
    </Popover>
  )
}

// ✅ MOVE SortDropdown OUTSIDE too
function SortDropdown({
  sortBy,
  sortDir,
  onSortByChange,
  onSortDirChange,
}: {
  sortBy: string
  sortDir: "asc" | "desc"
  onSortByChange: (v: any) => void
  onSortDirChange: (v: any) => void
}) {
  return (
    <div className="flex items-center gap-2">
      <Select value={sortBy} onValueChange={(v) => onSortByChange(v)}>
        <SelectTrigger className="w-[240px]">
          <SelectValue placeholder="Sort by" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="applied_date">Applied Date</SelectItem>
          <SelectItem value="match_score">Match Score</SelectItem>
          <SelectItem value="ats_score">ATS Score</SelectItem>
          <SelectItem value="company_name">Company</SelectItem>
          <SelectItem value="job_title">Job Title</SelectItem>
        </SelectContent>
      </Select>
      <Button
        variant="outline"
        size="sm"
        onClick={() => onSortDirChange(sortDir === "asc" ? "desc" : "asc")}
      >
        {sortDir === "asc" ? "Asc" : "Desc"}
      </Button>
    </div>
  )
}

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
  
  // ✅ Filter + Sort (client-side)
  const FILTER_STATUS_OPTIONS = STATUS_OPTIONS // reuse same list
  const [filterStatuses, setFilterStatuses] = useState<string[]>(FILTER_STATUS_OPTIONS) // default ALL selected
  const [sortBy, setSortBy] = useState<'applied_date' | 'match_score' | 'ats_score' | 'company_name' | 'job_title'>('applied_date')
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc')
  const [filterOpen, setFilterOpen] = useState(false)
  const [pendingStatuses, setPendingStatuses] = useState<string[]>(filterStatuses)

  //When user opens popover, we want pending = current:
  useEffect(() => {
    if (filterOpen) setPendingStatuses(filterStatuses)
  }, [filterOpen, filterStatuses])
  
  // Apply button action
  const applyFilter = useCallback(() => {
    setFilterStatuses(pendingStatuses)
    setFilterOpen(false)
  }, [pendingStatuses])

  // Filtered + Sorted applications
  const filteredSortedApplications = React.useMemo(() => {
    const apps = Array.isArray(applications) ? [...applications] : []
    const PREDEFINED = STATUS_OPTIONS.filter(s => s !== "Others")
    const selectedHasOther = filterStatuses.includes("Others")

    // Filter by status
    const filtered =
      filterStatuses.length === 0
        ? []
        : apps.filter((a: any) => {
            const status = (a.application_status ?? "").trim()

            const isPredefined = PREDEFINED.includes(status)

            // Normal statuses: match by exact selection
            if (isPredefined) return filterStatuses.includes(status)

            // Everything else: treated as "Others"
            return selectedHasOther
          })
    // Sorting
      const dir = sortDir === 'asc' ? 1 : -1
      const getNumber = (v: any) => {
        const n = Number(v)
        return Number.isFinite(n) ? n : -Infinity
      }

    filtered.sort((a: any, b: any) => {
      let va: any
      let vb: any

      switch (sortBy) {
        case 'company_name':
          va = (a.company_name ?? '').toString().toLowerCase()
          vb = (b.company_name ?? '').toString().toLowerCase()
          break
        case 'job_title':
          va = (a.job_title ?? '').toString().toLowerCase()
          vb = (b.job_title ?? '').toString().toLowerCase()
          break
        case 'match_score':
          va = getNumber(a.match_score)
          vb = getNumber(b.match_score)
          break
        case 'ats_score':
          va = getNumber(a.ats_score)
          vb = getNumber(b.ats_score)
          break
        case 'applied_date':
        default:
          va = new Date(a.applied_date).getTime()
          vb = new Date(b.applied_date).getTime()
          break
      }

      if (va < vb) return -1 * dir
      if (va > vb) return 1 * dir
      return 0
    })

    return filtered
  }, [applications, filterStatuses, sortBy, sortDir])

  const userId = useUserId()

  useEffect(() => {
    if (!userId) {
      console.warn('⚠ No valid user ID found.')
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
      setError('⚠ Failed to load applications. Please try again later.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleStatusChange = (applicationId: number, status: string) => {
    setSelectedStatus(prev => ({ ...prev, [applicationId]: status }));
    
    // If status is not "Others", update the status value directly
    if (status !== "Others") {
      setUpdateStatus(prev => ({ ...prev, [applicationId]: status }));
    } else {
      // If "Others" is selected, use the custom status if available, or empty string
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
        alert(`⚠ ${result.detail || "Failed to update status."}`);
        return;
      }
  
      alert("✅ Status updated successfully!");
      // Optional: Refresh list
      fetchApplications();
      
      // Reset states for this application
      setSelectedStatus(prev => ({ ...prev, [applicationId]: "" }));
      setCustomStatus(prev => ({ ...prev, [applicationId]: "" }));
    } catch (err) {
      console.error("⚠ Network error:", err);
      alert("⚠ Network error occurred.");
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
        <CardHeader className="space-y-3">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-xl font-bold">🧾 Application History</h2>
            <div className="text-sm text-muted-foreground">
              Showing <strong>{filteredSortedApplications.length}</strong> of{" "}
              <strong>{applications.length}</strong>
            </div>
          </div>

          <div className="flex items-center justify-between gap-3">
            {/* Left: Filter + Apply */}
            <div className="flex items-center gap-3">
              <FilterDropdown
                options={STATUS_OPTIONS}
                selected={pendingStatuses}          // used inside the checkbox list
                appliedSelected={filterStatuses}    // used for the trigger label (freeze)
                onChange={setPendingStatuses}
                open={filterOpen}
                onOpenChange={setFilterOpen}
                onApply={applyFilter}
              />
            </div>

            {/* Right: Sort */}
            <SortDropdown
              sortBy={sortBy}
              sortDir={sortDir}
              onSortByChange={setSortBy}
              onSortDirChange={setSortDir}
            />
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {isLoading ? (
            <Skeleton className="h-10 w-full" />
          ) : applications.length > 0 ? (
            filteredSortedApplications.map((app: any) => (
              <div key={app.application_id} className="border p-4 rounded-md">
                <p><strong>📄 Job #:</strong>{app.job_id}: {app.job_title}</p>
                <p><strong>🏢 Company:</strong> {app.company_name}{/* Add a few non-breaking spaces here */}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>📍 Location:</strong> {app.location}</p>
                <p><strong>💰 Salary Range:</strong> {app.salary ?? 'Unknown'}</p>
                <p><strong>👥 # of Applicants:</strong> {app.applicants_count ?? "Unknown"}</p>
                {(() => {
                  const url = (app.job_link ?? "").trim() || (app.application_url ?? "").trim()
                  return (
                    <p>
                      <strong>🔗 URL: </strong>
                      {url ? (
                        <a href={url} target="_blank" rel="noreferrer" className="text-blue-600 underline break-all">
                          {url}
                        </a>
                      ) : (
                        <span className="text-muted-foreground">N/A</span>
                      )}
                    </p>
                  )
                })()}
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
                        alert("⚠ Failed to download resume.")
                        console.error(err)
                      }
                    }}
                  >
                    ⬇️ Download 
                  </Button>
                </p>
                <p><strong>📅 Date Applied:</strong> {new Date(app.applied_date).toLocaleDateString()}</p>
                <div className="mt-2">
                  <p className="mt-2">
                    <strong>📈 Scores:</strong>{" "}
                    <Badge className="ml-2">Match: {app.match_score ?? "—"}%</Badge>
                    <Badge className="ml-2">ATS: {app.ats_score ?? "—"}%</Badge>
                  </p>
                  <p><strong>📊 Status:</strong> <Badge>{app.application_status}</Badge></p>
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
                          <SelectItem key={status} value={status}>{status}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    
                    {selectedStatus[app.application_id] === "Others" && (
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
            ))
          ) : (
            <p className="text-muted-foreground">No applications found.</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}