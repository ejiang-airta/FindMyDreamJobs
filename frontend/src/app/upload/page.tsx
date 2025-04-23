// ✅ File: frontend/src/app/upload/page.tsx
// This page is for uploading resumes.

'use client'

import UploadResume from '@/components/UploadResume'
import { useSession } from 'next-auth/react'
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
  return (
    <div className="max-w-3xl mx-auto mt-10 px-4">
      <h1 className="text-2xl font-bold mb-4">📤 Upload Resume</h1>
      <UploadResume isWizard={false} />
    </div>
  )
}