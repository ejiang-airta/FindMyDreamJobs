// ✅ File: frontend/src/app/upload/page.tsx
// This page is for uploading resumes.
// When opened with ?for_jdi=1 (from JDI Settings), writes the new resume ID to
// localStorage so JDISection can auto-add it to Base Resumes on focus.

'use client'

import UploadResume from '@/components/UploadResume'
import { useSearchParams } from 'next/navigation'
import { Protected } from '@/components/Protected'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  return (
    <Protected>
      <UploadPage />
    </Protected>
  )
}

function UploadPage() {
  const searchParams = useSearchParams()
  const forJdi = searchParams.get("for_jdi") === "1"

  const handleSuccess = (resumeId?: number) => {
    if (forJdi && resumeId) {
      // Signal JDISection (in the opener tab) to auto-add this resume to Base Resumes
      localStorage.setItem("jdi_pending_resume_id", String(resumeId))
    }
    if (forJdi) {
      // Close this tab and return to the Settings page
      window.close()
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 px-4">
      <h1 className="text-2xl font-bold mb-4">
        {forJdi ? "Upload Resume for Job Intel" : "📤 Upload Resume"}
      </h1>
      {forJdi && (
        <p className="text-sm text-muted-foreground mb-6">
          After uploading, this tab will close and the resume will be added to your Job Intel Base Resumes automatically.
        </p>
      )}
      <UploadResume isWizard={false} onSuccess={handleSuccess} />
    </div>
  )
}
