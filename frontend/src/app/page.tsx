// ✅ File: frontend/src/app/page.tsx
'use client'

import { Button } from '@/components/ui/button'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'

export default function HomePage() {
  const { data: session } = useSession()
  const router = useRouter()

  const handleGetStarted = () => {
    router.push('/wizard') // 👉 Go to the step-by-step onboarding wizard
  }
  const handleApplicationStatus = () => {
    router.push('/applications') // 👉 Show user's application status
  }
  const handleResumeAnalysis = () => {
    router.push('/upload') // 👉 Take user to resume analysis
  }

  const handleJobAnalysis = () => {
    router.push('/analyze') // 👉 Take user to job analysis
  }

  const handleLearnMore = () => {
    router.push('/about') // 👉 Take user to /about page
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-600 to-blue-400 text-white text-center p-10">
      <h1 className="text-5xl font-extrabold mb-4">Find Your Dream Job</h1>
      <p className="text-lg mb-8">
        Upload your resume and let our AI match you with the perfect job opportunities. 
      </p>
      <p className="text-lg font-semibold mb-8">
        IMPORTANT: Sign-up now for a two-week free trial!
      </p>
      {session?.user && (
        <p className="text-md font-semibold mb-6">
          Welcome back, {session.user.name}!
        </p>
      )}

      <div className="flex justify-center space-x-4">
        <Button onClick={handleGetStarted} className="bg-white text-blue-600 hover:bg-blue-100">
          Get Started
        </Button>
        <Button onClick={handleLearnMore} variant="ghost" className="text-white border border-white">
          Learn More
        </Button>
      </div>

      <section className="mt-20 bg-white text-gray-800 p-10 rounded-lg shadow-lg max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold mb-4">Why Choose Us</h2>
        <p className="mb-10">
          Our platform uses advanced AI to help you find and land your dream job.
        </p>

        <div className="grid md:grid-cols-3 gap-8">
          <div onClick={handleResumeAnalysis}  className="p-4 rounded shadow-md border">
            <h3 className="font-semibold text-lg mb-2">Smart Resume Analysis</h3>
            <p className="text-sm">Get insights about your resume and how it matches with job requirements.</p>
          </div>
          <div onClick={handleJobAnalysis} className="p-4 rounded shadow-md border">
            <h3 className="font-semibold text-lg mb-2">Automated Job Analysis</h3>
            <p className="text-sm">Find jobs that match your skills and experience automatically.</p>
          </div>
          <div onClick={handleApplicationStatus} className="p-4 rounded shadow-md border">
            <h3 className="font-semibold text-lg mb-2">Application Tracking</h3>
            <p className="text-sm">Track all your job applications in one place.</p>
          </div>
        </div>

        <div className="mt-10">
          <p className="text-xl font-semibold">Ready to find your dream job?</p>
          <Button onClick={handleGetStarted} className="mt-4 bg-blue-600 hover:bg-blue-700">
            Start your journey today.
          </Button>
        </div>
      </section>
    </div>
  )
}
