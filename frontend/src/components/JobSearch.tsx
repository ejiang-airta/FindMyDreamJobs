// File: frontend/src/components/JobSearch.tsx

import { useState } from 'react'
import axios from 'axios'

export default function JobSearch({ onSelect }: { onSelect: (job: any) => void }) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const searchJobs = async () => {
    setLoading(true)
    const res = await axios.get(`/api/search-jobs?query=${encodeURIComponent(query)}`)
    setResults(res.data.results || [])
    setLoading(false)
  }

  return (
    <div className="space-y-4">
      <input
        type="text"
        placeholder="Search job titles..."
        className="w-full border p-2 rounded"
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={searchJobs}>
        {loading ? 'Searching...' : 'Search'}
      </button>
      <ul className="divide-y border rounded">
        {results.map((job, idx) => (
          <li key={idx} className="p-2 hover:bg-gray-50 cursor-pointer" onClick={() => onSelect(job)}>
            <div className="font-bold">{job.job_title}</div>
            <div className="text-sm text-gray-600">{job.employer_name} — {job.job_location}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}