// ✅ File: frontend/src/pages/api/auth/[...nextauth].ts
import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import { NextApiHandler } from "next"

const handler: NextApiHandler = (req, res) =>
  NextAuth(req, res, {
    providers: [
      GoogleProvider({
        clientId: process.env.GOOGLE_CLIENT_ID!,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      }),
    ],
    secret: process.env.NEXTAUTH_SECRET,
    session: { strategy: "jwt" },
    callbacks: {
      async session({ session, token }: any) {
        session.user.id = token.sub
        return session
      },
      async jwt({ token, account, user }: { token: any, account: any, user: any }) {
        if (account && user) {
          token.id = user.id
        }
        return token
      },
    },
  })

export default handler