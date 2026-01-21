// ✅ File: frontend/tests/ui/test-config.ts
// Centralized test configuration - ALL URL logic lives here

// Environment detection
export const TEST_ENV = process.env.PLAYWRIGHT_BASE_URL 
  ? 'preview' 
  : (process.env.ENV || 'prod');

// Frontend URL
export const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || (
  process.env.ENV === 'dev' 
    ? 'http://localhost:3000' 
    : 'https://findmydreamjobs.com'
);

// Backend URL
export const BACKEND_URL = process.env.PLAYWRIGHT_BACKEND_URL || (
  process.env.ENV === 'dev' 
    ? 'http://localhost:8000' 
    : 'https://findmydreamjobs.onrender.com/'
);

// Warmup settings
export const TIMEOUT_MS = Number(process.env.WARMUP_TIMEOUT_MS || 420000);
export const INTERVAL_MS = Number(process.env.WARMUP_INTERVAL_MS || 10000);

// Log configuration on import
console.log("Test Environment:", TEST_ENV);
console.log("Frontend URL:", BASE_URL);
console.log("Backend URL:", BACKEND_URL);