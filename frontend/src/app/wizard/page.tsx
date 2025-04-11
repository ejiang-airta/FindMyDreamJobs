// ✅ File: frontend/src/app/wizard/page.tsx
'use client'

import { useEffect, useState } from 'react'
import UploadResume from '@/components/UploadResume'
import AnalyzeJob from '@/components/AnalyzeJob'
import MatchScore from '@/components/MatchScore'
import OptimizeResumePage from '@/components/OptimizeResume'
import ApplyJob from '@/components/ApplyJob'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { Loader } from 'lucide-react'

const steps = ['upload', 'analyze', 'match', 'optimize', 'apply']
const stepLabels = ['Upload Resume', 'Analyze Job', 'Match Score', 'Optimize Resume', 'Apply Job']

export default function WizardPage() {
  const [currentStep, setCurrentStep] = useState('upload')
  const { data: session, status } = useSession()
  const router = useRouter()
  const email = session?.user?.email || ''

  useEffect(() => {
    if (!email) return
    localStorage.setItem('wizard_mode', 'true')
    fetch('http://127.0.0.1:8000/wizard/progress/get', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    })
      .then(res => res.json())
      .then(data => setCurrentStep(data.step || 'upload'))
      .catch(() => setCurrentStep('upload'))
  }, [email])

  const updateStep = async (step: string) => {
    setCurrentStep(step)
    await fetch('http://127.0.0.1:8000/wizard/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, step })
    })
  }

  const renderStep = () => {
    const userId = typeof window !== 'undefined' ? localStorage.getItem("user_id") : null
    if (!userId) return <p className="text-center">❌ No user ID found</p>

    switch (currentStep) {
      case 'upload':
        return <UploadResume isWizard onSuccess={() => updateStep('analyze')} />
      case 'analyze':
        return <AnalyzeJob isWizard onSuccess={() => updateStep('match')} />
      case 'match':
        return <MatchScore isWizard onSuccess={() => updateStep('optimize')} />
      case 'optimize':
        return <OptimizeResumePage userId={userId} isWizard onSuccess={() => updateStep('apply')} />
      case 'apply':
        return <ApplyJob userId={userId} isWizard />
      default:
        return <UploadResume isWizard onSuccess={() => updateStep('analyze')} />
    }
  }

  if (status === 'loading') {
    return (
      <div className="text-center mt-10 text-gray-500">
        <Loader className="mx-auto animate-spin" /> Loading...
      </div>
    )
  }
  
  if (!email) return <p className="text-center text-red-600">❌ Unable to load wizard – user not signed in.</p>

  return (
    <div className="max-w-3xl mx-auto mt-8">
      <h1 className="text-3xl font-bold text-center mb-6">🚀 Smart Job Application Wizard</h1>
      <div className="flex justify-between items-center mb-6">
        {stepLabels.map((label, i) => (
          <div
            key={label}
            className={`text-sm text-center w-full px-1 py-2 rounded-md font-medium ${steps[i] === currentStep
              ? 'bg-blue-600 text-white'
              : steps.indexOf(steps[i]) < steps.indexOf(currentStep)
                ? 'bg-green-500 text-white'
                : 'bg-gray-200 text-gray-600'
              }`}
          >
            {label}
          </div>
        ))}
      </div>
      <div className="bg-white shadow-md rounded-md p-6">
        {renderStep()}
      </div>
    </div>
  )
}

