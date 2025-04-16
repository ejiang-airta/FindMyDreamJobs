// ✅ File; frontend/src/lib/env.ts
// This file contains the environment variables used in the application.
// It dynamically sets the backend and frontend base URLs based on the environment in PROD or Dev.
//

const IS_PROD = process.env.NODE_ENV === 'production'


export const BACKEND_BASE_URL = IS_PROD
  ? 'https://findmydreamjobs-service.onrender.com'
  : 'http://127.0.0.1:8000'

export const FRONTEND_BASE_URL = IS_PROD
  ? 'https://findmydreamjobs-frontend.onrender.com'
  : 'http://127.0.0.1:3000'
