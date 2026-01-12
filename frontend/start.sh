#!/bin/bash
# Start script for frontend service in App Platform

# Replace BACKEND_URL placeholder with actual backend URL
if [ -n "$BACKEND_URL" ]; then
    echo "✓ Configuring backend URL: $BACKEND_URL"
    sed -i "s|BACKEND_URL_PLACEHOLDER|$BACKEND_URL|g" /workspace/index.html
    sed -i "s|BACKEND_URL_PLACEHOLDER|$BACKEND_URL|g" /workspace/game.html
else
    echo "⚠️  Warning: BACKEND_URL not set, using relative URLs"
    sed -i "s|BACKEND_URL_PLACEHOLDER||g" /workspace/index.html
    sed -i "s|BACKEND_URL_PLACEHOLDER||g" /workspace/game.html
fi

# Start simple HTTP server
echo "✓ Starting frontend server on port 8080"
python3 -m http.server 8080
