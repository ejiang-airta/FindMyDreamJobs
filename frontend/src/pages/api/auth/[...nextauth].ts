// ✅ File: frontend/src/pages/api/auth/[...nextauth].ts
import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import { NextApiHandler } from "next"
import CredentialsProvider from 'next-auth/providers/credentials'


const handler: NextApiHandler = (req, res) => 
  NextAuth(req, res, {
    providers: [
      GoogleProvider({
        clientId: process.env.GOOGLE_CLIENT_ID!,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      }),
      CredentialsProvider({
        name: "Sign in with Email",
        credentials: {
          name: { label: "Name", type: "text" },
          email: { label: "Email", type: "email" },
        },
        async authorize(credentials) {
          if (!credentials?.email || !credentials?.name) return null

          return {
            id: credentials.email, // temporary ID
            email: credentials.email,
            name: credentials.name,
          }
        },
      }),
    ],
    session: {
      strategy: "jwt",
    },
    callbacks: {
      async jwt({ token, user }) {
        if (user) {
          token.id = user.id
          token.name = user.name
          token.email = user.email
        }
        return token
      },
      async session({ session, token }) {
        if (token) {
          session.user = {
            id: token.id as string,
            name: token.name as string,
            email: token.email as string,
          }
        }
        return session
      },
    },
  })

export default handler