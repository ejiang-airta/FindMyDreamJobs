//✅ File: frontend/src/app/analyze/page.tsx
// This page is for analyzing job descriptions and resumes.
'use client'
import JobInput from '@/components/JobInput'
import { useRouter } from 'next/navigation'
import React, { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import AnalyzeJob from '@/components/AnalyzeJob'


// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <AnalyzePage session={session} />
}

// This component is the main page for analyzing job descriptions and resumes.
function AnalyzePage({ session }: { session: any }) {
  const router = useRouter()
  const [analysisDone, setAnalysisDone] = useState(false)

  // 🔄 Auto-advance wizard if in wizard mode
  useEffect(() => {
    const wizardMode = localStorage.getItem("wizard_mode")
    if (analysisDone && wizardMode === "true") {
      // ✅ Update wizard progress to "match"
      fetch("http://127.0.0.1:8000/wizard/progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: session.user.email,
          step: "match"
        }),
      }).then(() => {
        router.push("/wizard") // 🚀 Go to next step in wizard
      })
    }
  }, [analysisDone, session, router])
  

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <header className="px-6 py-4 border-b bg-white shadow-sm">
        <h1 className="text-2xl font-semibold">🧠 Analyze Job Description</h1>
      </header>

      <main className="flex-1 overflow-auto px-6 py-4">
        <AnalyzeJob onSuccess={() => setAnalysisDone(true)} isWizard={false} />
      </main>
    </div>
  )
}
