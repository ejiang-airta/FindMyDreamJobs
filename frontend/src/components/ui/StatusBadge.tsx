// File: src/components/ui/StatusBadge.tsx
// Displays an application status with consistent color-coded styling.
// Used on Applications kanban cards, My Jobs list, and job detail panes.

import React from 'react'
import { cn } from '@/lib/utils'

export type ApplicationStatus =
  | 'applied'
  | 'review'
  | 'in_review'
  | 'reviewing'
  | 'interview'
  | 'interviewing'
  | 'offer'
  | 'rejected'

interface StatusBadgeProps {
  status: ApplicationStatus | string
  className?: string
}

const STATUS_CONFIG: Record<string, { label: string; className: string }> = {
  applied: {
    label: 'Applied',
    className: 'bg-gray-50 text-gray-600 border border-gray-200',
  },
  review: {
    label: 'In Review',
    className: 'bg-blue-50 text-blue-600 border border-blue-200',
  },
  in_review: {
    label: 'In Review',
    className: 'bg-blue-50 text-blue-600 border border-blue-200',
  },
  reviewing: {
    label: 'In Review',
    className: 'bg-blue-50 text-blue-600 border border-blue-200',
  },
  interview: {
    label: 'Interview',
    className: 'bg-green-50 text-green-700 border border-green-200',
  },
  interviewing: {
    label: 'Interview',
    className: 'bg-green-50 text-green-700 border border-green-200',
  },
  offer: {
    label: '🎉 Offer',
    className: 'bg-purple-50 text-purple-700 border border-purple-200',
  },
  rejected: {
    label: 'Rejected',
    className: 'bg-red-50 text-red-500 border border-red-200',
  },
}

const FALLBACK_CONFIG = {
  label: 'Unknown',
  className: 'bg-gray-50 text-gray-400 border border-gray-200',
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const normalised = status?.toLowerCase?.() ?? ''
  const config = STATUS_CONFIG[normalised] ?? FALLBACK_CONFIG

  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium whitespace-nowrap',
        config.className,
        className
      )}
    >
      {config.label}
    </span>
  )
}

export default StatusBadge
