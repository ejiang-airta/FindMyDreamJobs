// File: frontend/src/app/about/page.tsx
'use client'

import React from 'react'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'

export default function Hero() {
  const router = useRouter()

  return (
    <section className="bg-gradient-to-b from-gray-50 to-white py-20 px-6 text-center">
      <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
        Find Your Dream Job — Powered by AI
      </h1>
      <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto mb-8">
        Our intelligent platform helps you match your resume to the perfect job, optimize it with real-time insights, and track your application progress effortlessly.
      </p>

      <div className="flex justify-center gap-4 flex-wrap">
        <Button className="text-lg px-6 py-3" onClick={() => router.push('/upload')}>
          Upload Resume
        </Button>
        <Button variant="outline" className="text-lg px-6 py-3" onClick={() => router.push('/analyze')}>
          Analyze Job
        </Button>
        <Button variant="secondary" className="text-lg px-6 py-3" onClick={() => router.push('/applications')}>
          View Applications
        </Button>
      </div>

      <div className="mt-12 text-sm text-gray-500">
        <p>
          AI-powered job search tools | Resume & Job Matching | ATS Score Optimization
        </p>
      </div>
    </section>
  )
}
