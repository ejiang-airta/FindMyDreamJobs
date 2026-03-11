"use client"

import { useState, useEffect } from "react"
import { useSession } from "next-auth/react"
import { useUserId } from "@/hooks/useUserId"
import { getUserProfile, updateUserProfile } from "@/lib/jdi-api"
import { AppButton } from "@/components/ui/AppButton"
import { toast } from "sonner"
import { cn } from "@/lib/utils"

const WORK_ARRANGEMENTS = ["Remote", "Hybrid", "On-site"] as const

export function ProfileSection() {
  const { data: session } = useSession()
  const userId = useUserId()

  const [targetRole, setTargetRole]         = useState("")
  const [targetLocation, setTargetLocation] = useState("")
  const [workArrangements, setWorkArrangements] = useState<string[]>(["Remote", "Hybrid"])
  const [loading, setLoading]   = useState(true)
  const [saving, setSaving]     = useState(false)

  const displayName = session?.user?.name  ?? "—"
  const email       = session?.user?.email ?? "—"
  // Google OAuth users have an image URL set by NextAuth
  const isOAuth = !!(session?.user?.image)

  useEffect(() => {
    if (!userId) return
    getUserProfile(userId)
      .then(profile => {
        if (profile) {
          if (profile.target_titles?.[0])    setTargetRole(profile.target_titles[0])
          if (profile.target_locations?.[0]) setTargetLocation(profile.target_locations[0])
        }
        const stored = localStorage.getItem(`work_arrangement_${userId}`)
        if (stored) {
          try { setWorkArrangements(JSON.parse(stored)) } catch { /* ignore */ }
        }
      })
      .catch(() => {}) // 404 = no profile yet, that's fine
      .finally(() => setLoading(false))
  }, [userId])

  const toggleArrangement = (arr: string) => {
    setWorkArrangements(prev =>
      prev.includes(arr) ? prev.filter(a => a !== arr) : [...prev, arr]
    )
  }

  const handleSave = async () => {
    if (!userId) return
    setSaving(true)
    try {
      await updateUserProfile(userId, {
        target_titles:    targetRole.trim()     ? [targetRole.trim()]     : [],
        target_locations: targetLocation.trim() ? [targetLocation.trim()] : [],
      })
      localStorage.setItem(`work_arrangement_${userId}`, JSON.stringify(workArrangements))
      toast.success("Profile saved")
    } catch {
      toast.error("Failed to save profile")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900">Profile</h2>
        <p className="text-sm text-muted-foreground mt-0.5">
          Your personal info and job search preferences
        </p>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm divide-y divide-gray-100">

        {/* Account info (read-only) */}
        <div className="p-6 space-y-4">
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Account</h3>
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input
                type="text"
                value={displayName}
                disabled
                className="w-full px-3 py-2 border rounded-lg text-sm bg-gray-50 text-gray-500 cursor-not-allowed"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <div className="relative">
                <input
                  type="email"
                  value={email}
                  disabled
                  className="w-full px-3 py-2 border rounded-lg text-sm bg-gray-50 text-gray-500 cursor-not-allowed pr-16"
                />
                {isOAuth && (
                  <span className="absolute right-2 top-1/2 -translate-y-1/2 text-[10px] font-medium bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded">
                    Google
                  </span>
                )}
              </div>
            </div>
          </div>
          <p className="text-xs text-muted-foreground">
            Name and email are managed by your sign-in provider and cannot be changed here.
          </p>
        </div>

        {/* Job search preferences */}
        <div className="p-6 space-y-5">
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Job Search Preferences</h3>

          {loading ? (
            <p className="text-sm text-muted-foreground">Loading...</p>
          ) : (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Target Role
                </label>
                <input
                  type="text"
                  value={targetRole}
                  onChange={e => setTargetRole(e.target.value)}
                  placeholder="e.g. Senior Software Engineer"
                  className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Preferred Location
                </label>
                <input
                  type="text"
                  value={targetLocation}
                  onChange={e => setTargetLocation(e.target.value)}
                  placeholder="e.g. San Francisco, CA or Remote"
                  className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Work Arrangement
                </label>
                <div className="flex flex-wrap gap-2">
                  {WORK_ARRANGEMENTS.map(arr => (
                    <button
                      key={arr}
                      onClick={() => toggleArrangement(arr)}
                      className={cn(
                        "px-4 py-2 rounded-lg text-sm font-medium border transition-colors",
                        workArrangements.includes(arr)
                          ? "bg-blue-600 text-white border-blue-600"
                          : "bg-white text-gray-600 border-gray-200 hover:border-blue-300 hover:text-blue-600"
                      )}
                    >
                      {arr}
                    </button>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="flex justify-end">
        <AppButton onClick={handleSave} disabled={saving || loading}>
          {saving ? "Saving…" : "Save Changes"}
        </AppButton>
      </div>
    </div>
  )
}
