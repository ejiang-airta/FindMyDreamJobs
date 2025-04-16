// File: /frontend/src/hooks/useUserId.ts

'use client'

import { useSession } from 'next-auth/react'
import { useEffect, useState } from 'react'
import { BACKEND_BASE_URL } from '@/lib/env'
export function useUserId() {
  const { data: session, status } = useSession()
  const [userId, setUserId] = useState<string | null>(null)

  useEffect(() => {
    if (status === 'authenticated' && session?.user?.email) {
      // Fetch user ID securely from backend, always accurate
      fetch(`${BACKEND_BASE_URL}/auth/whoami`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: session.user.email, name: session.user.name || "" }),
      })
        .then(res => res.json())
        .then(data => {
          if (data.user_id) {
            setUserId(String(data.user_id))
          } else {
            console.error("No user_id returned:", data)
          }
        })
        .catch(err => {
          console.error("Failed fetching user_id:", err)
        })
    }
  }, [session, status])

  return userId
}
