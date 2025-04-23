//✅ File: frontend/src/app/analyze/page.tsx
// This page is for analyzing job descriptions and resumes.
'use client'
import React, { useState } from 'react'
import AnalyzeJob from '@/components/AnalyzeJob'
import { Protected } from '@/components/Protected'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  return (
    <Protected>
      <AnalyzePage />
    </Protected>
  )
}

// This component is the main page for analyzing job descriptions and resumes.
function AnalyzePage() {
  //const router = useRouter()
  const [analysisDone, setAnalysisDone] = useState(false)  

  return (
    <div className="flex flex-col overflow-hidden">
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
