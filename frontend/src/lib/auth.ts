// ✅ File: frontend/src/lib/auth.ts
// This file contains utility to get the user ID from local storage and check if the user is authenticated.

// Safely get user_id from localStorage
export function getUserId(): number | null {
    const value = localStorage.getItem("user_id")
    const parsed = parseInt(value || '', 10)
    return isNaN(parsed) ? null : parsed
  }
  
// 🔐 Check if user is authenticated (based on localStorage)
export function isAuthenticated(): boolean {
    return getUserId() !== null
  }