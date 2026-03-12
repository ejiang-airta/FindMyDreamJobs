"use client"

import { useState, useEffect } from "react"
import { useUserId } from "@/hooks/useUserId"
import { AppButton } from "@/components/ui/AppButton"
import { toast } from "sonner"
import { cn } from "@/lib/utils"

interface NotificationPrefs {
  newIntelCandidates: boolean
  interviewReminders: boolean
}

const NOTIFICATION_ITEMS: {
  key: keyof NotificationPrefs
  label: string
  description: string
}[] = [
  {
    key: "newIntelCandidates",
    label: "New Job Intel candidates",
    description: "Get notified when a scan finds new matching job opportunities",
  },
  {
    key: "interviewReminders",
    label: "Interview reminders",
    description: "Reminder emails before scheduled interviews in your pipeline",
  },
]

function Toggle({ on, onChange }: { on: boolean; onChange: () => void }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={on}
      onClick={onChange}
      className={cn(
        "relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500",
        on ? "bg-blue-600" : "bg-gray-200"
      )}
    >
      <span
        className={cn(
          "pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow transition duration-200",
          on ? "translate-x-4" : "translate-x-0"
        )}
      />
    </button>
  )
}

export function NotificationsSection() {
  const userId = useUserId()
  const [prefs, setPrefs] = useState<NotificationPrefs>({
    newIntelCandidates: true,
    interviewReminders: true,
  })

  useEffect(() => {
    if (!userId) return
    const stored = localStorage.getItem(`notification_prefs_${userId}`)
    if (stored) {
      try { setPrefs(JSON.parse(stored)) } catch { /* ignore */ }
    }
  }, [userId])

  const toggle = (key: keyof NotificationPrefs) =>
    setPrefs(prev => ({ ...prev, [key]: !prev[key] }))

  const handleSave = () => {
    if (!userId) return
    localStorage.setItem(`notification_prefs_${userId}`, JSON.stringify(prefs))
    toast.success("Notification preferences saved")
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900">Notifications</h2>
        <p className="text-sm text-muted-foreground mt-0.5">
          Control which email notifications you receive
        </p>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm divide-y divide-gray-100">
        {NOTIFICATION_ITEMS.map(item => (
          <div key={item.key} className="flex items-center justify-between p-5">
            <div className="pr-4">
              <p className="text-sm font-medium text-gray-900">{item.label}</p>
              <p className="text-xs text-muted-foreground mt-0.5">{item.description}</p>
            </div>
            <Toggle on={prefs[item.key]} onChange={() => toggle(item.key)} />
          </div>
        ))}
      </div>

      {/* Coming soon notice */}
      <div className="bg-amber-50 border border-amber-100 rounded-xl p-4">
        <p className="text-sm text-amber-700">
          <strong>Coming soon —</strong> email notifications are not yet live. These preferences
          will take effect when email delivery is enabled in a future update.
        </p>
      </div>

      <div className="flex justify-end">
        <AppButton onClick={handleSave}>Save Preferences</AppButton>
      </div>
    </div>
  )
}
