// frontend/src/components/SessionWrapper.tsx
// This component wraps the children with the SessionProvider from next-auth.
// This is useful for managing user sessions and authentication state in a React application.
// The SessionProvider component provides the session context to its children, allowing them to access the session data and authentication methods.
'use client'

import { SessionProvider } from 'next-auth/react'
import React from 'react'

export default function SessionWrapper({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>
}
