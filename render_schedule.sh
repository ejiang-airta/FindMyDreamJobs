#!/bin/bash

# Required ENV variables
API_KEY="${RENDER_API_KEY}"
SERVICE_ID="${FRONTEND_SERVICE_ID}"
ACTION="$1"  # 'resume' or 'suspend'

# API endpoint
URL="https://api.render.com/v1/services/${SERVICE_ID}/${ACTION}"

# Check for valid input
if [[ "$ACTION" != "resume" && "$ACTION" != "suspend" ]]; then
  echo "Usage: $0 [resume|suspend]"
  exit 1
fi

# Perform action
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$URL" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $API_KEY")

if [[ "$response" == "200" ]]; then
  echo "Successfully triggered $ACTION for service $SERVICE_ID"
else
  echo "Failed to $ACTION service. HTTP $response"
fi