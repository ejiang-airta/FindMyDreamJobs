// File: src/components/ui/skeleton.tsx
export function Skeleton({ className }: { className?: string }) {
    return (
      <div className={`animate-pulse bg-gray-300 rounded ${className || 'h-4 w-full'}`} />
    )
  }
  