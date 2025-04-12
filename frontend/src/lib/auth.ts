// ✅ File: frontend/src/lib/auth.ts
import CredentialsProvider from "next-auth/providers/credentials"
import GoogleProvider from "next-auth/providers/google"
import type { NextAuthOptions } from "next-auth"

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
          const response = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: credentials?.email,
              password: credentials?.password,
            }),
          })

          const user = await response.json()

          if (response.ok && user) return user
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

// ✅ Helper: Safely get user_id from localStorage
export function getUserId(): number | null {
  const value = localStorage.getItem("user_id")
  const parsed = parseInt(value || "", 10)
  return isNaN(parsed) ? null : parsed
}

// ✅ Check if user is authenticated
export function isAuthenticated(): boolean {
  return getUserId() !== null
}
