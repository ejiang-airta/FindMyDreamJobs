// File: frontend/src/app/jdi/setup/page.tsx
// JDI Setup page — Gmail OAuth connect + source/resume preferences
"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { CheckCircle2, Circle, Mail, X, Plus, Upload, ArrowLeft } from "lucide-react"
import { toast } from "sonner"
import axios from "axios"
import { BACKEND_BASE_URL } from "@/lib/env"
import { AppButton } from "@/components/ui/AppButton"
import { Protected } from "@/components/Protected"
import {
  getGmailConnectUrl,
  getGmailStatus,
  revokeGmailIntegration,
  getUserProfile,
  updateUserProfile,
  type GmailIntegrationStatus,
  type UserProfile,
} from "@/lib/jdi-api"

export default function ProtectedPage() {
  return (
    <Protected>
      <JDISetupPage />
    </Protected>
  )
}

interface ResumeOption {
  id: number
  name: string
}

const AVAILABLE_SOURCES = [
  { key: "linkedin", label: "LinkedIn", description: "jobalerts-noreply@linkedin.com" },
  { key: "indeed", label: "Indeed", description: "alert@indeed.com" },
  { key: "trueup", label: "TrueUp", description: "hello@trueup.io" },
  { key: "other", label: "Others", description: "Glassdoor, Talent.com, etc." },
]

const SCAN_WINDOW_OPTIONS = [
  { days: 1, label: "1 day" },
  { days: 2, label: "2 days" },
  { days: 3, label: "3 days" },
  { days: 5, label: "5 days" },
  { days: 7, label: "7 days" },
]

