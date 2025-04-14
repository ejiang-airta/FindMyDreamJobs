// ✅ File: frontend/src/app/signup/page.tsx
'use client'

import { signIn } from 'next-auth/react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import React, { useState } from 'react'
import { BACKEND_BASE_URL }  from '@/lib/env'

export default function SignupPage() {
  const router = useRouter()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSignup = async () => {
    if (!email || !password || !fullName) {
      return alert('Please enter all fields.')
    }

    try {
      const res = await fetch(`${BACKEND_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name: fullName, email, password })
      })

      const data = await res.json()
      if (!res.ok) return alert("Sign up failed: " + data.detail)

      const result = await signIn('credentials', {
        email,
        password,
        redirect: false
      })

      if (result?.error) {
        alert('Login failed after signup.')
      } else {
        router.push('/')
      }

    } catch (err) {
      alert('Unexpected error during signup.')
      console.error(err)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-12 bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-xl font-bold text-center mb-2">Create New Account</h2>
      <p className="text-sm text-center text-gray-500 mb-4">
        Already have an account?{' '}
        <a href="/login" className="text-blue-600 hover:underline">Sign In</a>
      </p>

      <div className="space-y-4">
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
          placeholder="Create a password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button className="w-full" onClick={handleSignup}>
          Create Account
        </Button>
      </div>
    </div>
  )
}
