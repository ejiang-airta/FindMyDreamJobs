// ✅ File: frontend/src/app/jobs/page.tsx
// This page is for displaying matched jobs:
"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { MapPin, CalendarDays, Bookmark, BarChart3, Send } from "lucide-react"
import axios from "axios"
import { BACKEND_BASE_URL } from "@/lib/env"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { AppButton } from '@/components/ui/AppButton'
import { toast } from 'sonner'
import { Protected } from '@/components/Protected'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  return (
    <Protected>
      <JobsPage />
    </Protected>
  )
}

function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([])
  const [query, setQuery] = useState("")
  const [location, setLocation] = useState("")
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState("all")
  const [userId, setUserId] = useState<string | null>(null)
  const [savedJobIds, setSavedJobIds] = useState<Set<string>>(new Set())
  const [analyzedJobIds, setAnalyzedJobIds] = useState<Set<string>>(new Set())
  const [appliedJobIds, setAppliedJobIds] = useState<Set<string>>(new Set())
  const router = useRouter()

  useEffect(() => {
    const uid = localStorage.getItem("user_id")
    if (uid && !isNaN(parseInt(uid))) {
      setUserId(uid)
    } else {
      console.warn("Invalid user_id found in localStorage:", uid)
      setUserId(null)
    }

    const saved = localStorage.getItem("saved_jobs")
    if (saved) setSavedJobIds(new Set(JSON.parse(saved)))

    const analyzed = localStorage.getItem("analyzed_jobs")
    if (analyzed) setAnalyzedJobIds(new Set(JSON.parse(analyzed)))

    const applied = localStorage.getItem("applied_jobs")
    if (applied) setAppliedJobIds(new Set(JSON.parse(applied)))

    const storedQuery = localStorage.getItem("last_query") || ""
    const storedLocation = localStorage.getItem("last_location") || ""
    const storedResults = localStorage.getItem("last_results")

    setQuery(storedQuery)
    setLocation(storedLocation)
    if (storedResults) setJobs(JSON.parse(storedResults))
  }, [])

  const persistSearch = (query: string, location: string, results: any[]) => {
    localStorage.setItem("last_query", query)
    localStorage.setItem("last_location", location)
    localStorage.setItem("last_results", JSON.stringify(results))
  }

  const searchJobs = async () => {
    setLoading(true)
    try {
      const searchQuery = location ? `${query} in ${location}` : query
      const params = new URLSearchParams({ query: searchQuery })
      const res = await axios.get(`${BACKEND_BASE_URL}/search-jobs?${params.toString()}`)
      const results = res.data.results || []
      setJobs(results)
      persistSearch(query, location, results)
    } catch (e) {
      console.error("Job fetch failed", e)
    }
    setLoading(false)
  }

  const handleAnalyze = async (job: any) => {
    try {
      const response = await axios.post(`${BACKEND_BASE_URL}/analyze-searched-job`, {
        job_title: job.job_title || "N/A",
        employer_name: job.employer_name || "N/A",
        job_description: job.description,
        job_location: job.job_location || null,
        salary: job.salary || null,
        job_link: job.redirect_url,
        user_id: parseInt(userId || "0"),
      })

      if (response.status === 200) {
        const jobId = job.job_id || job.id || job.redirect_url
        const updated = new Set(analyzedJobIds)
        updated.add(jobId)
        setAnalyzedJobIds(updated)
        localStorage.setItem("analyzed_jobs", JSON.stringify(Array.from(updated)))
        toast.success("✅ Job analyzed and saved!")
      }
    } catch (err) {
      console.error("Analyze failed", err)
      alert("Failed to analyze job description")
    }
  }

  const handleApply = (url: string, jobId: string) => {
    if (url) window.open(url, "_blank")
    const updated = new Set(appliedJobIds)
    updated.add(jobId)
    setAppliedJobIds(updated)
    localStorage.setItem("applied_jobs", JSON.stringify(Array.from(updated)))
  }

  const handleSave = (job: any) => {
    const jobId = job.job_id || job.id || job.redirect_url
    if (!jobId) return
    const updated = new Set(savedJobIds)
    updated.add(jobId)
    setSavedJobIds(updated)
    localStorage.setItem("saved_jobs", JSON.stringify(Array.from(updated)))
    toast.success("✅ Job saved to Saved tab")
  }

  const tabFilteredJobs = jobs.filter(job => {
    const jobId = job.job_id || job.id || job.redirect_url
    switch (activeTab) {
      case 'saved': return savedJobIds.has(jobId)
      case 'analyzed': return analyzedJobIds.has(jobId)
      case 'applied': return appliedJobIds.has(jobId)
      default: return true
    }
  })

  const getTabCount = (type: string) => {
    switch (type) {
      case 'saved': return savedJobIds.size
      case 'analyzed': return analyzedJobIds.size
      case 'applied': return appliedJobIds.size
      case 'new': return 0
      default: return jobs.length
    }
  }

  return (
    <div className="px-6 py-10 max-w-5xl mx-auto space-y-8">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold">Find Your Dream Opportunity</h1>
        <p className="text-muted-foreground">Discover jobs that match your skills and preferences</p>
      </div>

      <div className="flex flex-col md:flex-row gap-2 w-full">
        <Input placeholder="Job title or keywords" value={query} onChange={(e) => setQuery(e.target.value)} className="flex-1 w-108" />
        <Input placeholder="Location (optional)" value={location} onChange={(e) => setLocation(e.target.value)} className="flex-1 w-84" />
        <AppButton onClick={searchJobs} disabled={loading} className="md:w-40">
          {loading ? "Searching..." : "Search Jobs"}
        </AppButton>
      </div>

      <div className="flex gap-4 text-sm font-medium text-muted-foreground border-b pb-2">
        {["all", "saved", "analyzed", "applied", "new"].map(tab => (
          <div key={tab} onClick={() => setActiveTab(tab)}
            className={`cursor-pointer px-3 py-1 rounded-md transition ${activeTab === tab ? 'bg-blue-100 text-blue-700 font-semibold' : ''}`}>{
              tab === 'all' ? `All Jobs (${getTabCount(tab)})` : `${tab.charAt(0).toUpperCase() + tab.slice(1)} (${getTabCount(tab)})`
            }</div>
        ))}
      </div>

      <div className="text-muted-foreground text-sm">Showing {tabFilteredJobs.length} jobs</div>

      <div className="space-y-6">
        {tabFilteredJobs.map((job, idx) => {
          const jobId = job.job_id || job.id || job.redirect_url
          const isSaved = savedJobIds.has(jobId)
          return (
            <div key={idx} className="rounded-lg border bg-white p-6 shadow-sm space-y-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-xl font-semibold leading-snug">{job.job_title}</h3>
                  <p className="text-muted-foreground">{job.employer_name}</p>
                </div>
                <div className="flex flex-col items-end space-y-1">
                  <Badge className="bg-green-100 text-green-800">94% Match</Badge>
                  <span className="text-xs text-gray-400">
                    {job.posted_at ? new Date(job.posted_at).toLocaleDateString() : ""}
                  </span>
                </div>
              </div>
              <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <MapPin className="h-4 w-4" />
                  {job.job_location || "Unknown"}
                </div>

                <div className="flex items-center gap-1">
                  <CalendarDays className="h-4 w-4" />
                  {job.posted_at ? new Date(job.posted_at).toDateString() : ""}
                </div>
                {job.salary && (
                  <div className="text-foreground font-medium">{job.salary}</div>
                )}
              </div>
              <p className="text-sm text-gray-700 line-clamp-3">{job.description}</p>
              <div className="flex gap-2">
                <AppButton variant="ghost" size="sm" onClick={() => handleSave(job)} className={isSaved ? "bg-blue-50" : ""}>
                  <Bookmark className="h-4 w-4 mr-1" /> {isSaved ? "Saved" : "Save"}
                </AppButton>
                <AppButton variant="ghost" size="sm" onClick={() => handleAnalyze(job)}>
                  <BarChart3 className="h-4 w-4 mr-1" /> Analyze
                </AppButton>
                <AppButton variant="default" size="sm" onClick={() => handleApply(job.redirect_url, jobId)}>
                  <Send className="h-4 w-4 mr-1" /> Apply
                </AppButton>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
