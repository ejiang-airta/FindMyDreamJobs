// ✅ File: frontend/src/app/stats/page.tsx
// This page displays application stats for a user, 
// It fetches data from the backend and displays it in a bar chart using recharts
'use client'

import React, { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useSession } from 'next-auth/react'
import { getUserId } from '@/lib/auth'
import { BACKEND_BASE_URL }  from '@/lib/env'

// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <p>Loading...</p>
  if (!session) return <p>Unauthorized. Please sign in.</p>

  return <StatsPage />
}

// This component is the main page for displaying application stats.
// It fetches the application data from the backend and displays it in a bar chart:
function StatsPage() {
  const [data, setData] = useState<{ status: string; count: number }[]>([])
  const [error, setError] = useState('')
  // define the color scheme for the bar chart:
  const STATUS_COLORS: Record<string, string> = {
    'In Progress': '#8884d8',
    'Offered': '#82ca9d',
    'Rejected': '#f87171',
    'Default': '#a0aec0'
  }

  // This type defines the structure of the application data:
  // you can add more fields here if needed
  type Application = {
    application_status: string
    // you can add more fields here if needed
  }
  // This function retrieves the user ID from local storage:
  const userId = getUserId()
  if (!userId) {
    console.warn("❌ No valid user ID found.")
    setError("⚠️ You're not logged in. Please sign in.")
  return
  }
    console.log("🧠 Using global user ID:", userId)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const res = await fetch(`${BACKEND_BASE_URL}/applications/${userId}`)
      const apps = await res.json()

      if (!res.ok) {
        throw new Error(apps.detail || 'Failed to fetch application stats')
      }

      // Group and count by application_status
      const counts = (apps as Application[]).reduce<Record<string, number>>((acc, app) => {
        acc[app.application_status] = (acc[app.application_status] || 0) + 1
        return acc
      }, {})
      

      const chartData = Object.entries(counts).map(([status, count]) => ({
        status,
        count,
      }))

      setData(chartData)
    } catch (err) {
      console.error(err)
      setError('❌ Could not load stats')
    }
  }

  return (
    <div className="max-w-4xl mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-4">📊 Application Stats</h1>
      <p className="text-sm text-muted-foreground mb-6">
        Here’s a breakdown of your job application statuses so far.
      </p>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardContent className="p-6">
          {data.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="status" />
                <YAxis allowDecimals={false} label={{ value: 'Applications', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Bar dataKey="count">
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={STATUS_COLORS[entry.status] || STATUS_COLORS.Default} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-muted-foreground text-sm">No application data available.</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
