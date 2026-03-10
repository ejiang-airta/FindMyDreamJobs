// File: src/components/ui/SourceBadge.tsx
// Indicates where a job came from: JSearch API search, Job Intel (JDI/Gmail), or manual paste.
// Used on My Jobs list, Applications kanban cards, and Job Intel job cards.

import React from 'react'
import { cn } from '@/lib/utils'

export type JobSource = 'search' | 'intel' | 'manual'

interface SourceBadgeProps {
  source: JobSource
  className?: string
}

const SOURCE_CONFIG: Record<JobSource, { label: string; className: string }> = {
  search: {
    label: '🔍 Search',
    className: 'bg-blue-50 text-blue-600 border border-blue-200',
  },
  intel: {
    label: '✦ Intel',
    className: 'bg-indigo-50 text-indigo-600 border border-indigo-200',
  },
  manual: {
    label: '✏ Manual',
    className: 'bg-gray-50 text-gray-500 border border-gray-200',
  },
}

export function SourceBadge({ source, className }: SourceBadgeProps) {
  const config = SOURCE_CONFIG[source]

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium whitespace-nowrap',
        config.className,
        className
      )}
    >
      {config.label}
    </span>
  )
}

export default SourceBadge
