// File: frontend/src/app/about/page.tsx
import React from 'react'

export default function AboutPage() {
  return (
    <section className="bg-gray-50 py-16 px-6 text-center">
      <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
        Our Mission
      </h1>
      <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-12">
        We're on a mission to revolutionize the job search process by leveraging artificial
        intelligence to match candidates with their dream jobs. Our platform helps job seekers
        find opportunities that truly align with their skills, experience, and career goals.
      </p>

      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-8">Our Values</h2>
      <div className="grid gap-6 md:grid-cols-3 max-w-5xl mx-auto">
        <div className="bg-white shadow-md rounded-xl p-6 text-left">
          <h3 className="text-xl font-semibold mb-2">Innovation</h3>
          <p className="text-gray-600 text-sm">
            We constantly push the boundaries of what's possible with AI and technology
            to improve the job search experience.
          </p>
        </div>
        <div className="bg-white shadow-md rounded-xl p-6 text-left">
          <h3 className="text-xl font-semibold mb-2">Transparency</h3>
          <p className="text-gray-600 text-sm">
            We believe in being open and honest about how our matching algorithms work
            and how we use your data.
          </p>
        </div>
        <div className="bg-white shadow-md rounded-xl p-6 text-left">
          <h3 className="text-xl font-semibold mb-2">User-First</h3>
          <p className="text-gray-600 text-sm">
            Everything we do is designed with our users' needs and success in mind.
          </p>
        </div>
      </div>
    </section>
  )
}
