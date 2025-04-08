// ✅ File: frontend/src/app/layout.tsx
//✅ Shared layout
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import NavBar from '@/components/NavBar'  // ✅ import your new NavBar
import { ReactNode } from 'react' 
import SessionWrapper from '@/components/SessionWrapper' // ✅ integrate the NextAuth session provider
import ToasterComponent from "@/components/ui/toaster" // ✅ Import at top

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Find My Dream Jobs',
  description: 'Smart job search & resume optimizer',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <SessionWrapper>
          <NavBar />
          {children}
        </SessionWrapper>
        <ToasterComponent /> {/* ✅ Add Toaster component here */}
      </body>
    </html>
  )
}