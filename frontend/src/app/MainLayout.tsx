'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { useSession, signOut } from 'next-auth/react';
import { Toaster } from 'react-hot-toast';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const pathname = usePathname();
  const { data: session } = useSession();

  const handleSignOut = async () => {
    await signOut({ callbackUrl: 'http://localhost:3001' });
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Left Sidebar */}
      <div className="fixed left-0 h-full w-64 bg-white shadow-md">
        <div className="p-4">
          <span className="text-2xl font-bold text-primary-600">DreamJobs</span>
        </div>
        <nav aria-label="Side Navigation" className="mt-4">
          <Link
            href="/dashboard"
            className={`flex items-center px-4 py-2 text-sm font-medium ${
              pathname === '/dashboard'
                ? 'bg-primary-50 text-primary-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3">📊</span>
            Dashboard
          </Link>
          <Link
            href="/resumes"
            className={`flex items-center px-4 py-2 text-sm font-medium ${
              pathname === '/resumes'
                ? 'bg-primary-50 text-primary-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3">📄</span>
            Resumes
          </Link>
          <Link
            href="/jobs"
            className={`flex items-center px-4 py-2 text-sm font-medium ${
              pathname === '/jobs'
                ? 'bg-primary-50 text-primary-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3">💼</span>
            Jobs
          </Link>
          <Link
            href="/applications"
            className={`flex items-center px-4 py-2 text-sm font-medium ${
              pathname === '/applications'
                ? 'bg-primary-50 text-primary-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3">📝</span>
            Applications
          </Link>
          <Link
            href="/matches"
            className={`flex items-center px-4 py-2 text-sm font-medium ${
              pathname === '/matches'
                ? 'bg-primary-50 text-primary-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3">🎯</span>
            Matches
          </Link>
          <Link
            href="/optimize"
            className={`flex items-center px-4 py-2 text-sm font-medium ${
              pathname === '/optimize'
                ? 'bg-primary-50 text-primary-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3">⚡</span>
            Optimize
          </Link>
          <Link
            href="/finalize"
            className={`flex items-center px-4 py-2 text-sm font-medium ${
              pathname === '/finalize'
                ? 'bg-primary-50 text-primary-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3">✅</span>
            Finalize
          </Link>
          <Link
            href="/apply"
            className={`flex items-center px-4 py-2 text-sm font-medium ${
              pathname === '/apply'
                ? 'bg-primary-50 text-primary-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3">📤</span>
            Apply
          </Link>
          <Link
            href="/stats"
            className={`flex items-center px-4 py-2 text-sm font-medium ${
              pathname === '/stats'
                ? 'bg-primary-50 text-primary-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3">📈</span>
            Stats
          </Link>
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 ml-64">
        {/* Top Navigation */}
        <div className="fixed top-0 right-0 left-64 h-16 bg-white shadow-md z-10">
          <nav aria-label="Top Navigation" className="flex items-center justify-between px-4 py-3">
            <div className="flex items-center space-x-4">
              <Link
                href="/"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">🏠</span>
                Home
              </Link>
              <Link
                href="/upload"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/upload'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">⬆️</span>
                Upload
              </Link>
              <Link
                href="/analyze"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/analyze'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">🔍</span>
                Analyze
              </Link>
              <Link
                href="/match"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/match'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">🎯</span>
                Match
              </Link>
              <Link
                href="/optimize"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/optimize'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">⚡</span>
                Optimize
              </Link>
              <Link
                href="/finalize"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/finalize'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">✅</span>
                Finalize
              </Link>
              <Link
                href="/apply"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/apply'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">📤</span>
                Apply
              </Link>
              <Link
                href="/applications"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/applications'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">📝</span>
                Applications
              </Link>
              <Link
                href="/jobs"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/jobs'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">💼</span>
                Jobs
              </Link>
              <Link
                href="/matches"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/matches'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">🎯</span>
                Matches
              </Link>
              <Link
                href="/stats"
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  pathname === '/stats'
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">📈</span>
                Stats
              </Link>
            </div>
            <div className="flex items-center">
              {session ? (
                <div className="flex items-center space-x-3">
                  <span className="text-sm text-gray-600">
                    {session.user?.name || session.user?.email}
                  </span>
                  <button 
                    onClick={handleSignOut}
                    className="px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-50"
                  >
                    Sign Out
                  </button>
                </div>
              ) : (
                <Link
                  href="/auth/signin"
                  className="px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-50"
                >
                  Sign In
                </Link>
              )}
            </div>
          </nav>
        </div>

        {/* Content */}
        <main className="mt-16 p-6">
          {children}
        </main>
      </div>
      <Toaster position="top-right" />
    </div>
  );
};

export default MainLayout; 