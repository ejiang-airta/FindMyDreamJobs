// ✅ File: frontend/src/app/login/page.tsx
// This page is for logging in to the application.
// ✅ Improved login page UI + logic
'use client'

import { signIn, useSession } from 'next-auth/react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import React, { useEffect, useState } from 'react'
import Link from 'next/link'

export default function LoginPage() {
  const { data: session } = useSession()
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  

  useEffect(() => {
    if (session?.user?.email) {
      router.push('/')
    }
  }, [session, router])

  const handleLogin = async () => {
    if (!email || !password) return alert("Please enter both email and password.")
    const result = await signIn('credentials', {
      email,
      password,
      redirect: false
    })
    if (result?.error) {
      alert("Login failed: " + result.error)
    } else {
      router.push('/')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-12 bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-xl font-bold text-center mb-2">Sign In</h2>
      <p className="text-sm text-center text-gray-500 mb-4">
        Don’t have an account?{' '}
        <a href="/signup" className="text-blue-600 hover:underline">Create one</a>
      </p>
      

      <div className="space-y-4">
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
        {/* Added a link to the forgot password page: */}
        <div className="text-sm text-right">
          <Link href="/login/forgot-password" className="font-medium text-blue-600 hover:text-blue-500">
            Forgot your password?
          </Link>
        </div>

        <Button className="w-full" onClick={handleLogin}>
          Sign In
        </Button>

        <div className="text-center text-sm text-gray-500">or sign in with</div>

        <div className="flex justify-center space-x-4">
          <Button onClick={() => signIn('google')} variant="outline">Google</Button>
        </div>
      </div>
    </div>
  )
}