function JDISetupPage() {
  const router = useRouter()
  const [userId, setUserId] = useState<string | null>(null)
  const [gmailStatus, setGmailStatus] = useState<GmailIntegrationStatus | null>(null)
  const [gmailLoading, setGmailLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  // Preferences state
  const [selectedSources, setSelectedSources] = useState<string[]>(["linkedin", "indeed", "trueup", "other"])
  const [selectedResumeIds, setSelectedResumeIds] = useState<number[]>([])
  const [minScore, setMinScore] = useState(60)
  const [scanWindowDays, setScanWindowDays] = useState(7)
  const [customSourcePatterns, setCustomSourcePatterns] = useState<string[]>([])
  const [newCustomPattern, setNewCustomPattern] = useState("")
  const [resumes, setResumes] = useState<ResumeOption[]>([])
  const [selectedDropdownResume, setSelectedDropdownResume] = useState<number | "">("")

  // Load user data on mount
  useEffect(() => {
    const uid = localStorage.getItem("user_id")
    if (!uid) return
    setUserId(uid)

    // Load Gmail status
    getGmailStatus(uid)
      .then(status => setGmailStatus(status))
      .catch(() => setGmailStatus(null))
      .finally(() => setGmailLoading(false))

    // Load existing profile
    getUserProfile(uid)
      .then(profile => {
        if (profile) {
          if (profile.jdi_sources_enabled) setSelectedSources(profile.jdi_sources_enabled)
          if (profile.jdi_base_resume_ids) setSelectedResumeIds(profile.jdi_base_resume_ids)
          if (profile.jdi_min_score) setMinScore(profile.jdi_min_score)
          if (profile.jdi_scan_window_days) setScanWindowDays(profile.jdi_scan_window_days)
          if (profile.jdi_custom_source_patterns) setCustomSourcePatterns(profile.jdi_custom_source_patterns)
        }
      })
      .catch(() => {}) // 404 is fine — no profile yet

    // Load user resumes
    axios.get(`${BACKEND_BASE_URL}/resumes/by-user/${uid}`)
      .then(res => {
        const data = res.data || []
        setResumes(data.map((r: any) => ({ id: r.id, name: r.resume_name || `Resume #${r.id}` })))
      })
      .catch(() => setResumes([]))
  }, [])

  // Check for Gmail OAuth callback redirect
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    if (params.get("jdi_connected") === "true") {
      toast.success("Gmail connected successfully!")
      // Refresh status
      if (userId) {
        getGmailStatus(userId).then(status => setGmailStatus(status))
      }
      // Clean URL
      router.replace("/jdi/setup")
    } else if (params.get("jdi_error") === "true") {
      toast.error("Failed to connect Gmail. Please try again.")
      // Clean URL
      router.replace("/jdi/setup")
    }
  }, [userId, router])

  const handleGmailConnect = async () => {
    if (!userId) return
    try {
      const authUrl = await getGmailConnectUrl(userId)
      window.location.href = authUrl
    } catch (err) {
      console.error("Failed to get Gmail connect URL:", err)
      toast.error("Failed to initiate Gmail connection")
    }
  }

  const handleGmailRevoke = async () => {
    if (!userId) return
    try {
      await revokeGmailIntegration(userId)
      setGmailStatus(prev => prev ? { ...prev, status: "revoked" } : null)
      toast.success("Gmail disconnected")
    } catch (err) {
      console.error("Failed to revoke Gmail:", err)
      toast.error("Failed to disconnect Gmail")
    }
  }

  const handleSourceToggle = (source: string) => {
    setSelectedSources(prev =>
      prev.includes(source) ? prev.filter(s => s !== source) : [...prev, source]
    )
  }

  const handleAddResume = () => {
    if (selectedDropdownResume === "" || selectedDropdownResume === null) return
    const resumeId = Number(selectedDropdownResume)
    if (selectedResumeIds.includes(resumeId)) {
      toast.error("Resume already selected")
      return
    }
    if (selectedResumeIds.length >= 3) {
      toast.error("Maximum 3 base resumes allowed")
      return
    }
    setSelectedResumeIds(prev => [...prev, resumeId])
    setSelectedDropdownResume("")
  }

  const handleRemoveResume = (resumeId: number) => {
    setSelectedResumeIds(prev => prev.filter(id => id !== resumeId))
  }

  const handleAddCustomPattern = () => {
    const pattern = newCustomPattern.trim()
    if (!pattern) return
    if (!pattern.includes("@")) {
      toast.error("Please enter a valid email address")
      return
    }
    if (customSourcePatterns.includes(pattern)) {
      toast.error("Pattern already added")
      return
    }
    setCustomSourcePatterns(prev => [...prev, pattern])
    setNewCustomPattern("")
  }

  const handleRemoveCustomPattern = (pattern: string) => {
    setCustomSourcePatterns(prev => prev.filter(p => p !== pattern))
  }

  const handleSave = async () => {
    if (!userId) return
    setSaving(true)
    try {
      await updateUserProfile(userId, {
        jdi_sources_enabled: selectedSources,
        jdi_base_resume_ids: selectedResumeIds,
        jdi_min_score: minScore,
        jdi_scan_window_days: scanWindowDays,
        jdi_custom_source_patterns: customSourcePatterns.length > 0 ? customSourcePatterns : null,
      })
      toast.success("JDI preferences saved!")
      // Navigate to Jobs page (JDI tab) after save
      router.push("/jobs?tab=jdi")
    } catch (err) {
      console.error("Failed to save preferences:", err)
      toast.error("Failed to save preferences")
    } finally {
      setSaving(false)
    }
  }

  const isGmailActive = gmailStatus?.status === "active"

  // Get resume name by ID
  const getResumeName = (id: number) => {
    const resume = resumes.find(r => r.id === id)
    return resume?.name || `Resume #${id}`
  }

  // Get available resumes for dropdown (not already selected)
  const availableResumes = resumes.filter(r => !selectedResumeIds.includes(r.id))

  return (
    <div className="px-6 py-10 max-w-3xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center gap-3">
        <button onClick={() => router.push("/jobs")} className="text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-3xl font-bold">Job Daily Intelligence</h1>
          <p className="text-muted-foreground">Set up your automated job scanning preferences</p>
        </div>
      </div>

      {/* Step 1: Gmail Connection */}
      <div className="rounded-lg border bg-white p-6 space-y-4">
        <div className="flex items-center gap-2">
          {isGmailActive ? (
            <CheckCircle2 className="h-5 w-5 text-green-600" />
          ) : (
            <Circle className="h-5 w-5 text-gray-300" />
          )}
          <h2 className="text-lg font-semibold">Step 1: Connect Gmail</h2>
        </div>
        <p className="text-sm text-muted-foreground">
          JDI needs read-only access to your Gmail to scan job alert emails.
          We only read emails from job platforms — nothing else.
        </p>

        {gmailLoading ? (
          <p className="text-sm text-muted-foreground">Checking connection...</p>
        ) : isGmailActive ? (
          <div className="flex items-center gap-3">
            <span className="text-sm text-green-700 bg-green-50 px-3 py-1 rounded-md">
              <Mail className="inline h-4 w-4 mr-1" /> Gmail Connected
            </span>
            {gmailStatus?.last_sync_at && (
              <span className="text-xs text-muted-foreground">
                Last scan: {new Date(gmailStatus.last_sync_at).toLocaleString()}
              </span>
            )}
            <AppButton variant="ghost" size="sm" onClick={handleGmailRevoke}>
              Disconnect
            </AppButton>
          </div>
        ) : (
          <AppButton onClick={handleGmailConnect}>
            <Mail className="h-4 w-4 mr-2" /> Connect Gmail
          </AppButton>
        )}
      </div>

      {/* Step 2: Job Sources */}
      <div className="rounded-lg border bg-white p-6 space-y-4">
        <div className="flex items-center gap-2">
          {selectedSources.length > 0 ? (
            <CheckCircle2 className="h-5 w-5 text-green-600" />
          ) : (
            <Circle className="h-5 w-5 text-gray-300" />
          )}
          <h2 className="text-lg font-semibold">Step 2: Select Job Alert Sources</h2>
        </div>
        <p className="text-sm text-muted-foreground">
          Choose which job platforms to scan for alerts in your inbox.
        </p>
        <div className="space-y-2">
          {AVAILABLE_SOURCES.map(source => (
            <label
              key={source.key}
              className="flex items-center gap-3 p-3 rounded-md border cursor-pointer hover:bg-gray-50 transition"
            >
              <input
                type="checkbox"
                checked={selectedSources.includes(source.key)}
                onChange={() => handleSourceToggle(source.key)}
                className="h-4 w-4 text-blue-600 rounded"
              />
              <div>
                <span className="font-medium">{source.label}</span>
                <span className="text-xs text-muted-foreground ml-2">({source.description})</span>
              </div>
            </label>
          ))}
        </div>

        {/* Custom Source Patterns (shown when "Others" is selected) */}
        {selectedSources.includes("other") && (
          <div className="mt-4 pt-4 border-t">
            <p className="text-sm font-medium mb-2">Custom Email Patterns</p>
            <p className="text-xs text-muted-foreground mb-3">
              Add email addresses from other job alert services you use.
            </p>
            <div className="flex gap-2 mb-3">
              <input
                type="email"
                value={newCustomPattern}
                onChange={(e) => setNewCustomPattern(e.target.value)}
                placeholder="e.g., alerts@mycompany.com"
                className="flex-1 px-3 py-2 border rounded-md text-sm"
                onKeyDown={(e) => e.key === "Enter" && handleAddCustomPattern()}
              />
              <AppButton variant="secondary" size="sm" onClick={handleAddCustomPattern}>
                <Plus className="h-4 w-4" />
              </AppButton>
            </div>
            {customSourcePatterns.length > 0 && (
              <div className="space-y-1">
                {customSourcePatterns.map(pattern => (
                  <div key={pattern} className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded-md text-sm">
                    <span>{pattern}</span>
                    <button
                      onClick={() => handleRemoveCustomPattern(pattern)}
                      className="text-gray-400 hover:text-red-500"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Step 3: Base Resumes */}
      <div className="rounded-lg border bg-white p-6 space-y-4">
        <div className="flex items-center gap-2">
          {selectedResumeIds.length > 0 ? (
            <CheckCircle2 className="h-5 w-5 text-green-600" />
          ) : (
            <Circle className="h-5 w-5 text-gray-300" />
          )}
          <h2 className="text-lg font-semibold">Step 3: Choose Base Resumes</h2>
        </div>
        <p className="text-sm text-muted-foreground">
          Select up to 3 resumes to score incoming jobs against. JDI will automatically
          pick the best match for each job.
        </p>

        {/* Selected Resumes Display */}
        <div className="border rounded-md p-4 bg-gray-50 min-h-[80px]">
          <p className="text-xs font-medium text-gray-500 mb-2">Selected Resumes:</p>
          {selectedResumeIds.length === 0 ? (
            <p className="text-sm text-muted-foreground italic">
              Please select default resumes to enable job matching.
            </p>
          ) : (
            <div className="space-y-2">
              {selectedResumeIds.map(id => (
                <div key={id} className="flex items-center justify-between bg-white px-3 py-2 rounded-md border">
                  <span className="text-sm font-medium">{getResumeName(id)}</span>
                  <button
                    onClick={() => handleRemoveResume(id)}
                    className="text-gray-400 hover:text-red-500"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Resume Dropdown + Add */}
        {resumes.length > 0 && selectedResumeIds.length < 3 && (
          <div className="flex gap-2 items-center">
            <select
              value={selectedDropdownResume}
              onChange={(e) => setSelectedDropdownResume(e.target.value ? Number(e.target.value) : "")}
              className="flex-1 px-3 py-2 border rounded-md text-sm bg-white"
            >
              <option value="">Select a resume...</option>
              {availableResumes.map(resume => (
                <option key={resume.id} value={resume.id}>
                  {resume.name}
                </option>
              ))}
            </select>
            <AppButton
              variant="secondary"
              size="sm"
              onClick={handleAddResume}
              disabled={selectedDropdownResume === ""}
            >
              <Plus className="h-4 w-4 mr-1" /> Add
            </AppButton>
          </div>
        )}

        {/* Upload New Resume Button */}
        <AppButton
          variant="ghost"
          size="sm"
          onClick={() => router.push("/upload")}
          className="text-blue-600"
        >
          <Upload className="h-4 w-4 mr-2" /> Upload New Resume
        </AppButton>
      </div>

      {/* Step 4: Minimum Match Score */}
      <div className="rounded-lg border bg-white p-6 space-y-4">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="h-5 w-5 text-green-600" />
          <h2 className="text-lg font-semibold">Step 4: Set Minimum Match Score</h2>
        </div>
        <p className="text-sm text-muted-foreground">
          Only show jobs that score above this threshold. Lower = more results, higher = better quality.
        </p>
        <div className="flex items-center gap-4">
          <input
            type="range"
            min={0}
            max={100}
            step={5}
            value={minScore}
            onChange={e => setMinScore(parseInt(e.target.value))}
            className="flex-1"
          />
          <span className="text-lg font-bold text-blue-700 w-12 text-center">{minScore}%</span>
        </div>
        <div className="flex justify-between text-xs text-muted-foreground px-1">
          <span>More results</span>
          <span>Higher quality</span>
        </div>
      </div>

      {/* Step 5: Email Scan Window */}
      <div className="rounded-lg border bg-white p-6 space-y-4">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="h-5 w-5 text-green-600" />
          <h2 className="text-lg font-semibold">Step 5: Email Scan Window</h2>
        </div>
        <p className="text-sm text-muted-foreground">
          How far back should JDI scan your inbox for job alerts?
        </p>
        <div className="flex flex-wrap gap-2">
          {SCAN_WINDOW_OPTIONS.map(option => (
            <button
              key={option.days}
              onClick={() => setScanWindowDays(option.days)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition ${
                scanWindowDays === option.days
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
        <p className="text-xs text-muted-foreground">
          Tip: Shorter = faster scans. Longer = catches more jobs but may include older listings.
        </p>
      </div>

      {/* Save Button */}
      <div className="flex gap-3">
        <AppButton onClick={handleSave} disabled={saving} className="flex-1">
          {saving ? "Saving..." : "Save & Go to JDI"}
        </AppButton>
      </div>
    </div>
  )
}
