//✅ File: frontend/src/app/analyze/page.tsx
// This page is for analyzing job descriptions and resumes.
'use client'
import JobInput from '@/components/JobInput'
import { useRouter } from 'next/navigation'
import React, { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import AnalyzeJob from '@/components/AnalyzeJob'
import { BACKEND_BASE_URL }  from '@/lib/env'
import { getUserId } from '@/lib/auth'


// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()
  const userId = getUserId()

    if (status === "loading") return <p>Loading...</p>
    if (!session?.user || !userId) return <p>Unauthorized or user ID missing</p>

    return <AnalyzePage />
  }

// This component is the main page for analyzing job descriptions and resumes.
function AnalyzePage() {
  const router = useRouter()
  const [analysisDone, setAnalysisDone] = useState(false)  

  return (
    <div className="flex flex-col overflow-hidden">
      <header className="px-6 py-4 border-b bg-white shadow-sm">
        <h1 className="text-2xl font-semibold">🧠 Analyze Job Description</h1>
      </header>

      <main className="flex-1  px-6 py-4">
        <AnalyzeJob onSuccess={() => setAnalysisDone(true)} isWizard={false} />
        {analysisDone && (
          <div className="mt-4 text-green-600 text-sm font-medium">
            ✅ Job analysis completed successfully.
          </div>
        )}
      </main>
    </div>
  )
}
