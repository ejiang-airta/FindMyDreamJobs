#!/bin/bash
# suspend_service.sh

echo "Suspending frontend..."
curl -X POST "https://api.render.com/v1/services/${FRONTEND_SERVICE_ID}/suspend" \
     -H "Authorization: Bearer ${RENDER_API_KEY}"

echo "Suspending backend..."
curl -X POST "https://api.render.com/v1/services/${BACKEND_SERVICE_ID}/suspend" \
     -H "Authorization: Bearer ${RENDER_API_KEY}"
