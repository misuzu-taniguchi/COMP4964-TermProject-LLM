#!/usr/bin/env bash
# Test that the hosted model is reachable and responds correctly.

ENDPOINT=${1:-"http://127.0.0.1:11434"}
DATA='{"model":"qwen2.5:3b-instruct","prompt":"Say hi"}'

echo "Sending test request to $ENDPOINT..."
curl -s -X POST "$ENDPOINT/api/generate" \
     -H "Content-Type: application/json" \
     -d "$DATA" | head -n 10
