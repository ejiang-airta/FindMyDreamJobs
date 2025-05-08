// ✅ File: frontend/src/app/layout.tsx
//✅ Shared layout
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import NavBar from '@/components/NavBar'  // ✅ import your new NavBar
import { ReactNode } from 'react' 
import SessionWrapper from '@/components/SessionWrapper' // ✅ integrate the NextAuth session provider
import { Toaster } from 'sonner'



const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Find My Dream Jobs',
  description: 'Smart job search & resume optimizer',
  icons: {
    icon: '/favicon.ico',
  },
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <SessionWrapper>
          <NavBar />
          {children}
          <Toaster 
          position="top-center"          
          toastOptions={{
            duration: 2000, // Set the global duration to 3 seconds
            style: {
              marginTop: '2rem', // Adjust this value to move the toaster lower
            },
          }} />
        </SessionWrapper>
      </body>
    </html>
  )
}