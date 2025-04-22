// ✅ File: frontend/src/components/ui/AppButton.tsx
// AppButton is a wrapper around the Button component to create centralized look n feel cross all pages.

'use client'

import { Button } from './button'
import { cn } from '@/lib/utils'  // your className merge util if available
import type { ComponentProps } from 'react'

/** Available variants for AppButton styling */
type Variant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline'

/**
 * Props for AppButton
 * Omits the underlying Button's variant prop to define custom variants
 */
type AppButtonProps = Omit<ComponentProps<typeof Button>, 'variant'> & {
  /** Button variant to control look & feel across the app */
  variant?: Variant
}

export function AppButton({ variant = 'primary', className, ...props }: AppButtonProps) {
  const variantStyles: Record<Variant, string> = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-100 text-gray-800 hover:bg-gray-200',
    ghost: 'bg-transparent border border-gray-300 text-gray-700 hover:bg-gray-100',
    danger: 'bg-red-600 text-white hover:bg-red-700',
    outline: 'border border-gray-400 text-gray-800 hover:bg-gray-50',
  }

  return (
    <Button
      className={cn(
        'rounded-md px-4 py-2 text-sm font-semibold',
        variantStyles[variant as Variant],  // ✅ Ensures no type error
        className
      )}
      {...props}
    />
  )
}
