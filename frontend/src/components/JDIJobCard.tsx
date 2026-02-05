// File: frontend/src/components/JDIJobCard.tsx
// JDI candidate card — shows match score, reasons, and action buttons
"use client"

import { useState } from "react"
import {
  MapPin, Briefcase, WalletIcon, ExternalLink,
  BarChart3, Bookmark, XCircle, ChevronDown, ChevronUp,
} from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { AppButton } from "@/components/ui/AppButton"
import type { JDICandidate } from "@/lib/jdi-api"

interface JDIJobCardProps {
  candidate: JDICandidate
  onPromote: (id: string, mode: "save" | "analyze", jdText?: string | null) => void
  onIgnore: (id: string) => void
  onMarkSeen: (id: string) => void
  expandedId: string | null
  onToggleExpand: (id: string) => void
  jdText?: string | null
}

function getScoreColor(score: number | null): string {
  if (!score) return "bg-gray-100 text-gray-600"
  if (score >= 80) return "bg-green-100 text-green-800"
  if (score >= 60) return "bg-yellow-100 text-yellow-800"
  return "bg-orange-100 text-orange-800"
}

function getSourceBadge(source: string): string {
  switch (source) {
    case "linkedin": return "bg-blue-100 text-blue-700"
    case "indeed": return "bg-purple-100 text-purple-700"
    case "trueup": return "bg-teal-100 text-teal-700"
    default: return "bg-gray-100 text-gray-600"
  }
}

export function JDIJobCard({
  candidate,
  onPromote,
  onIgnore,
  onMarkSeen,
  expandedId,
  onToggleExpand,
  jdText,
}: JDIJobCardProps) {
  const isExpanded = expandedId === candidate.id
  const isUnread = !candidate.seen_at

  const handleExpand = () => {
    if (!isExpanded && isUnread) {
      onMarkSeen(candidate.id)
    }
    onToggleExpand(candidate.id)
  }

  return (
    <div className={`rounded-lg border bg-white p-6 shadow-sm space-y-4 transition ${isUnread ? "border-l-4 border-l-blue-500" : ""}`}>
      {/* Header: Title + Score */}
      <div className="flex justify-between items-start">
        <div className="flex items-start gap-2">
          {isUnread && (
            <span className="mt-2 h-2.5 w-2.5 rounded-full bg-blue-500 flex-shrink-0" title="Unread" />
          )}
          <div>
            <h3 className="text-xl font-semibold leading-snug">
              {candidate.title || "Untitled Position"}
            </h3>
            <p className="text-muted-foreground">{candidate.company || "Unknown Company"}</p>
          </div>
        </div>
        <div className="flex flex-col items-end gap-1">
          <Badge className={getScoreColor(candidate.match_score)}>
            {candidate.match_score !== null ? `${candidate.match_score}% Match` : "N/A"}
          </Badge>
          <Badge className={getSourceBadge(candidate.source)}>
            {candidate.source.charAt(0).toUpperCase() + candidate.source.slice(1)}
          </Badge>
        </div>
      </div>

      {/* Metadata row */}
      <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
        {candidate.location && (
          <div className="flex items-center gap-1">
            <MapPin className="h-4 w-4" />
            {candidate.location}
          </div>
        )}
        {candidate.employment_type && (
          <div className="flex items-center gap-1">
            <Briefcase className="h-4 w-4" />
            {candidate.employment_type}
          </div>
        )}
        {candidate.salary_text && (
          <div className="flex items-center gap-1">
            <WalletIcon className="h-4 w-4" />
            {candidate.salary_text}
          </div>
        )}
        {candidate.job_url_raw && (
          <a
            href={candidate.job_url_raw}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-blue-600 hover:underline"
          >
            <ExternalLink className="h-4 w-4" />
            View Original
          </a>
        )}
      </div>

      {/* Match reasons */}
      {candidate.match_reasons && candidate.match_reasons.length > 0 && (
        <div className="bg-blue-50 rounded-md p-3">
          <p className="text-xs font-semibold text-blue-700 mb-1">Why this matches you</p>
          <ul className="text-sm text-blue-900 space-y-0.5">
            {candidate.match_reasons.map((reason, i) => (
              <li key={i} className="flex items-start gap-1.5">
                <span className="text-blue-500 mt-0.5">&#8226;</span>
                {reason}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Expandable JD section */}
      <button
        onClick={handleExpand}
        className="flex items-center gap-1 text-sm text-blue-600 hover:underline"
      >
        {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        {isExpanded ? "Hide Description" : "Show Description"}
      </button>

      {isExpanded && jdText && (
        <div className="text-gray-600 text-sm max-h-64 overflow-y-auto border rounded-md p-3 bg-gray-50">
          {jdText.split(/\n+/).filter(l => l.trim()).map((line, i) => (
            <p key={i} className="mb-1">{line.trim()}</p>
          ))}
        </div>
      )}

      {/* Action buttons */}
      <div className="flex gap-2 pt-1">
        <AppButton variant="ghost" size="sm" onClick={() => onPromote(candidate.id, "analyze", jdText)}>
          <BarChart3 className="h-4 w-4 mr-1" /> Analyze Deeper
        </AppButton>
        <AppButton variant="ghost" size="sm" onClick={() => onPromote(candidate.id, "save", jdText)}>
          <Bookmark className="h-4 w-4 mr-1" /> Save
        </AppButton>
        <AppButton variant="ghost" size="sm" onClick={() => onIgnore(candidate.id)} className="text-gray-400 hover:text-red-500">
          <XCircle className="h-4 w-4 mr-1" /> Ignore
        </AppButton>
      </div>
    </div>
  )
}
