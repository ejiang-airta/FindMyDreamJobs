// File: src/components/ui/CompanyInitial.tsx
// Deterministic colored avatar showing first letter of company name.
// Used on all job cards across Search, Job Intel, My Jobs, and Applications pages.

import React from 'react'
import { cn } from '@/lib/utils'

interface CompanyInitialProps {
  name: string
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

// Deterministic color palette — maps initial letter to a Tailwind bg/text pair.
// Groups of 4-5 letters per color for even distribution across the alphabet.
const COLOR_MAP: Record<string, string> = {
  A: 'bg-blue-100 text-blue-700',
  B: 'bg-blue-100 text-blue-700',
  C: 'bg-violet-100 text-violet-700',
  D: 'bg-violet-100 text-violet-700',
  E: 'bg-emerald-100 text-emerald-700',
  F: 'bg-emerald-100 text-emerald-700',
  G: 'bg-blue-100 text-blue-700',
  H: 'bg-amber-100 text-amber-700',
  I: 'bg-amber-100 text-amber-700',
  J: 'bg-pink-100 text-pink-700',
  K: 'bg-pink-100 text-pink-700',
  L: 'bg-teal-100 text-teal-700',
  M: 'bg-yellow-100 text-yellow-700',
  N: 'bg-yellow-100 text-yellow-700',
  O: 'bg-orange-100 text-orange-700',
  P: 'bg-orange-100 text-orange-700',
  Q: 'bg-purple-100 text-purple-700',
  R: 'bg-red-100 text-red-700',
  S: 'bg-pink-100 text-pink-700',
  T: 'bg-teal-100 text-teal-700',
  U: 'bg-indigo-100 text-indigo-700',
  V: 'bg-indigo-100 text-indigo-700',
  W: 'bg-cyan-100 text-cyan-700',
  X: 'bg-cyan-100 text-cyan-700',
  Y: 'bg-lime-100 text-lime-700',
  Z: 'bg-lime-100 text-lime-700',
}

const DEFAULT_COLOR = 'bg-gray-100 text-gray-600'

const SIZE_CLASSES = {
  sm: 'w-8 h-8 text-xs font-semibold',
  md: 'w-10 h-10 text-sm font-bold',
  lg: 'w-12 h-12 text-base font-bold',
}

export function CompanyInitial({ name, size = 'md', className }: CompanyInitialProps) {
  const initial = (name?.trim()?.[0] ?? '?').toUpperCase()
  const colorClass = COLOR_MAP[initial] ?? DEFAULT_COLOR
  const sizeClass = SIZE_CLASSES[size]

  return (
    <div
      className={cn(
        'inline-flex items-center justify-center rounded-lg shrink-0 select-none',
        colorClass,
        sizeClass,
        className
      )}
      aria-label={`${name} logo`}
    >
      {initial}
    </div>
  )
}

export default CompanyInitial
