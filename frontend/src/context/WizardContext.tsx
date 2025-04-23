//File: frontend/src/context/WizardContext.tsx
// // This file contains the context and provider for the wizard state.
'use client'

import { createContext, useContext, useState, ReactNode } from 'react'

type WizardState = {
    resumeId: string
    setResumeId: React.Dispatch<React.SetStateAction<string>>
    jobId: string
    setJobId: React.Dispatch<React.SetStateAction<string>>
    justification: string
    setJustification: React.Dispatch<React.SetStateAction<string>>
    jobDescription: string
    setJobDescription: React.Dispatch<React.SetStateAction<string>>
    resumeText: string
    setResumeText: React.Dispatch<React.SetStateAction<string>>
  }
  
  

const WizardContext = createContext<WizardState | undefined>(undefined)

export const WizardProvider = ({ children }: { children: ReactNode }) => {
  const [resumeText, setResumeText] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [justification, setJustification] = useState('')
  const [resumeId, setResumeId] = useState('')
  const [jobId, setJobId] = useState('')

  return (
    <WizardContext.Provider
        value={{
            resumeText, setResumeText,
            jobDescription, setJobDescription,
            justification, setJustification,
            resumeId, setResumeId,
            jobId, setJobId,
        }}
    >
      {children}
    </WizardContext.Provider>
  )
}

export const useWizardState = () => {
  const context = useContext(WizardContext)
  if (!context) {
    throw new Error('useWizardState must be used within WizardProvider')
  }
  return context
}
