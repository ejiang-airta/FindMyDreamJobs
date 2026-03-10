// File: src/components/ui/MatchBadge.tsx
// Displays a job match score with consistent color-coded styling.
// Consolidates match score color logic that was previously duplicated across pages.
//
// Color tiers:
//   ≥ 80%  → green  (strong match)
//   ≥ 60%  → yellow (decent match)
//   < 60%  → orange (weak match)
//   null / undefined → gray (not yet scored)

import React from 'react'
import { cn } from '@/lib/utils'

interface MatchBadgeProps {
  score: number | null | undefined
  showLabel?: boolean   // if true, renders "XX% Match" — default true
  className?: string
}

function getColorClass(score: number): string {
  if (score >= 80) return 'bg-green-50 text-green-700 border border-green-200'
  if (score >= 60) return 'bg-yellow-50 text-yellow-700 border border-yellow-200'
  return 'bg-orange-50 text-orange-700 border border-orange-200'
}

export function MatchBadge({ score, showLabel = true, className }: MatchBadgeProps) {
  if (score == null) {
    return (
      <span
        className={cn(
          'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium whitespace-nowrap',
          'bg-gray-50 text-gray-400 border border-gray-200',
          className
        )}
      >
        {showLabel ? 'Not scored' : '—'}
      </span>
    )
  }

  const rounded = Math.round(score)
  const colorClass = getColorClass(rounded)

  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium whitespace-nowrap',
        colorClass,
        className
      )}
    >
      {showLabel ? `${rounded}% Match` : `${rounded}%`}
    </span>
  )
}

export default MatchBadge
