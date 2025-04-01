// ✅ File: frontend/src/lib/auth.ts
// This file contains utility functions for managing user authentication and session data.
export function getUserId(): number {
    return parseInt(localStorage.getItem("user_id") || "0")
    }