"use client"

import { useState, useEffect } from "react"
import { User, Zap, Bell, CreditCard } from "lucide-react"
import { cn } from "@/lib/utils"
import { Protected } from "@/components/Protected"
import { ProfileSection } from "@/components/settings/ProfileSection"
import { JDISection } from "@/components/settings/JDISection"
import { NotificationsSection } from "@/components/settings/NotificationsSection"
import { MembershipSection } from "@/components/settings/MembershipSection"

const NAV_ITEMS = [
  { id: "profile",       label: "Profile",       icon: User },
  { id: "jdi",           label: "Job Intel",      icon: Zap },
  { id: "notifications", label: "Notifications",  icon: Bell },
  { id: "membership",    label: "Membership",     icon: CreditCard },
] as const

type SectionId = (typeof NAV_ITEMS)[number]["id"]

export default function ProtectedPage() {
  return (
    <Protected>
      <SettingsPage />
    </Protected>
  )
}

function SettingsPage() {
  const [activeSection, setActiveSection] = useState<SectionId>("profile")

  // Sync with URL hash so /settings#jdi deep-links work
  useEffect(() => {
    const readHash = () => {
      const hash = window.location.hash.replace("#", "") as SectionId
      if (NAV_ITEMS.some(n => n.id === hash)) setActiveSection(hash)
    }
    readHash()
    window.addEventListener("hashchange", readHash)
    return () => window.removeEventListener("hashchange", readHash)
  }, [])

  const navigateTo = (id: SectionId) => {
    window.location.hash = id
    setActiveSection(id)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-10">

        {/* Page header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Manage your profile, Job Intel, and account preferences
          </p>
        </div>

        {/* Mobile: horizontal scroll tab bar */}
        <div className="md:hidden mb-6 flex gap-1 overflow-x-auto pb-1">
          {NAV_ITEMS.map(item => {
            const Icon = item.icon
            return (
              <button
                key={item.id}
                onClick={() => navigateTo(item.id)}
                className={cn(
                  "flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors shrink-0",
                  activeSection === item.id
                    ? "bg-blue-600 text-white"
                    : "bg-white border border-gray-200 text-gray-600 hover:text-gray-900"
                )}
              >
                <Icon className="h-3.5 w-3.5" />
                {item.label}
              </button>
            )
          })}
        </div>

        <div className="flex gap-8">
          {/* Desktop sidebar */}
          <aside className="hidden md:block w-52 shrink-0">
            <nav className="space-y-1 sticky top-6">
              {NAV_ITEMS.map(item => {
                const Icon = item.icon
                return (
                  <button
                    key={item.id}
                    onClick={() => navigateTo(item.id)}
                    className={cn(
                      "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-left",
                      activeSection === item.id
                        ? "bg-blue-50 text-blue-700"
                        : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                    )}
                  >
                    <Icon className="h-4 w-4 shrink-0" />
                    <span className="flex-1">{item.label}</span>
                    {item.id === "jdi" && (
                      <span className="text-[10px] font-semibold bg-indigo-100 text-indigo-700 px-1.5 py-0.5 rounded">
                        PRO
                      </span>
                    )}
                  </button>
                )
              })}
            </nav>
          </aside>

          {/* Content area */}
          <main className="flex-1 min-w-0">
            {activeSection === "profile"       && <ProfileSection />}
            {activeSection === "jdi"           && <JDISection />}
            {activeSection === "notifications" && <NotificationsSection />}
            {activeSection === "membership"    && <MembershipSection />}
          </main>
        </div>

      </div>
    </div>
  )
}
