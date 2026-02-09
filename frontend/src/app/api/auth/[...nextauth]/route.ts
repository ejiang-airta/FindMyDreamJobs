// ✅ File: frontend/src/app/api/auth/[...nextauth]/route.ts
import NextAuth from "next-auth"
import { authOptions } from "@/lib/auth"

// ✅ DEBUG: Log NEXTAUTH_URL to verify what value is being used in preview
console.log("🔍 NEXTAUTH_URL:", process.env.NEXTAUTH_URL)
console.log("🔍 NEXTAUTH_SECRET:", process.env.NEXTAUTH_SECRET ? "SET" : "NOT SET")
console.log("🔍 NODE_ENV:", process.env.NODE_ENV)
console.log("🔍 ENV (from render.yaml):", process.env.ENV)

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }
