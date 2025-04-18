// ✅ File: frontend/src/lib/auth.ts
// This file configures NextAuth for Google and credentials-based login
import CredentialsProvider from "next-auth/providers/credentials"
import GoogleProvider from "next-auth/providers/google"
import type { NextAuthOptions } from "next-auth"
import { useUserId } from "@/hooks/useUserId"
import { BACKEND_BASE_URL } from '@/lib/env'

export const authOptions: NextAuthOptions = {
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
      async authorize(credentials) {
        try {
          const response = await fetch(`${BACKEND_BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: credentials?.email,
              password: credentials?.password,
            }),
          })

          // ✅ Only parse JSON if the response is OK
          if (!response.ok) {
            const text = await response.text()
            console.error("❌ Login failed:", text)
            return null
          }

          const user = await response.json()
          if (response.ok && user) {
            // ✅ Save token and user_id for later use
            if (typeof window !== "undefined") {
              localStorage.setItem("token", user.token)
              localStorage.setItem("user_id", user.user_id?.toString() || "")
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