// ✅ File: frontend/src/app/page.tsx
// This is the main page of the application. It serves as a landing page and provides options for users to sign in or sign out:
'use client'
import { signIn, signOut, useSession } from "next-auth/react"
import { Button } from "@/components/ui/button"

export default function HomePage() {
  const { data: session } = useSession()

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