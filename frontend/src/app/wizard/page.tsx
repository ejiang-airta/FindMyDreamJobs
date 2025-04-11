// ✅ File: frontend/src/app/wizard/page.tsx (updated with Prev/Next buttons)
'use client'

import { useEffect, useState } from 'react'
import UploadResumePage from '@/app/upload/page'
import AnalyzePage from '@/app/analyze/page'
import MatchScore from '@/app/match/page'
import OptimizeResumePage from '@/app/optimize/page'
import ApplyPage from '@/app/apply/page'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { Loader } from 'lucide-react'
import { Button } from '@/components/ui/button'

const steps = ['upload', 'analyze', 'match', 'optimize', 'apply']
const stepLabels = ['Upload Resume', 'Analyze Job', 'Match Score', 'Optimize Resume', 'Apply Job']

export default function WizardPage() {
  const [currentStep, setCurrentStep] = useState('upload')
  const { data: session } = useSession()
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

  const currentIndex = steps.indexOf(currentStep)

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
      case 'upload': return <UploadResumePage isWizard onSuccess={() => updateStep('analyze')} />
      case 'analyze': return <AnalyzePage isWizard onSuccess={() => updateStep('match')} />
      case 'match': return <MatchScore isWizard onSuccess={() => updateStep('optimize')} />
      case 'optimize': return <OptimizeResumePage userId={userId} isWizard onSuccess={() => updateStep('apply')} />
      case 'apply': return <ApplyPage isWizard />
      default: return <UploadResumePage isWizard onSuccess={() => updateStep('analyze')} />
    }
  }

  const handlePrev = () => {
    if (currentIndex > 0) updateStep(steps[currentIndex - 1])
  }

  const handleNext = () => {
    if (currentIndex < steps.length - 1) updateStep(steps[currentIndex + 1])
  }

  if (!email) {
    return (
      <div className="text-center mt-10 text-gray-500">
        <Loader className="mx-auto animate-spin" /> Loading...
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto mt-8">
      <h1 className="text-3xl font-bold text-center mb-6">🚀 Smart Job Application Wizard</h1>
      <div className="flex justify-between items-center mb-6">
        {stepLabels.map((label, i) => (
          <div
            key={label}
            className={`text-sm text-center w-full px-1 py-2 rounded-md font-medium ${steps[i] === currentStep
              ? 'bg-blue-600 text-white'
              : steps.indexOf(steps[i]) < currentIndex
                ? 'bg-green-500 text-white'
                : 'bg-gray-200 text-gray-600'}`}
          >
            {label}
          </div>
        ))}
      </div>

      <div className="bg-white shadow-md rounded-md p-6">
        {renderStep()}

        {/* 👇 Prev/Next Buttons */}
        <div className="flex justify-between pt-6">
          <Button onClick={handlePrev} disabled={currentIndex === 0} variant="secondary">
            ⬅️ Prev
          </Button>
          <Button onClick={handleNext} disabled={currentIndex === steps.length - 1}>
            Next ➡️
          </Button>
        </div>
      </div>
    </div>
  )
}
