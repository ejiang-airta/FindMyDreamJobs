// ✅ File: frontend/src/lib/auth.ts
import CredentialsProvider from "next-auth/providers/credentials"
import GoogleProvider from "next-auth/providers/google"
import type { NextAuthOptions } from "next-auth"
import { useUserId } from "@/hooks/useUserId"

// 🌐 Dynamically resolve backend API base
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000"

export const authOptions: NextAuthOptions = {
  providers: [
    // 🔐 Email/Password login
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },  
      async authorize(credentials) {
        try {
          const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: credentials?.email,
              password: credentials?.password,
            }),
          })

          const user = await response.json()
          if (response.ok && user) {
            // ✅ Save token and user_id for later use
            if (typeof window !== "undefined") {
              localStorage.setItem("token", user.token)
              localStorage.setItem("user_id", user.user_id?.toString() || "")
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


    // 🔐 Google login
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],

  // 🔄 Session strategy
  session: {
    strategy: "jwt",
  },

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.user = user
      }
      return token
    },
    async session({ session, token }) {
      if (token?.user) {
        session.user = token.user as any
      }
      return session
    },
  },

  pages: {
    signIn: "/login", // Redirects here when login is needed
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