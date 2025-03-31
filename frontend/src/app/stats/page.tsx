// ✅ File: frontend/src/app/stats/page.tsx
// This page displays application stats for a user, 
// It fetches data from the backend and displays it in a bar chart using recharts
'use client'

import React, { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'

export default function StatsPage() {
  const [data, setData] = useState<{ status: string; count: number }[]>([])
  const [error, setError] = useState('')
  const userId = 1 // 🔐 Hardcoded for now

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/applications/${userId}`)
      const apps = await res.json()

      if (!res.ok) {
        throw new Error(apps.detail || 'Failed to fetch application stats')
      }

      // Group and count by application_status
      const counts = apps.reduce((acc: any, app: any) => {
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
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="count">
                    {data.map((entry, index) => (
                        <Cell
                        key={`cell-${index}`}
                        fill={
                            entry.status === 'In Progress' ? '#8884d8' :
                            entry.status === 'Offered' ? '#82ca9d' :
                            entry.status === 'Rejected' ? '#f87171' : 
                            '#a0aec0'  // default gray
                        }
                        />
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
