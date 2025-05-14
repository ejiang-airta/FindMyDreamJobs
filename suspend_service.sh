#!/bin/bash
# suspend_service.sh

# Required ENV variables
API_KEY="${RENDER_API_KEY}"
SERVICE_ID="${FRONTEND_SERVICE_ID}"

# API endpoint
response=$(curl -X POST \
  https://api.render.com/v1/services/$SERVICE_ID/suspend) \
  -H "Authorization: Bearer $API_KEY" 
  
# Check for success
if [[ "$response" == "200" ]]; then
  echo "Successfully triggered $ACTION for service $SERVICE_ID"
else
  echo "Failed to $ACTION service. HTTP $response"
fi

