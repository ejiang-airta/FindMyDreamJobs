// File: frontend/src/components/JDIFeed.tsx
// JDI candidate feed — shows filtered list of JDI candidates with actions
"use client"

import { useEffect, useState, useCallback } from "react"
import { useRouter } from "next/navigation"
import { RefreshCw, Settings, Mail } from "lucide-react"
import { toast } from "sonner"
import { AppButton } from "@/components/ui/AppButton"
import { JDIJobCard } from "@/components/JDIJobCard"
import {
  fetchJDICandidates,
  fetchJDICandidateDetail,
  markCandidateSeen,
  ignoreCandidate,
  promoteCandidate,
  runJDIIngestion,
  getGmailStatus,
  type JDICandidate,
  type JDICandidateDetail,
} from "@/lib/jdi-api"

interface JDIFeedProps {
  userId: string
}

type FilterMode = "all" | "unread" | "read"

export function JDIFeed({ userId }: JDIFeedProps) {
  const router = useRouter()
  const [candidates, setCandidates] = useState<JDICandidate[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [scanning, setScanning] = useState(false)
  const [filterMode, setFilterMode] = useState<FilterMode>("all")
  const [sourceFilter, setSourceFilter] = useState<string>("")
  const [expandedId, setExpandedId] = useState<string | null>(null)
  const [expandedDetails, setExpandedDetails] = useState<Record<string, string>>({})
  const [gmailConnected, setGmailConnected] = useState<boolean | null>(null)
  // Separate state for unread count (fetched independently)
  const [unreadCount, setUnreadCount] = useState(0)

  // Fetch unread count separately so it persists across filter changes
  const loadUnreadCount = useCallback(async () => {
    try {
      const data = await fetchJDICandidates(userId, {
        status: "new",
        unread_only: true,
        limit: 1,  // We only need the total count
      })
      setUnreadCount(data.total)
    } catch (err) {
      console.error("Failed to load unread count:", err)
    }
  }, [userId])

  const loadCandidates = useCallback(async () => {
    setLoading(true)
    try {
      const data = await fetchJDICandidates(userId, {
        status: "new",
        unread_only: filterMode === "unread",
        read_only: filterMode === "read",
        source: sourceFilter || undefined,
        limit: 50,
      })
      setCandidates(data.candidates)
      setTotal(data.total)
    } catch (err) {
      console.error("Failed to load JDI candidates:", err)
    } finally {
      setLoading(false)
    }
  }, [userId, filterMode, sourceFilter])

  // Check Gmail connection status on mount
  useEffect(() => {
    getGmailStatus(userId)
      .then(status => setGmailConnected(status?.status === "active"))
      .catch(() => setGmailConnected(false))
  }, [userId])

  // Load candidates on mount and when filters change
  useEffect(() => {
    if (gmailConnected) {
      loadCandidates()
    }
  }, [gmailConnected, loadCandidates])

  // Load unread count on mount and when Gmail status changes
  useEffect(() => {
    if (gmailConnected) {
      loadUnreadCount()
    }
  }, [gmailConnected, loadUnreadCount])

  const handleRefresh = async () => {
    setScanning(true)
    try {
      const result = await runJDIIngestion(userId)
      toast.success(`Scan complete: ${result.new_candidates} new jobs found from ${result.total_emails_scanned} emails`)
      await loadCandidates()
      await loadUnreadCount()  // Refresh unread count after scanning
    } catch (err) {
      console.error("JDI scan failed:", err)
      toast.error("Failed to scan for new jobs")
    } finally {
      setScanning(false)
    }
  }

  const handlePromote = async (candidateId: string, mode: "save" | "analyze", jdText?: string | null) => {
    try {
      // If we don't have jdText yet, fetch the candidate detail to get it
      let jd = jdText
      if (!jd && mode === "analyze") {
        try {
          const detail = await fetchJDICandidateDetail(candidateId, userId)
          jd = detail.jd_text
        } catch {
          // Continue without JD if fetch fails
        }
      }

      const result = await promoteCandidate(candidateId, userId, mode)
      setCandidates(prev => prev.filter(c => c.id !== candidateId))

      if (mode === "analyze") {
        // Store JD in localStorage for the Analyze page to read
        if (jd) {
          localStorage.setItem("jdi_analyze_jd", jd)
        }
        toast.success("Job promoted! Navigating to analysis...")
        router.push(`/analyze?job_id=${result.job_id}`)
      } else {
        toast.success("Job saved to your collection!")
      }
    } catch (err) {
      console.error("Promote failed:", err)
      toast.error("Failed to promote candidate")
    }
  }

  const handleIgnore = async (candidateId: string) => {
    try {
      await ignoreCandidate(candidateId, userId)
      setCandidates(prev => prev.filter(c => c.id !== candidateId))
      toast.success("Candidate ignored")
    } catch (err) {
      console.error("Ignore failed:", err)
      toast.error("Failed to ignore candidate")
    }
  }

  const handleMarkSeen = async (candidateId: string) => {
    try {
      await markCandidateSeen(candidateId, userId)
      setCandidates(prev =>
        prev.map(c => c.id === candidateId ? { ...c, seen_at: new Date().toISOString() } : c)
      )
      // Decrement unread count
      setUnreadCount(prev => Math.max(0, prev - 1))
    } catch (err) {
      console.error("Mark seen failed:", err)
    }
  }

  const handleToggleExpand = async (candidateId: string) => {
    if (expandedId === candidateId) {
      setExpandedId(null)
      return
    }
    setExpandedId(candidateId)
    // Fetch full detail if not cached
    if (!expandedDetails[candidateId]) {
      try {
        const detail = await fetchJDICandidateDetail(candidateId, userId)
        setExpandedDetails(prev => ({ ...prev, [candidateId]: detail.jd_text || "" }))
      } catch (err) {
        console.error("Failed to fetch candidate detail:", err)
      }
    }
  }

  // Not connected state
  if (gmailConnected === false) {
    return (
      <div className="text-center py-16 space-y-4">
        <Mail className="h-16 w-16 mx-auto text-gray-300" />
        <h3 className="text-xl font-semibold text-gray-700">Connect Gmail to Get Started</h3>
        <p className="text-muted-foreground max-w-md mx-auto">
          JDI scans your Gmail for job alert emails from LinkedIn, Indeed, and TrueUp,
          then scores and surfaces the best matches for you.
        </p>
        <AppButton onClick={() => router.push("/jdi/setup")}>
          Set Up JDI
        </AppButton>
      </div>
    )
  }

  // Loading initial state
  if (gmailConnected === null) {
    return (
      <div className="text-center py-16">
        <p className="text-muted-foreground">Checking Gmail connection...</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div className="flex gap-2 items-center">
          {/* Filter pills */}
          {(["all", "unread", "read"] as FilterMode[]).map(mode => (
            <button
              key={mode}
              onClick={() => setFilterMode(mode)}
              className={`px-3 py-1 text-sm rounded-md transition ${
                filterMode === mode
                  ? "bg-blue-100 text-blue-700 font-semibold"
                  : "text-muted-foreground hover:bg-gray-100"
              }`}
            >
              {mode.charAt(0).toUpperCase() + mode.slice(1)}
              {mode === "unread" && unreadCount > 0 && (
                <span className="ml-1 bg-blue-500 text-white text-xs rounded-full px-1.5 py-0.5">
                  {unreadCount}
                </span>
              )}
            </button>
          ))}

          {/* Source filter */}
          <select
            value={sourceFilter}
            onChange={e => setSourceFilter(e.target.value)}
            className="text-sm border rounded-md px-2 py-1 text-muted-foreground"
          >
            <option value="">All Sources</option>
            <option value="linkedin">LinkedIn</option>
            <option value="indeed">Indeed</option>
            <option value="trueup">TrueUp</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="flex gap-2">
          <AppButton
            variant="ghost"
            size="sm"
            onClick={() => router.push("/jdi/setup")}
          >
            <Settings className="h-4 w-4 mr-1" /> Settings
          </AppButton>
          <AppButton
            variant="primary"
            size="sm"
            onClick={handleRefresh}
            disabled={scanning}
          >
            <RefreshCw className={`h-4 w-4 mr-1 ${scanning ? "animate-spin" : ""}`} />
            {scanning ? "Scanning..." : "Scan Now"}
          </AppButton>
        </div>
      </div>

      {/* Results count */}
      <p className="text-muted-foreground text-sm">
        Showing {candidates.length} of {total} candidates
      </p>

      {/* Candidate list */}
      {loading ? (
        <div className="text-center py-8">
          <p className="text-muted-foreground">Loading candidates...</p>
        </div>
      ) : candidates.length === 0 ? (
        <div className="text-center py-12 space-y-3">
          <p className="text-lg font-medium text-gray-600">No candidates found</p>
          <p className="text-sm text-muted-foreground">
            Try scanning for new jobs or adjusting your filters.
          </p>
          <AppButton variant="primary" size="sm" onClick={handleRefresh} disabled={scanning}>
            <RefreshCw className={`h-4 w-4 mr-1 ${scanning ? "animate-spin" : ""}`} />
            Scan Now
          </AppButton>
        </div>
      ) : (
        <div className="space-y-4">
          {candidates.map(candidate => (
            <JDIJobCard
              key={candidate.id}
              candidate={candidate}
              onPromote={handlePromote}
              onIgnore={handleIgnore}
              onMarkSeen={handleMarkSeen}
              expandedId={expandedId}
              onToggleExpand={handleToggleExpand}
              jdText={expandedDetails[candidate.id]}
            />
          ))}
        </div>
      )}
    </div>
  )
}
