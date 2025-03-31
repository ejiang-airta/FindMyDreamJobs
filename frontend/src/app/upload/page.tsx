// ✅ File: frontend/src/app/upload/page.tsx
// This page is for uploading resumes.
'use client'
import UploadResume from '@/components/UploadResume'
import { useSession } from 'next-auth/react'
import React from 'react'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <UploadPage />
}

// This component is the main page for uploading resumes.
// It uses the UploadResume component to allow users to upload their resumes:
function UploadPage() {
  return (
    <main className="flex justify-center items-center h-screen">
      <UploadResume />
    </main>
  )
}
