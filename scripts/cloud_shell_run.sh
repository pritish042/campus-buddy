#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# Campus Buddy - Google Cloud Shell Server Runner
# Runs the ADK Web Dev UI on 0.0.0.0:8080 with Cloud Shell CORS origin allowed.
# ==============================================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

# Activate virtual environment if present
if [ -d ".venv" ]; then
    # shellcheck source=/dev/null
    source .venv/bin/activate
fi

# Validate dependencies
if ! command -v adk &>/dev/null; then
    echo "❌ Error: 'adk' command not found. Please run ./scripts/cloud_shell_setup.sh first."
    exit 1
fi

# Check .env
if [ ! -f ".env" ]; then
    echo "⚠️ Warning: .env not found. Please run ./scripts/cloud_shell_setup.sh or create .env from .env.example"
fi

HOST="0.0.0.0"
PORT="8080"
ALLOWED_ORIGINS="regex:https://.*\.cloudshell\.dev"

echo "===================================================================="
echo "🚀 Starting Campus Buddy ADK Server on ${HOST}:${PORT}"
echo "🌐 Allowed Origins: ${ALLOWED_ORIGINS}"
echo "===================================================================="
echo "👉 In Google Cloud Shell, click 'Web Preview' (top right icon)"
echo "   and select 'Preview on port 8080'."
echo ""
echo "👉 Inside the ADK Dev UI, select 'campus_buddy' in the app dropdown."
echo "   Press Ctrl+C to stop the server."
echo "===================================================================="
echo ""

# Launch ADK Web Dev UI with CORS support for Cloud Shell Web Preview
exec adk web \
  --host "${HOST}" \
  --port "${PORT}" \
  --allow_origins "${ALLOWED_ORIGINS}" \
  .
