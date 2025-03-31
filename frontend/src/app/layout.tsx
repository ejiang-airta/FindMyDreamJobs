//✅ Shared layout
// /frontend/src/app/layout.tsx
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import NavBar from '@/components/NavBar'  // ✅ import your new NavBar


const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Find My Dream Jobs',
  description: 'Smart job search & resume optimizer',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <NavBar />  {/* ✅ Add this line */}
        {children}
      </body>
    </html>
  )
}
