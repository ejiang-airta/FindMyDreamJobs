// ✅ File: frontend/src/components/NavBar.tsx
// Nevigation bar to let user navigate around the pages:

'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { getSession, useSession, signIn, signOut } from 'next-auth/react'
import { Button } from '@/components/ui/button'
import { useEffect, useState } from 'react'
import { User } from 'lucide-react'


const navItems = [
  { href: '/', label: '🏠 Home' },
  { href: '/dashboard', label: '📊 Dashboard' },
  { href: '/upload', label: '📤 Upload' },
  { href: '/analyze', label: '📑 Analyze' },
  { href: '/match', label: '🔍 Match' },
  { href: '/optimize', label: '🛠 Optimize' },
  //{ href: '/finalize', label: '✅ Finalize' }, // this page is a bit duplicative with the apply page
  { href: '/apply', label: '📩 Apply' },
  { href: '/applications', label: '🧾 Applications' },
  //{ href: '/matches', label: '🧠 Matches' },  //hide this page for now for a cleaner UI
  { href: '/stats', label: '📈 Stats' },
  { href: '/wizard', label: '🧙 Wizard' },
]

export default function NavBar() {
  const pathname = typeof window !== 'undefined' ? usePathname() : ''
  const { data: session, status } = useSession()
  const [ username, setUserName] = useState("")

  

  useEffect(() => {
    const fetchUserId = async () => {
      const session = await getSession()
    if (!session?.user?.email) return
    const res = await fetch("http://127.0.0.1:8000/auth/whoami", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: session.user.email,
        name: session.user.name || "",
      })
    })

    const data = await res.json();
    if (res.ok && data.user_id) {
      console.log("✅ Registered user:", data)
      localStorage.setItem("user_id", data.user_id)  // 👈 Store local DB ID
    }
  }

  fetchUserId()
}, [])


  // 🔐 SIGNUP - Register the user in the DB
  const handleSignup = async () => {
    try {
      const result = await signIn('google', { redirect: false })
  
      if (result?.error) {
        console.error("⚠️ Google sign-in error:", result.error)
        alert("⚠️ Google sign-in failed.")
        return
      }
  
      // 🧠 Wait for the session to be fully available
      let session = await getSession()
      let retryCount = 0
  
      while (!session && retryCount < 10) {
        await new Promise((r) => setTimeout(r, 300))
        session = await getSession()
        retryCount++
      }
  
      if (!session || !session.user?.email) {
        console.error("⚠️ Session not established after sign-up.")
        alert("⚠️ Failed to complete signup.")
        return
      }
  
      // ✅ Now call backend to register user
      const whoamiRes = await fetch("http://127.0.0.1:8000/auth/whoami", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: session.user.email,
          name: session.user.name || ""
        })
      })
  
      const whoamiData = await whoamiRes.json()
  
      if (whoamiRes.ok && whoamiData.user_id) {
        localStorage.setItem("user_id", whoamiData.user_id)
        console.log("✅ User signed up and registered:", whoamiData.user_id)
      } else {
        console.error("❌ Failed to register user:", whoamiData)
        alert("⚠️ Signup successful, but user not registered.")
      }
    } catch (err) {
      console.error("❌ Signup failed:", err)
      alert("⚠️ Signup error occurred.")
    }
  }

  return (
    <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">

        {/* Left: Navigation Links */}  
        <div className="max-w-10xl px-2 py-3 flex space-x-2 overflow-x-auto">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'px-3 py-2 rounded text-sm whitespace-nowrap font-medium hover:bg-gray-100 transition',
                pathname === item.href ? 'bg-gray-200 text-black font-semibold' : 'text-gray-600'
              )}
            >
              {item.label}
            </Link>
          ))}
        </div>

        {/* Right: Auth Controls */}
        <div className="flex justify-end space-x-2 items-center">
        {status === 'authenticated' ? (
            <>
              <span className="text-sm text-gray-600">{username}</span>
              <Button onClick={() => signOut()} variant="outline">
                Sign Out
              </Button>
            </>
          ) : (
            <>
              <Button onClick={() => signIn('google')} variant="outline">
                Log in
              </Button>
              <Link href="/login">
                <Button className="bg-white text-blue-600 hover:bg-gray-100">
                  Sign up
                </Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}