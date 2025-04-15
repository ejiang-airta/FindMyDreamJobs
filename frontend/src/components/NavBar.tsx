// ✅ File: frontend/src/components/NavBar.tsx
// Nevigation bar to let user navigate around the pages:

'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { getSession, useSession, signIn, signOut } from 'next-auth/react'
import { Button } from '@/components/ui/button'
import { useEffect, useState } from 'react'
import { BACKEND_BASE_URL }  from '@/lib/env'

const navItems = [
  { href: '/', label: '🏠 Home' },
  { href: '/dashboard', label: '📊 Dashboard' },
  { href: '/upload', label: '📤 Upload' },
  { href: '/analyze', label: '📑 Analyze' },
  { href: '/match', label: '🔍 Match' },
  { href: '/optimize', label: '🛠 Optimize' },
  { href: '/apply', label: '📩 Apply' },
  { href: '/applications', label: '🧾 Applications' },
  { href: '/stats', label: '📈 Stats' },
  { href: '/wizard', label: '🧙 Wizard' },
]

export default function NavBar() {
  const pathname = usePathname()
  const { data: session, status } = useSession()
  const [username, setUsername] = useState("")

  useEffect(() => {
    const fetchUser = async () => {
      const session = await getSession()
      if (!session?.user?.email) return

      // Register user
      const res = await fetch(`${BACKEND_BASE_URL}/auth/whoami`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: session.user.email,
          name: session.user.name || ""
        }),
      })

      const data = await res.json()
      if (res.ok && data.user_id) {
        localStorage.setItem("user_id", data.user_id)
        setUsername(session.user.name || session.user.email || "")
      }

      // Fetch wizard progress
      const wizardRes = await fetch(`${BACKEND_BASE_URL}/wizard/progress/get`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: session.user.email })
      })
      const wizardData = await wizardRes.json()
      localStorage.setItem("wizard_progress", wizardData.step || "")

      // Redirect brand new user
      if (!wizardData.step && pathname === '/dashboard') {
        window.location.href = '/'
      }
    }

    fetchUser()
  }, [pathname])

  return (
    <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">

        {/* LEFT: NAV */}
        <div className="flex space-x-2 overflow-x-auto">
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

        {/* RIGHT: SESSION */}
        <div className="flex items-center gap-3">
          {status === 'authenticated' ? (
            <>
              <span className="text-sm text-gray-700">{username}</span>
              <Button onClick={() => signOut()} variant="outline">Sign Out</Button>
            </>
          ) : (
            <>
              <Link href="/login">
                <Button variant="outline">Log in</Button>
              </Link>
              <Link href="/signup">
                <Button className="bg-blue-600 text-white hover:bg-blue-700">Sign up</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
