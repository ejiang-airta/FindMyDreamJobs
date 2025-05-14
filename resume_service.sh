#!/bin/bash
# resume_service.sh

# Required ENV variables
API_KEY="${RENDER_API_KEY}"
SERVICE_ID="${FRONTEND_SERVICE_ID}"

# API endpoint
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  https://api.render.com/v1/services/$SERVICE_ID/resume
