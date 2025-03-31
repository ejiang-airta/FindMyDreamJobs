// Shows a specific resume-to-job match score (usually used during matching a JD and Resume).
// 🟡 Use MatchScore

import MatchScore from '@/components/MatchScore'

export default function MatchPage() {
  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold">🔍 Job Match Score</h1>
      <MatchScore />
    </div>
  )
}
