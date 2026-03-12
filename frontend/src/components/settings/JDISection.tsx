"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Mail, CheckCircle2, Circle, Plus, X, Upload } from "lucide-react"
import { toast } from "sonner"
import axios from "axios"
import { cn } from "@/lib/utils"
import { BACKEND_BASE_URL } from "@/lib/env"
import { AppButton } from "@/components/ui/AppButton"
import { useUserId } from "@/hooks/useUserId"
import {
  getGmailConnectUrl,
  getGmailStatus,
  revokeGmailIntegration,
  getUserProfile,
  updateUserProfile,
  type GmailIntegrationStatus,
} from "@/lib/jdi-api"

const AVAILABLE_SOURCES = [
  { key: "linkedin", label: "LinkedIn", description: "jobalerts-noreply@linkedin.com" },
  { key: "indeed",   label: "Indeed",   description: "alert@indeed.com" },
  { key: "trueup",   label: "TrueUp",   description: "hello@trueup.io" },
  { key: "other",    label: "Others",   description: "Glassdoor, Talent.com, etc." },
]

const SCAN_WINDOW_OPTIONS = [
  { days: 1, label: "1 day" },
  { days: 2, label: "2 days" },
  { days: 3, label: "3 days" },
  { days: 5, label: "5 days" },
  { days: 7, label: "7 days" },
]

interface ResumeOption { id: number; name: string }

