"use client"

import Link from "next/link"
import { CheckCircle2 } from "lucide-react"
import { AppButton } from "@/components/ui/AppButton"

const FREE_FEATURES = [
  "AI-powered resume analysis",
  "Job description parsing & ATS scoring",
  "Resume optimization suggestions",
  "Job application tracking",
  "Match score calculations",
]

const PRO_FEATURES = [
  "Everything in Free",
  "Job Intel ✦ — automated Gmail scanning",
  "Priority match scoring",
  "Unlimited resume analyses",
  "Early access to new features",
]

export function MembershipSection() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900">Membership</h2>
        <p className="text-sm text-muted-foreground mt-0.5">Your current plan and upgrade options</p>
      </div>

      {/* Current plan banner */}
      <div className="bg-blue-50 border border-blue-100 rounded-xl p-5 flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold text-blue-500 uppercase tracking-wider">Current plan</p>
          <p className="text-2xl font-bold text-blue-700 mt-0.5">Free</p>
        </div>
        <span className="text-xs text-blue-600 bg-blue-100 px-3 py-1 rounded-full font-medium">
          Active
        </span>
      </div>

      {/* Plan comparison */}
      <div className="grid sm:grid-cols-2 gap-4">

        {/* Free card */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5 space-y-4">
          <div>
            <h3 className="font-semibold text-gray-900">Free</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">
              $0{" "}
              <span className="text-sm font-normal text-muted-foreground">/ forever</span>
            </p>
          </div>
          <ul className="space-y-2">
            {FREE_FEATURES.map(f => (
              <li key={f} className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0 mt-0.5" />
                {f}
              </li>
            ))}
          </ul>
          <div className="pt-1">
            <span className="block text-sm text-gray-400 border border-gray-200 px-4 py-2 rounded-lg text-center">
              Current plan
            </span>
          </div>
        </div>

        {/* Pro card */}
        <div className="relative bg-white rounded-xl border-2 border-indigo-200 shadow-sm p-5 space-y-4">
          <div className="absolute -top-3 right-4">
            <span className="bg-indigo-600 text-white text-xs font-semibold px-3 py-1 rounded-full">
              PRO
            </span>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">Pro</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">
              $12{" "}
              <span className="text-sm font-normal text-muted-foreground">/ month</span>
            </p>
          </div>
          <ul className="space-y-2">
            {PRO_FEATURES.map(f => (
              <li key={f} className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="h-4 w-4 text-indigo-500 shrink-0 mt-0.5" />
                {f}
              </li>
            ))}
          </ul>
          <div className="pt-1">
            <Link href="/pricing" className="block w-full">
              <AppButton className="w-full bg-indigo-600 hover:bg-indigo-700 text-white justify-center">
                Upgrade to Pro
              </AppButton>
            </Link>
          </div>
        </div>

      </div>
    </div>
  )
}
