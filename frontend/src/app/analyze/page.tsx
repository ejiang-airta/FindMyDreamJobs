//✅ File: frontend/src/app/analyze/page.tsx
// This page is for analyzing job descriptions and resumes.
'use client'
import JobInput from '@/components/JobInput'
import { useSession } from 'next-auth/react'
import React, { useState } from 'react'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <AnalyzePage />
}

// This component is the main page for analyzing job descriptions and resumes.
function AnalyzePage() {
  const [jobDescription, setJobDescription] = useState("")

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <header className="px-6 py-4 border-b bg-white shadow-sm">
        <h1 className="text-2xl font-semibold">🧠 Analyze Job Description</h1>
      </header>

      <main className="flex-1 overflow-auto px-6 py-4">
        <JobInput />
        {/* 👇 Job analysis results */}
        <div className="mt-6 space-y-2">
          {/* Render job info here */}
        </div>
      </main>
    </div>
  )
}
