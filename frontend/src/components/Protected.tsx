// File: src/components/Protected.tsx
// This component is used to protect pages that require authentication.
'use client'

import { useSession } from 'next-auth/react'
import { useEffect, useRef  } from 'react'
import { useRouter } from 'next/navigation'
import { toast } from 'sonner'

export function Protected({ children }: { children: React.ReactNode }) {
  const { status } = useSession()
  const router = useRouter()
  const hasRedirected = useRef(false)  // ✅ NEW: use this to track if we have already redirected

  useEffect(() => {
    if (status === 'unauthenticated' && !hasRedirected.current) {
    hasRedirected.current = true  // ✅ Prevent multiple toasts & redirects
    toast("👋 Welcome to FindMyDreamJobs.com! Please sign in or create an account to get started.")
    setTimeout(() => router.push('/login'), 1500)
    }
  }, [status, router])

  if (status === 'loading') return <p>Loading...</p>
  if (status === 'unauthenticated') return null

  return <>{children}</>
}
