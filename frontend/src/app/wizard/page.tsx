// ✅ File: frontend/src/app/wizard/page.tsx
// This page is for the wizard mode to guide the user through the process of applying for a job.

'use client'

import { useEffect, useState } from 'react'
import UploadResume from '@/components/UploadResume'
import AnalyzeJob from '@/components/AnalyzeJob'
import MatchScore from '@/components/MatchScore'
import OptimizeResume from '@/components/OptimizeResume'
import ApplyJob from '@/components/ApplyJob'
import { BACKEND_BASE_URL }  from '@/lib/env'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { Loader } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useUserId } from '@/hooks/useUserId'

const steps = ['upload', 'analyze', 'match', 'optimize', 'apply']
const stepLabels = ['Upload Resume', 'Analyze Job', 'Match Score', 'Optimize Resume', 'Apply Job']

export default function ProtectedPage() {
  const { data: session, status } = useSession()
  const userId = useUserId()

    if (status === "loading") return <p>Loading...</p>
    if (!session?.user || !userId) return <p>Unauthorized or user ID missing</p>

    return <WizardPage />
  }

function WizardPage() {
  const [currentStep, setCurrentStep] = useState<string | null>(null)
  const [isReady, setIsReady] = useState(false)
  const [stepComplete, setStepComplete] = useState(false)
  const { data: session, status } = useSession()
  const router = useRouter()

  const email = session?.user?.email || ''
  const userId = useUserId()

  useEffect(() => {
    if (!email || !userId) return

    console.log("📦 Wizard: email =", email)
    console.log("📦 Wizard: user_id =", userId)
    localStorage.setItem('wizard_mode', 'true')

    fetch(`${BACKEND_BASE_URL}/wizard/progress/get`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    })
      .then(res => res.json())
      .then(data => {
        const step = data?.step
        console.log("📥 Wizard Progress Step:", step)

        setCurrentStep(step && steps.includes(step) ? step : 'upload')

        setIsReady(true)
      })
      .catch(err => {
        console.error("❌ Failed to fetch wizard progress:", err)
        setCurrentStep('upload')
        setIsReady(true)
      })
  }, [email, userId])

  const updateStep = async (step: string) => {
    console.log("🔁 Moving to step:", step)
    setCurrentStep(step)
    setStepComplete(false)
    await fetch(`${BACKEND_BASE_URL}/wizard/progress`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, step })
    })
  }

  const goToPrevStep = () => {
    const idx = steps.indexOf(currentStep || '')
    if (idx > 0) updateStep(steps[idx - 1])
  }

  const goToNextStep = () => {
    const idx = steps.indexOf(currentStep || '')
    if (idx < steps.length - 1) updateStep(steps[idx + 1])
  }

  const renderStep = () => {
    if (!userId) return <p className="text-center text-red-500">❌ User ID not found.</p>

    const commonControls = (
      <>
        {stepComplete && <p className="text-green-600 text-sm mt-4">✅ Step completed. Click Next to continue.</p>}
        <div className="flex justify-between mt-6">
          <Button variant="secondary" onClick={goToPrevStep} disabled={steps.indexOf(currentStep || '') === 0}>
            ⬅️ Prev
          </Button>
          {currentStep !== 'apply' && (
            <Button onClick={goToNextStep} disabled={!stepComplete}>
              Next ➡️
            </Button>
          )}
        </div>
      </>
    )

    switch (currentStep) {
      case 'upload':
        return (
          <>
            <UploadResume isWizard onSuccess={() => setStepComplete(true)} />
            {stepComplete && <p className="text-green-600 text-sm mt-4">✅ Step completed. Click Next to continue.</p>}
            <div className="flex justify-end mt-6"> {/* ✅ Only show "Next" */}
              <Button onClick={goToNextStep} disabled={!stepComplete}>
                Next ➡️
              </Button>
            </div>
          </>
        )
      case 'analyze':
        return (
          <>
            <AnalyzeJob isWizard onSuccess={() => setStepComplete(true)} />
            {commonControls}
          </>
        )
        case 'match':
          return (
            <>
              <MatchScore
                userId={String(userId)}
                isWizard
                onSuccess={() => setStepComplete(true)}
              />
              {commonControls}
            </>
          )
      case 'optimize':
        return (
          <>
            <OptimizeResume userId={String(userId)} isWizard onSuccess={() => setStepComplete(true)} />  
            {commonControls}
          </>
        )
      case 'apply':
        return (
          <>
            <ApplyJob userId={String(userId)} isWizard />
            <div className="flex justify-between mt-6">
              <Button variant="secondary" onClick={goToPrevStep}>⬅️ Prev</Button>
              <Button
                onClick={() => {
                  localStorage.removeItem('wizard_mode')
                  router.push('/applications')
                }}
              >
                ✅ Finish
              </Button>
            </div>
          </>
        )
      default:
        return <p className="text-center text-red-500">Unknown step. Starting over...</p>
    }
  }

  if (status === 'loading' || !isReady || !currentStep) {
    return (
      <div className="text-center mt-10 text-gray-500">
        <Loader className="mx-auto animate-spin" /> Loading...
      </div>
    )
  }

  if (status === 'unauthenticated') {
    return <p className="text-center text-gray-500 mt-10">🔐 Please log in to access the wizard.</p>
  }

  return (
    <div className="max-w-3xl mx-auto mt-8">
      <h1 className="text-3xl font-bold text-center mb-6">🚀 Smart Job Application Wizard</h1>
      <div className="flex justify-between items-center mb-6">
        {stepLabels.map((label, i) => (
          <div
            key={label}
            className={`text-sm text-center w-full px-1 py-2 rounded-md font-medium ${
              steps[i] === currentStep
                ? 'bg-blue-600 text-white'
                : steps.indexOf(steps[i]) < steps.indexOf(currentStep || '')
                ? 'bg-green-500 text-white'
                : 'bg-gray-200 text-gray-600'
            }`}
          >
            {label}
          </div>
        ))}
      </div>
      <div className="bg-white shadow-md rounded-md p-6">{renderStep()}</div>
    </div>
  )
}
