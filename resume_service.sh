#!/bin/bash
# resume_service.sh
#

echo "wake up frontend..."
curl -X POST "https://api.render.com/v1/services/${FRONTEND_SERVICE_ID}/resume" \
     -H "Authorization: Bearer ${RENDER_API_KEY}"

echo "wake up backend..."
curl -X POST "https://api.render.com/v1/services/${BACKEND_SERVICE_ID}/resume" \
     -H "Authorization: Bearer ${RENDER_API_KEY}"
