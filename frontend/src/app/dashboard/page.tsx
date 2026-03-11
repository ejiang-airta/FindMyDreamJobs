'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useSession } from 'next-auth/react'
import { useUserId } from '@/hooks/useUserId'
import { BACKEND_BASE_URL } from '@/lib/env'
import { Protected } from '@/components/Protected'
import { fetchJDICandidates } from '@/lib/jdi-api'
import {
  FileText, Briefcase, TrendingUp, Zap,
  Upload, ScanText, Wand2, ArrowRight,
  CheckCircle2, Clock, Star, Award,
} from 'lucide-react'
import { cn } from '@/lib/utils'

export default function ProtectedPage() {
  return (
    <Protected>
      <DashboardPage />
    </Protected>
  )
}

// ── helpers ──────────────────────────────────────────────────────────────────

function greeting(name: string) {
  const h = new Date().getHours()
  const time = h < 12 ? 'Good morning' : h < 18 ? 'Good afternoon' : 'Good evening'
  const first = name.split(' ')[0]
  return `${time}, ${first}`
}

function todayLabel() {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long', month: 'long', day: 'numeric',
  })
}

function normaliseStatus(s: string) {
  const l = s.toLowerCase()
  if (l === 'applied')                           return 'applied'
  if (l.includes('review') || l === 'in_review') return 'review'
  if (l.includes('interview'))                   return 'interview'
  if (l === 'offer')                             return 'offer'
  if (l === 'rejected')                          return 'rejected'
  return 'other'
}

// ── sub-components ────────────────────────────────────────────────────────────

function MetricCard({
  icon: Icon, label, value, sub, accent = false, href,
}: {
  icon: React.ElementType
  label: string
  value: string | number
  sub?: string
  accent?: boolean
  href?: string
}) {
  return (
    <div className={cn(
      'rounded-xl border shadow-sm p-5 flex flex-col gap-2 h-full transition-colors',
      accent
        ? 'bg-indigo-50 border-indigo-100 hover:bg-indigo-100/60'
        : 'bg-white border-gray-100 hover:bg-gray-50',
    )}>
      <div className="flex items-center justify-between">
        <span className={cn(
          'text-xs font-semibold uppercase tracking-wide',
          accent ? 'text-indigo-500' : 'text-gray-400',
        )}>
          {label}
        </span>
        <Icon className={cn('h-4 w-4', accent ? 'text-indigo-400' : 'text-gray-300')} />
      </div>
      <p className={cn('text-3xl font-bold', accent ? 'text-indigo-700' : 'text-gray-900')}>
        {value}
      </p>
      {sub && <p className="text-xs text-muted-foreground">{sub}</p>}
      {href && (
        <Link
          href={href}
          className={cn(
            'text-xs font-medium mt-auto flex items-center gap-1',
            accent ? 'text-indigo-600' : 'text-blue-600',
          )}
        >
          Review now <ArrowRight className="h-3 w-3" />
        </Link>
      )}
    </div>
  )
}

