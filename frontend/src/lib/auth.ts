// ✅ File: frontend/src/lib/auth.ts
// This file configures NextAuth for Google and credentials-based login
import CredentialsProvider from "next-auth/providers/credentials"
import GoogleProvider from "next-auth/providers/google"
import type { NextAuthOptions } from "next-auth"
import { useUserId } from "@/hooks/useUserId"
import { BACKEND_BASE_URL } from '@/lib/env'

export const authOptions: NextAuthOptions = {
  //trustHost: true,  // ✅ Auto-detect URL from request headers for preview environments
  providers: [
    // 🔐 Google login
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    }),

    // 🔐 Email/Password login
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },  
      async authorize(credentials, req) {
        try {
          // Derive backend URL from the incoming request's host header.
          // authorize() always runs server-side. BACKEND_BASE_URL is a module-level
          // constant resolved at startup — in preview it resolves to the PRODUCTION
          // backend (env-group NEXT_PUBLIC_API_BASE_URL overrides render.yaml previewValue).
          // Instead, read 'x-forwarded-host' (set by Cloudflare CDN) or 'host' from the
          // live HTTP request, which always reflects the actual FE hostname being served.
          //   Preview:    x-forwarded-host = 'findmydreamjobs-pr-57.onrender.com' → derive preview BE
          //   Production: x-forwarded-host = 'findmydreamjobs.com'               → no match → fallback
          //   Dev:        host             = 'localhost:3000'                     → no match → fallback
          const hostHeader = String(
            req?.headers?.['x-forwarded-host'] || req?.headers?.host || ''
          ).split(',')[0].trim()
          const prMatch = hostHeader.match(/findmydreamjobs-pr-(\d+)\.onrender\.com/)
          const backendUrl = prMatch
            ? `https://findmydreamjobs-service-pr-${prMatch[1]}.onrender.com`
            : BACKEND_BASE_URL

          console.log("🔍 Attempting login to:", `${backendUrl}/auth/login`)
          console.log("🔍 Host header:", hostHeader)
          console.log("🔍 Email:", credentials?.email)

          const response = await fetch(`${backendUrl}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: credentials?.email,
              password: credentials?.password,
            }),
          })

          console.log("🔍 Response status:", response.status)
          console.log("🔍 Response OK:", response.ok)

          // ✅ Only parse JSON if the response is OK
          if (!response.ok) {
            const text = await response.text()
            console.error("❌ Login failed:", text)
            console.error("❌ Response headers:", Array.from(response.headers.entries()))
            return null
          }

          const user = await response.json()
          console.log("✅ Login successful, user:", JSON.stringify(user, null, 2))

          if (response.ok && user) {
            // ✅ Save token and user_id for later use
            if (typeof window !== "undefined") {
              localStorage.setItem("token", user.token)
              localStorage.setItem("user_id", user.user_id?.toString() || "")
              console.log("✅ Saved to localStorage - token:", user.token ? "present" : "undefined")
            }
          // ✅ Optional: store user_id in localStorage (only works client-side)
          if (typeof window !== "undefined" && user?.user_id) {
            localStorage.setItem("user_id", String(user.user_id))
          }
            return user
          }
          return null
        } catch (err) {
          console.error("❌ Login error:", err)
          console.error("❌ Error stack:", (err as Error).stack)
          return null
        }
      },
    }),
  ],
  pages: {
    signIn: "/login",
    error: "/login", // redirect to login on error
  },

  // 🔄 Session strategy
  session: {
    strategy: "jwt",
  },

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = (user as any).user_id || user.id
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.id as string
        session.user.name = token.name as string
        session.user.email = token.email as string
      }
      return session
    },
  },
}

// ✅ Check if user is authenticated
export function isAuthenticated(): boolean {
  return useUserId() !== null
}

// ✅ Helper: Get JWT token from localStorage (for auth headers)
export function getToken(): string | null {
  return localStorage.getItem("token") || null
}