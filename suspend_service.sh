#!/bin/bash
# suspend_service.sh


curl -X POST "https://api.render.com/v1/services/${FRONTEND_SERVICE_ID}/suspend" \
     -H "Authorization: Bearer ${RENDER_API_KEY}"