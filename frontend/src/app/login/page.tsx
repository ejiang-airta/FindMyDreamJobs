// ✅ File: frontend/src/app/login/page.tsx
// This page is for logging in to the application.
'use client'

import { signIn, signOut, useSession } from "next-auth/react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import React, { useEffect, useState } from 'react'


export default function LoginPage() {
  const { data: session } = useSession()
  const [email, setEmail] = useState('')
  const [fullName, setFullName] = useState('')
  const [password, setPassword] = useState('') // add this for signup and login with password


  useEffect(() => {
      const fetchUserId = async () => {
      if (session?.user?.email) {
          const res = await fetch("http://127.0.0.1:8000/auth/whoami", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
              email: session.user.email,
              name: session.user.name ?? ""
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

  // Function to handle signup
  const handleSignup = async () => {
    if (!email || !fullName) {
      alert("Please enter both name and email.")
      return
    }

    try {
      // 1️⃣ Create user via backend
      const res = await fetch("http://127.0.0.1:8000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, full_name: fullName, password })
      })
  
      const data = await res.json()
      if (!res.ok) {
        alert("❌ Sign up failed: " + data.detail)
        return
      }
  
      // 2️⃣ Now sign in using NextAuth credentials provider
      const result = await signIn("credentials", {
        email,
        password,
        name: fullName,
        redirect: false,
        callbackUrl: "/dashboard"
      })

      console.log("🧪 signIn result:", result)
  
      if (result?.error) {
        alert("❌ Login failed: " + result.error)
      } else {
        // ✅ Redirect manually to dashboard
        window.location.href = "/dashboard"
      }
    } catch (err) {
      console.error("❌ Error during signup:", err)
      alert("❌ Something went wrong. Please try again.")
    }
  }
  

  return (
    <div className="max-w-xl mx-auto mt-10 space-y-6 text-center">
      <h1 className="text-2xl font-bold">🔐 Sign In to Continue</h1>

      {session ? (
        <>
          <p>Welcome back, {session.user?.name || "User"}!</p>
          <Button onClick={() => signOut()} className="w-full">
            Sign out
          </Button>
        </>
      ) : (
          <div className="space-y-4">
            <Button onClick={() => signIn("google")} className="w-full" variant="outline">
              Sign in with Google
            </Button>
            <Button onClick={handleSignup} className="w-full">
              Sign up with Email
            </Button>        
          <div className="border-t pt-4 space-y-2">
          <Input
              type="text"
              placeholder="Your full name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />

            <Input
              type="email"
              placeholder="Your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Input
              type="password"
              placeholder="Your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>
      )}
    </div>
  )
}