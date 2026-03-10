// ✅ File: frontend/src/lib/env.ts
// Dynamically sets backend/frontend URLs for Production, Preview, and Dev environments.

const IS_PROD =
  process.env.NODE_ENV === 'production' ||
  process.env.NEXT_PUBLIC_ENV === 'production'

export const BACKEND_BASE_URL = (() => {
  // Client-side: detect preview from hostname
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname
    const prMatch = hostname.match(/findmydreamjobs-pr-(\d+)\.onrender\.com/)
    if (prMatch) {
      return `https://findmydreamjobs-service-pr-${prMatch[1]}.onrender.com`
    }
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://127.0.0.1:8000'
    }
  }
  // Server-side fallback: use NEXT_PUBLIC_API_BASE_URL (baked in at build time).
  // NOTE: In preview the eugene-env-group overrides render.yaml previewValue, so this
  // resolves to the PRODUCTION backend. Auth (authorize in auth.ts) fixes this at
  // request time by reading the 'x-forwarded-host' header directly — no env var needed.
  return process.env.NEXT_PUBLIC_API_BASE_URL || (IS_PROD ? 'https://findmydreamjobs.onrender.com' : 'http://127.0.0.1:8000')
})()

export const FRONTEND_BASE_URL = (() => {
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname
    const prMatch = hostname.match(/findmydreamjobs-pr-(\d+)\.onrender\.com/)
    if (prMatch) {
      return `https://findmydreamjobs-pr-${prMatch[1]}.onrender.com`
    }
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://127.0.0.1:3000'
    }
  }
  return IS_PROD ? 'https://findmydreamjobs.com' : 'http://127.0.0.1:3000'
})()