// File: src/components/ui/badge.tsx
import { cn } from "@/lib/utils"

export function Badge({ children, className }: { children: React.ReactNode, className?: string }) {
  return (
    <span className={cn("inline-block px-2 py-1 text-xs font-semibold rounded bg-gray-200 text-gray-800", className)}>
      {children}
    </span>
  )
}
