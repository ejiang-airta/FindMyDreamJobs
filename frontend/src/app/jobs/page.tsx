// ✅ File: frontend/src/app/jobs/page.tsx
// This page is for displaying matched jobs:
'use client'

import React, { useEffect, useState } from 'react'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Protected } from '@/components/Protected'
import { useSession } from 'next-auth/react'
import MainLayout from '@/app/MainLayout'



// This ensures page is only accessible to authenticated users:
export default function ProtectedPage() {
  return (
    <Protected>
      <JobSearchPage />
    </Protected>
  )
}
// This component is the main page for displaying matched jobs.
// It fetches the matched jobs from the backend and allows the user to optimize and apply for each job.
function JobSearchPage() {
  const [matches, setMatches] = useState([])
  const [error, setError] = useState('')

  const filters = [
    { label: 'All Jobs', value: 'all' },
    { label: 'Saved Jobs', value: 'saved' },
    { label: 'Applied', value: 'applied' },
    { label: 'Interviews', value: 'interviews' },
  ];

  const jobListings = [
    {
      id: 1,
      title: 'Senior Software Engineer',
      company: 'TechCorp',
      location: 'San Francisco, CA',
      salary: '$120,000 - $150,000',
      matchScore: 95,
      postedDate: '2 days ago',
      description: 'Looking for an experienced software engineer to join our team...',
    },
    {
      id: 2,
      title: 'Product Manager',
      company: 'InnovateCo',
      location: 'Remote',
      salary: '$100,000 - $130,000',
      matchScore: 88,
      postedDate: '1 week ago',
      description: 'Seeking a product manager to lead our development team...',
    },
    // Add more job listings as needed
  ];

  useEffect(() => {
    fetchMatches()
  }, [])

  const fetchMatches = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8001/matches")
      const data = await res.json()

      if (!res.ok) throw new Error(data.detail || 'Failed to fetch matches')
      setMatches(data)
    } catch (err) {
      console.error(err)
      setError('❌ Failed to load job matches.')
    }
  }

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row gap-6">
          {/* Filters Sidebar */}
          <div className="w-full md:w-64 space-y-4">
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="text-lg font-semibold mb-4">Filters</h3>
              <div className="space-y-2">
                {filters.map((filter) => (
                  <button
                    key={filter.value}
                    className="w-full text-left px-3 py-2 rounded-md hover:bg-gray-100 transition-colors"
                  >
                    {filter.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Job Listings */}
          <div className="flex-1 space-y-4">
            {jobListings.map((job) => (
              <div
                key={job.id}
                className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-xl font-semibold">{job.title}</h2>
                    <p className="text-gray-600">{job.company}</p>
                    <p className="text-gray-500">{job.location}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-green-600 font-semibold">
                      {job.matchScore}% Match
                    </div>
                    <div className="text-gray-500 text-sm">{job.postedDate}</div>
                  </div>
                </div>
                <div className="mt-4">
                  <p className="text-gray-700">{job.description}</p>
                </div>
                <div className="mt-4 flex justify-between items-center">
                  <div className="text-gray-600">{job.salary}</div>
                  <div className="space-x-2">
                    <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
                      Apply Now
                    </button>
                    <button className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-100 transition-colors">
                      Save
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  )
}
