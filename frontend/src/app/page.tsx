// ✅ File: frontend/src/app/page.tsx
// This is the main page of the application. It serves as a landing page and provides options for users to sign in or sign out:
'use client'
import { signIn, signOut, useSession } from "next-auth/react"
import { Button } from "@/components/ui/button"
import { useEffect } from 'react'


export default function HomePage() {
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
    <div className="p-10 text-center">
      {session ? (
        <>
          <p>👋 Hello, {session.user?.name}</p>
          <button onClick={() => signOut()}>Sign out</button>
        </>
      ) : (
        <button onClick={() => signIn("google")}>Sign in with Google</button>
      )}
      <h1 className="text-3xl font-bold">🎯 Welcome to FindMyDreamJobs!</h1>
      <p className="mt-4 text-muted-foreground">Upload your resume, match it to jobs, optimize it — and land interviews faster.</p>  
    </div>
    
  )
}