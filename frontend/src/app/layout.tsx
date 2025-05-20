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
      <head>
        {/* Google Tag Manager head script*/}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
              new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
              j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
              'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            })(window,document,'script','dataLayer','GTM-K7DB35BN');`,
          }}
        />
        {/* End Google Tag Manager */}
      </head>
      <body className={inter.className}>
        {/* Google Tag Manager (noscript) for body */}
        <noscript
          suppressHydrationWarning
          dangerouslySetInnerHTML={{
            __html: `
              <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-K7DB35BN"
              height="0" width="0" style="display:none;visibility:hidden"></iframe>
            `,
          }}
        />
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