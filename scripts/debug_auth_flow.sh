#!/bin/bash

# Title: Simulate Tier Access Test (macOS Safari only)
# Author: Cevher Dogan & GPT CoPilot
# Usage: ./scripts/debug_auth_flow.sh [tier]

TIER="${1:-free}"

echo "⏳ Setting localStorage tier to '$TIER' in Safari..."

osascript <<EOF
tell application "Safari"
    activate
    tell front document
        do JavaScript "localStorage.setItem('tier', '$TIER'); location.reload();" in current tab
    end tell
end tell
EOF

echo "✅ Tier set to '$TIER'. Safari should reload with new tier."

