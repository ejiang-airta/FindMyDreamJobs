// File: frontend/src/app/jdi/setup/page.tsx
// Redirect shim — Job Intel setup has moved to /settings#jdi.
// This route is kept alive so the Gmail OAuth callback (?jdi_connected=true /
// ?jdi_error=true) is forwarded to the new Settings page correctly.
"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { Protected } from "@/components/Protected"

export default function ProtectedPage() {
  return (
    <Protected>
      <JDISetupRedirect />
    </Protected>
  )
}

function JDISetupRedirect() {
  const router = useRouter()

  useEffect(() => {
    // Forward any OAuth callback query params (?jdi_connected=true, ?jdi_error=true)
    const params = new URLSearchParams(window.location.search)
    const qs = params.toString()
    router.replace(`/settings${qs ? `?${qs}` : ""}#jdi`)
  }, [router])

  return (
    <div className="flex items-center justify-center min-h-[50vh]">
      <p className="text-sm text-muted-foreground">Redirecting to Settings…</p>
    </div>
  )
}
