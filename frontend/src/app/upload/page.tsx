//✅ Page for uploading resume

import ResumeUploadForm from "@/components/ResumeUploadForm"

export default function UploadPage() {
  return (
    <div className="max-w-xl mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-4">Upload Your Resume</h1>
      <ResumeUploadForm />
    </div>
  )
}
