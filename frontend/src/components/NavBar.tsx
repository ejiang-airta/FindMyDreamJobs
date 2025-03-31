// ✅ File: frontend/src/components/NavBar.tsx
// Nevigation bar to let user navigate around the pages:

'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'

const navItems = [
  { href: '/dashboard', label: '📊 Dashboard' },
  { href: '/upload', label: '📤 Upload' },
  { href: '/analyze', label: '📑 Analyze' },
  { href: '/match', label: '🔍 Match' },
  { href: '/optimize', label: '🛠 Optimize' },
  { href: '/finalize', label: '✅ Finalize' },
  { href: '/apply', label: '📩 Apply' },
  { href: '/applications', label: '🧾 Applications' },
  { href: '/jobs', label: '📋 Jobs' },
  { href: '/matches', label: '🧠 Matches' },
  { href: '/stats', label: '📈 Stats' },
]

export default function NavBar() {
  const pathname = usePathname()

  return (
    <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex space-x-4 overflow-x-auto">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              'px-3 py-2 rounded text-sm whitespace-nowrap font-medium hover:bg-gray-100 transition',
              pathname === item.href ? 'bg-gray-200 text-black font-semibold' : 'text-gray-600'
            )}
          >
            {item.label}
          </Link>
        ))}
      </div>
    </nav>
  )
}