function PipelineFunnel({ applied, review, interview, offer }: {
  applied: number; review: number; interview: number; offer: number
}) {
  const stages = [
    { label: 'Applied',   count: applied,   color: 'bg-gray-100 text-gray-700',    dot: 'bg-gray-400' },
    { label: 'In Review', count: review,    color: 'bg-blue-50 text-blue-700',     dot: 'bg-blue-400' },
    { label: 'Interview', count: interview, color: 'bg-green-50 text-green-700',   dot: 'bg-green-500' },
    { label: 'Offer 🎉',  count: offer,     color: 'bg-purple-50 text-purple-700', dot: 'bg-purple-500' },
  ]
  const total = applied + review + interview + offer

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex flex-col gap-4 h-full">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Briefcase className="h-4 w-4 text-gray-300" />
          <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">
            Application Pipeline
          </span>
        </div>
        <Link href="/applications" className="text-xs text-blue-600 font-medium flex items-center gap-1 hover:underline">
          View all <ArrowRight className="h-3 w-3" />
        </Link>
      </div>

      {total === 0 ? (
        <p className="text-sm text-muted-foreground">No applications tracked yet.</p>
      ) : (
        <div className="grid grid-cols-4 gap-2">
          {stages.map((s) => (
            <div key={s.label} className={cn('rounded-lg px-3 py-3 flex flex-col gap-1', s.color)}>
              <div className="flex items-center gap-1.5">
                <span className={cn('h-2 w-2 rounded-full shrink-0', s.dot)} />
                <span className="text-[11px] font-medium leading-tight">{s.label}</span>
              </div>
              <p className="text-2xl font-bold">{s.count}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function ActivityFeed({ applications }: { applications: any[] }) {
  const items = [...applications]
    .sort((a, b) => new Date(b.applied_date).getTime() - new Date(a.applied_date).getTime())
    .slice(0, 5)

  const iconFor = (status: string) => {
    const n = normaliseStatus(status)
    if (n === 'interview') return <Star className="h-3.5 w-3.5 text-green-500" />
    if (n === 'offer')     return <Award className="h-3.5 w-3.5 text-purple-500" />
    if (n === 'review')    return <Clock className="h-3.5 w-3.5 text-blue-500" />
    return <CheckCircle2 className="h-3.5 w-3.5 text-gray-400" />
  }

  const labelFor = (app: any) => {
    const n = normaliseStatus(app.application_status)
    if (n === 'interview') return `Interview — ${app.job_title} at ${app.company_name}`
    if (n === 'offer')     return `Offer from ${app.company_name}!`
    if (n === 'review')    return `In review — ${app.job_title} at ${app.company_name}`
    return `Applied to ${app.job_title} at ${app.company_name}`
  }

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex flex-col gap-4">
      <div className="flex items-center gap-2">
        <TrendingUp className="h-4 w-4 text-gray-300" />
        <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">Recent Activity</span>
      </div>
      {items.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          No activity yet — apply to a job to get started.
        </p>
      ) : (
        <ul className="space-y-3">
          {items.map((app: any) => (
            <li key={app.application_id} className="flex items-start gap-3">
              <div className="mt-0.5 shrink-0">{iconFor(app.application_status)}</div>
              <div className="min-w-0">
                <p className="text-sm text-gray-700 leading-snug truncate">{labelFor(app)}</p>
                <p className="text-xs text-muted-foreground mt-0.5">
                  {new Date(app.applied_date).toLocaleDateString('en-US', {
                    month: 'short', day: 'numeric',
                  })}
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

function ResumesPanel({ resumes }: { resumes: any[] }) {
  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FileText className="h-4 w-4 text-gray-300" />
          <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">Resumes</span>
        </div>
        <Link href="/upload" className="text-xs text-blue-600 font-medium hover:underline">
          + Upload
        </Link>
      </div>

      {resumes.length === 0 ? (
        <p className="text-sm text-muted-foreground">No resumes uploaded yet.</p>
      ) : (
        <ul className="space-y-2">
          {resumes.slice(0, 3).map((r: any) => (
            <li key={r.id} className="flex items-center justify-between text-sm">
              <span className="truncate text-gray-700 font-medium max-w-[160px]">
                {r.resume_name || `Resume #${r.id}`}
              </span>
              {r.ats_score_final != null && r.ats_score_final > 0 ? (
                <span className="text-xs text-green-600 font-semibold shrink-0 ml-2">
                  ATS {r.ats_score_final}%
                </span>
              ) : r.ats_score_initial != null ? (
                <span className="text-xs text-gray-400 shrink-0 ml-2">
                  ATS {r.ats_score_initial}%
                </span>
              ) : null}
            </li>
          ))}
          {resumes.length > 3 && (
            <p className="text-xs text-muted-foreground">+{resumes.length - 3} more</p>
          )}
        </ul>
      )}

      {/* Quick actions */}
      <div className="pt-3 border-t border-gray-100 space-y-2">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Quick Actions</p>
        <div className="flex flex-col gap-2">
          {[
            { href: '/analyze',  icon: ScanText,     label: 'Analyze a Job' },
            { href: '/ats',      icon: CheckCircle2, label: 'ATS Check' },
            { href: '/optimize', icon: Wand2,        label: 'Optimize Resume' },
          ].map(({ href, icon: Icon, label }) => (
            <Link
              key={href}
              href={href}
              className="flex items-center gap-2.5 px-3 py-2 rounded-lg border border-gray-100 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
            >
              <Icon className="h-4 w-4 shrink-0 text-gray-400" />
              {label}
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}

// ── main page ─────────────────────────────────────────────────────────────────

function DashboardPage() {
  const { data: session } = useSession()
  const userId = useUserId()

  const [resumes, setResumes]           = useState<any[]>([])
  const [matches, setMatches]           = useState<any[]>([])
  const [applications, setApplications] = useState<any[]>([])
  const [intelUnread, setIntelUnread]   = useState<number | null>(null)
  const [loading, setLoading]           = useState(true)

  useEffect(() => {
    if (!userId) return

    const coreData = Promise.all([
      fetch(`${BACKEND_BASE_URL}/resumes/by-user/${userId}`).then(r => r.ok ? r.json() : []),
      fetch(`${BACKEND_BASE_URL}/matches/${userId}`).then(r => r.ok ? r.json() : []),
      fetch(`${BACKEND_BASE_URL}/applications/${userId}`).then(r => r.ok ? r.json() : []),
    ])

    // JDI unread count — gracefully fails if user hasn't connected Gmail
    const intelData = fetchJDICandidates(userId, { unread_only: true, limit: 1 })
      .then(feed => feed.total)
      .catch(() => null)

    Promise.all([coreData, intelData])
      .then(([[resumeData, matchData, appData], unread]) => {
        setResumes(resumeData)
        setMatches(matchData)
        setApplications(appData)
        setIntelUnread(unread)
      })
      .catch(err => console.error('Dashboard fetch error:', err))
      .finally(() => setLoading(false))
  }, [userId])

  // Pipeline funnel counts
  const pipeline = applications.reduce(
    (acc, app) => {
      const n = normaliseStatus(app.application_status)
      if      (n === 'applied')   acc.applied++
      else if (n === 'review')    acc.review++
      else if (n === 'interview') acc.interview++
      else if (n === 'offer')     acc.offer++
      return acc
    },
    { applied: 0, review: 0, interview: 0, offer: 0 }
  )

  // Average match score
  const avgMatchScore = (() => {
    const scores = matches
      .map((m: any) => m.match_score_final ?? m.match_score_initial)
      .filter((s): s is number => s != null)
    if (scores.length === 0) return null
    return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
  })()

  const name    = session?.user?.name ?? 'there'
  const isEmpty = !loading &&
    resumes.length === 0 && matches.length === 0 && applications.length === 0

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-10 space-y-6">

        {/* Greeting */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{greeting(name)}</h1>
          <p className="text-sm text-muted-foreground mt-0.5">{todayLabel()}</p>
        </div>

        {/* First-time empty state banner */}
        {isEmpty && (
          <div className="bg-blue-50 border border-blue-100 rounded-xl p-5 flex items-center justify-between gap-4 flex-wrap">
            <div>
              <p className="text-sm font-semibold text-blue-900">Welcome to FindMyDreamJobs!</p>
              <p className="text-sm text-blue-700 mt-0.5">
                Upload your first resume to start analyzing jobs and tracking applications.
              </p>
            </div>
            <Link href="/upload">
              <button className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors">
                <Upload className="h-4 w-4" /> Upload Resume
              </button>
            </Link>
          </div>
        )}

        {/* Top metrics row: Pipeline (2-col) + Intel + Match Score */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="sm:col-span-2">
            <PipelineFunnel {...pipeline} />
          </div>
          <MetricCard
            icon={Zap}
            label="New Job Intel"
            value={intelUnread ?? '—'}
            sub={
              intelUnread === null ? 'Connect Gmail to enable'
              : intelUnread === 0  ? 'All caught up'
              : `unread candidate${intelUnread !== 1 ? 's' : ''}`
            }
            accent
            href={intelUnread != null && intelUnread > 0 ? '/jobs?tab=jdi' : undefined}
          />
          <MetricCard
            icon={TrendingUp}
            label="Avg Match Score"
            value={avgMatchScore != null ? `${avgMatchScore}%` : '—'}
            sub={
              matches.length > 0
                ? `across ${matches.length} job${matches.length !== 1 ? 's' : ''}`
                : 'Analyze a job to see score'
            }
          />
        </div>

        {/* Lower section: Activity (2/3) + Resumes/Actions (1/3) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
            <ActivityFeed applications={applications} />
          </div>
          <div>
            <ResumesPanel resumes={resumes} />
          </div>
        </div>

      </div>
    </div>
  )
}