export function JDISection() {
  const router = useRouter()
  const userId = useUserId()

  const [gmailStatus, setGmailStatus]   = useState<GmailIntegrationStatus | null>(null)
  const [gmailLoading, setGmailLoading] = useState(true)
  const [saving, setSaving]             = useState(false)

  // Preferences
  const [selectedSources, setSelectedSources]             = useState<string[]>(["linkedin", "indeed", "trueup", "other"])
  const [selectedResumeIds, setSelectedResumeIds]         = useState<number[]>([])
  const [minScore, setMinScore]                           = useState(60)
  const [scanWindowDays, setScanWindowDays]               = useState(7)
  const [customSourcePatterns, setCustomSourcePatterns]   = useState<string[]>([])
  const [newCustomPattern, setNewCustomPattern]           = useState("")
  const [resumes, setResumes]                             = useState<ResumeOption[]>([])
  const [selectedDropdownResume, setSelectedDropdownResume] = useState<number | "">("")

  useEffect(() => {
    if (!userId) return

    getGmailStatus(userId)
      .then(s => setGmailStatus(s))
      .catch(() => setGmailStatus(null))
      .finally(() => setGmailLoading(false))

    getUserProfile(userId)
      .then(profile => {
        if (!profile) return
        if (profile.jdi_sources_enabled)       setSelectedSources(profile.jdi_sources_enabled)
        if (profile.jdi_base_resume_ids)       setSelectedResumeIds(profile.jdi_base_resume_ids)
        if (profile.jdi_min_score)             setMinScore(profile.jdi_min_score)
        if (profile.jdi_scan_window_days)      setScanWindowDays(profile.jdi_scan_window_days)
        if (profile.jdi_custom_source_patterns) setCustomSourcePatterns(profile.jdi_custom_source_patterns)
      })
      .catch(() => {})

    axios.get(`${BACKEND_BASE_URL}/resumes/by-user/${userId}`)
      .then(res => {
        const data: any[] = res.data || []
        setResumes(data.map(r => ({ id: r.id, name: r.resume_name || `Resume #${r.id}` })))
      })
      .catch(() => setResumes([]))
  }, [userId])

  // Handle OAuth callback landing back on /settings?jdi_connected=true#jdi
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    if (params.get("jdi_connected") === "true") {
      toast.success("Gmail connected successfully!")
      if (userId) getGmailStatus(userId).then(s => setGmailStatus(s))
      window.history.replaceState(null, "", "/settings#jdi")
    } else if (params.get("jdi_error") === "true") {
      toast.error("Failed to connect Gmail. Please try again.")
      window.history.replaceState(null, "", "/settings#jdi")
    }
  }, [userId])

  const handleGmailConnect = async () => {
    if (!userId) return
    try {
      // Pass window.location.origin so the backend embeds it in the OAuth state.
      // This ensures the callback redirects back to the correct frontend
      // (preview vs production) regardless of which backend handles the callback.
      const authUrl = await getGmailConnectUrl(userId, window.location.origin)
      window.location.href = authUrl
    } catch {
      toast.error("Failed to initiate Gmail connection")
    }
  }

  const handleGmailRevoke = async () => {
    if (!userId) return
    try {
      await revokeGmailIntegration(userId)
      setGmailStatus(prev => prev ? { ...prev, status: "revoked" } : null)
      toast.success("Gmail disconnected")
    } catch {
      toast.error("Failed to disconnect Gmail")
    }
  }

  const addCustomPattern = () => {
    const p = newCustomPattern.trim()
    if (!p.includes("@"))            { toast.error("Enter a valid email address"); return }
    if (customSourcePatterns.includes(p)) { toast.error("Already added"); return }
    setCustomSourcePatterns(prev => [...prev, p])
    setNewCustomPattern("")
  }

  const addResume = () => {
    if (selectedDropdownResume === "") return
    const id = Number(selectedDropdownResume)
    if (selectedResumeIds.includes(id)) { toast.error("Already selected"); return }
    setSelectedResumeIds(prev => [...prev, id])
    setSelectedDropdownResume("")
  }

  const handleSave = async () => {
    if (!userId) return
    setSaving(true)
    try {
      await updateUserProfile(userId, {
        jdi_sources_enabled:       selectedSources,
        jdi_base_resume_ids:       selectedResumeIds,
        jdi_min_score:             minScore,
        jdi_scan_window_days:      scanWindowDays,
        jdi_custom_source_patterns: customSourcePatterns.length > 0 ? customSourcePatterns : null,
      })
      toast.success("Job Intel settings saved")
    } catch {
      toast.error("Failed to save settings")
    } finally {
      setSaving(false)
    }
  }

  const isGmailActive  = gmailStatus?.status === "active"
  const getResumeName  = (id: number) => resumes.find(r => r.id === id)?.name ?? `Resume #${id}`
  const availableResumes = resumes.filter(r => !selectedResumeIds.includes(r.id))

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-lg font-semibold text-gray-900">Job Intel</h2>
          <span className="text-[10px] font-semibold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">PRO</span>
        </div>
        <p className="text-sm text-muted-foreground mt-0.5">
          Automated job scanning from your Gmail inbox
        </p>
      </div>

      {/* Gmail connection */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 space-y-4">
        <div className="flex items-center gap-2">
          {isGmailActive
            ? <CheckCircle2 className="h-4 w-4 text-green-600" />
            : <Circle className="h-4 w-4 text-gray-300" />}
          <h3 className="text-sm font-semibold text-gray-900">Gmail Connection</h3>
        </div>
        <p className="text-sm text-muted-foreground">
          Read-only access to scan job alert emails. We never read personal emails.
        </p>
        {gmailLoading ? (
          <p className="text-sm text-muted-foreground">Checking connection…</p>
        ) : isGmailActive ? (
          <div className="flex flex-wrap items-center gap-3">
            <span className="inline-flex items-center gap-1.5 text-sm text-green-700 bg-green-50 px-3 py-1.5 rounded-lg border border-green-100">
              <Mail className="h-4 w-4" /> Gmail Connected
            </span>
            {gmailStatus?.last_sync_at && (
              <span className="text-xs text-muted-foreground">
                Last scan: {new Date(gmailStatus.last_sync_at).toLocaleString()}
              </span>
            )}
            <AppButton variant="ghost" size="sm" onClick={handleGmailRevoke}>Disconnect</AppButton>
          </div>
        ) : (
          <AppButton onClick={handleGmailConnect}>
            <Mail className="h-4 w-4 mr-2" /> Connect Gmail
          </AppButton>
        )}
      </div>

      {/* Job alert sources */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 space-y-4">
        <h3 className="text-sm font-semibold text-gray-900">Job Alert Sources</h3>
        <p className="text-sm text-muted-foreground">Which platforms' job alerts should we scan?</p>
        <div className="space-y-2">
          {AVAILABLE_SOURCES.map(source => (
            <label
              key={source.key}
              className="flex items-center gap-3 p-3 rounded-lg border cursor-pointer hover:bg-gray-50 transition"
            >
              <input
                type="checkbox"
                checked={selectedSources.includes(source.key)}
                onChange={() =>
                  setSelectedSources(prev =>
                    prev.includes(source.key)
                      ? prev.filter(s => s !== source.key)
                      : [...prev, source.key]
                  )
                }
                className="h-4 w-4 text-blue-600 rounded"
              />
              <span className="text-sm font-medium">{source.label}</span>
              <span className="text-xs text-muted-foreground">({source.description})</span>
            </label>
          ))}
        </div>

        {/* Custom email patterns (only when "other" selected) */}
        {selectedSources.includes("other") && (
          <div className="pt-4 border-t space-y-3">
            <p className="text-sm font-medium">Custom Email Patterns</p>
            <p className="text-xs text-muted-foreground">
              Add email addresses from other job alert services.
            </p>
            <div className="flex gap-2">
              <input
                type="email"
                value={newCustomPattern}
                onChange={e => setNewCustomPattern(e.target.value)}
                placeholder="e.g. alerts@mycompany.com"
                onKeyDown={e => e.key === "Enter" && addCustomPattern()}
                className="flex-1 px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <AppButton variant="secondary" size="sm" onClick={addCustomPattern}>
                <Plus className="h-4 w-4" />
              </AppButton>
            </div>
            {customSourcePatterns.map(pattern => (
              <div key={pattern} className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded-lg text-sm">
                <span>{pattern}</span>
                <button
                  onClick={() => setCustomSourcePatterns(prev => prev.filter(p => p !== pattern))}
                  className="text-gray-400 hover:text-red-500"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Base resumes */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 space-y-4">
        <h3 className="text-sm font-semibold text-gray-900">Base Resumes</h3>
        <p className="text-sm text-muted-foreground">
          Up to 3 resumes to score incoming jobs against. Job Intel picks the best match automatically.
        </p>
        <div className="border rounded-lg p-4 bg-gray-50 min-h-[72px] space-y-2">
          {selectedResumeIds.length === 0 ? (
            <p className="text-sm text-muted-foreground italic">No resumes selected yet</p>
          ) : (
            selectedResumeIds.map(id => (
              <div key={id} className="flex items-center justify-between bg-white px-3 py-2 rounded-lg border text-sm">
                <span className="font-medium">{getResumeName(id)}</span>
                <button
                  onClick={() => setSelectedResumeIds(prev => prev.filter(i => i !== id))}
                  className="text-gray-400 hover:text-red-500"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            ))
          )}
        </div>
        {resumes.length > 0 && selectedResumeIds.length < 3 && (
          <div className="flex gap-2">
            <select
              value={selectedDropdownResume}
              onChange={e => setSelectedDropdownResume(e.target.value ? Number(e.target.value) : "")}
              className="flex-1 px-3 py-2 border rounded-lg text-sm bg-white"
            >
              <option value="">Select a resume…</option>
              {availableResumes.map(r => (
                <option key={r.id} value={r.id}>{r.name}</option>
              ))}
            </select>
            <AppButton variant="secondary" size="sm" disabled={selectedDropdownResume === ""} onClick={addResume}>
              <Plus className="h-4 w-4 mr-1" /> Add
            </AppButton>
          </div>
        )}
        <button
          onClick={() => router.push("/upload")}
          className="text-sm text-blue-600 hover:underline flex items-center gap-1"
        >
          <Upload className="h-3.5 w-3.5" /> Upload new resume
        </button>
      </div>

      {/* Minimum match score */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 space-y-4">
        <h3 className="text-sm font-semibold text-gray-900">Minimum Match Score</h3>
        <p className="text-sm text-muted-foreground">
          Only surface jobs that score above this threshold.
        </p>
        <div className="flex items-center gap-4">
          <input
            type="range" min={0} max={100} step={5} value={minScore}
            onChange={e => setMinScore(parseInt(e.target.value))}
            className="flex-1"
          />
          <span className="text-lg font-bold text-blue-700 w-12 text-center">{minScore}%</span>
        </div>
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>More results</span>
          <span>Higher quality</span>
        </div>
      </div>

      {/* Email scan window */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 space-y-4">
        <h3 className="text-sm font-semibold text-gray-900">Email Scan Window</h3>
        <p className="text-sm text-muted-foreground">
          How far back to scan your inbox for job alerts.
        </p>
        <div className="flex flex-wrap gap-2">
          {SCAN_WINDOW_OPTIONS.map(opt => (
            <button
              key={opt.days}
              onClick={() => setScanWindowDays(opt.days)}
              className={cn(
                "px-4 py-2 rounded-lg text-sm font-medium transition",
                scanWindowDays === opt.days
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              )}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      <div className="flex justify-end">
        <AppButton onClick={handleSave} disabled={saving}>
          {saving ? "Saving…" : "Save Job Intel Settings"}
        </AppButton>
      </div>
    </div>
  )
}
