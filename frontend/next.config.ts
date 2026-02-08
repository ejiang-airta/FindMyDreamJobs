//File: /frontend/next.config.ts

import type { NextConfig } from "next"

// ✅ DEBUG: Log environment variables during build (visible in GitLab CI logs)
console.log("==========================================")
console.log("🔍 BUILD-TIME ENVIRONMENT VARIABLES:")
console.log("🔍 NEXTAUTH_URL:", process.env.NEXTAUTH_URL)
console.log("🔍 NEXTAUTH_SECRET:", process.env.NEXTAUTH_SECRET ? "SET" : "NOT SET")
console.log("🔍 NEXT_PUBLIC_API_BASE_URL:", process.env.NEXT_PUBLIC_API_BASE_URL)
console.log("🔍 NODE_ENV:", process.env.NODE_ENV)
console.log("==========================================")

const nextConfig: NextConfig = {
  reactStrictMode: true,
  eslint: {
    ignoreDuringBuilds: true,
  },
}

export default nextConfig
