// ✅ File: frontend/src/app/login/page.tsx
// This page is for logging in to the application.
'use client'

import { signIn, signOut, useSession } from "next-auth/react"
import { Button } from "@/components/ui/button"
import React, { useEffect }  from 'react'


export default function LoginPage() {
  const { data: session } = useSession()

    useEffect(() => {
        const fetchUserId = async () => {
        if (session?.user?.email) {
            const res = await fetch("http://127.0.0.1:8000/auth/whoami", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: session.user.email,
                name: session.user.name
            })
            })
            const data = await res.json()
            if (data?.user_id) {
            localStorage.setItem("user_id", data.user_id)
            }
        }
        }
    
        fetchUserId()
    }, [session])

  return (
    <div className="max-w-xl mx-auto mt-10 space-y-6 text-center">
      <h1 className="text-2xl font-bold">🔐 Sign In to Continue</h1>

      {session ? (
        <>
          <p>✅ Logged in as: <strong>{session.user?.email}</strong></p>
          <Button onClick={() => signOut()}>🚪 Sign Out</Button>
        </>
      ) : (
        <Button onClick={() => signIn("google")}>🔑 Sign in with Google</Button>
      )}
    </div>
  )
}
