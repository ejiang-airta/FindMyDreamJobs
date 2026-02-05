// File: frontend/src/lib/jdi-api.ts
// API client functions for JDI (Job Daily Intelligence) feature
import axios from "axios"
import { BACKEND_BASE_URL } from "@/lib/env"

// --- Types ---

export interface JDICandidate {
  id: string
  source: string
  title: string | null
  company: string | null
  location: string | null
  employment_type: string | null
  salary_text: string | null
  match_score: number | null
  match_reasons: string[] | null
  status: string
  seen_at: string | null
  job_url_raw: string | null
  created_at: string
}

export interface JDICandidateDetail extends JDICandidate {
  jd_text: string | null
  jd_extraction_confidence: number | null
  job_url_canonical: string | null
  selected_resume_id: number | null
  updated_at: string | null
}

export interface JDICandidateFeed {
  candidates: JDICandidate[]
  total: number
  limit: number
  offset: number
}

export interface JDIRunResult {
  new_candidates: number
  total_emails_scanned: number
  message: string
}

export interface GmailIntegrationStatus {
  id: string
  user_id: number
  provider: string
  status: string
  scopes: string[] | null
  last_sync_at: string | null
  created_at: string
  updated_at: string | null
}

export interface UserProfile {
  user_id: number
  target_titles: string[] | null
  target_locations: string[] | null
  jdi_min_score: number
  jdi_sources_enabled: string[] | null
  jdi_base_resume_ids: number[] | null
  jdi_resume_select_mode: string
  jdi_resume_keyword_rules: Record<string, number> | null
  jdi_scan_window_days: number
  jdi_custom_source_patterns: string[] | null
  created_at: string
  updated_at: string | null
}

// --- JDI Candidates API ---

export async function fetchJDICandidates(
  userId: string,
  params: {
    status?: string
    min_score?: number
    unread_only?: boolean
    read_only?: boolean
    source?: string
    limit?: number
    offset?: number
  } = {}
): Promise<JDICandidateFeed> {
  const searchParams = new URLSearchParams({ user_id: userId })
  if (params.status) searchParams.set("status", params.status)
  if (params.min_score !== undefined) searchParams.set("min_score", String(params.min_score))
  if (params.unread_only) searchParams.set("unread_only", "true")
  if (params.read_only) searchParams.set("read_only", "true")
  if (params.source) searchParams.set("source", params.source)
  if (params.limit) searchParams.set("limit", String(params.limit))
  if (params.offset) searchParams.set("offset", String(params.offset))

  const res = await axios.get(`${BACKEND_BASE_URL}/api/jdi/candidates?${searchParams.toString()}`)
  return res.data
}

export async function fetchJDICandidateDetail(
  candidateId: string,
  userId: string
): Promise<JDICandidateDetail> {
  const res = await axios.get(
    `${BACKEND_BASE_URL}/api/jdi/candidates/${candidateId}?user_id=${userId}`
  )
  return res.data
}

export async function markCandidateSeen(candidateId: string, userId: string) {
  return axios.post(
    `${BACKEND_BASE_URL}/api/jdi/candidates/${candidateId}/mark-seen?user_id=${userId}`
  )
}

export async function ignoreCandidate(candidateId: string, userId: string) {
  return axios.post(
    `${BACKEND_BASE_URL}/api/jdi/candidates/${candidateId}/ignore?user_id=${userId}`
  )
}

export async function promoteCandidate(
  candidateId: string,
  userId: string,
  mode: "save" | "analyze"
): Promise<{ job_id: number; status: string }> {
  const res = await axios.post(
    `${BACKEND_BASE_URL}/api/jdi/candidates/${candidateId}/promote?user_id=${userId}`,
    { mode }
  )
  return res.data
}

export async function runJDIIngestion(
  userId: string,
  windowHours: number = 24
): Promise<JDIRunResult> {
  const res = await axios.post(
    `${BACKEND_BASE_URL}/api/jdi/run?user_id=${userId}`,
    { window_hours: windowHours }
  )
  return res.data
}

// --- Gmail Integration API ---

export async function getGmailConnectUrl(userId: string): Promise<string> {
  const res = await axios.get(
    `${BACKEND_BASE_URL}/api/integrations/gmail/connect?user_id=${userId}`
  )
  return res.data.authorization_url
}

export async function getGmailStatus(userId: string): Promise<GmailIntegrationStatus | null> {
  try {
    const res = await axios.get(
      `${BACKEND_BASE_URL}/api/integrations/gmail/status?user_id=${userId}`
    )
    return res.data
  } catch (err: any) {
    if (err?.response?.status === 404) return null
    throw err
  }
}

export async function revokeGmailIntegration(userId: string) {
  return axios.post(
    `${BACKEND_BASE_URL}/api/integrations/gmail/revoke?user_id=${userId}`
  )
}

// --- User Profile API ---

export async function getUserProfile(userId: string): Promise<UserProfile | null> {
  try {
    const res = await axios.get(`${BACKEND_BASE_URL}/api/profile/${userId}`)
    return res.data
  } catch (err: any) {
    if (err?.response?.status === 404) return null
    throw err
  }
}

export async function updateUserProfile(
  userId: string,
  data: Partial<UserProfile>
): Promise<UserProfile> {
  const res = await axios.put(`${BACKEND_BASE_URL}/api/profile/${userId}`, data)
  return res.data
}
