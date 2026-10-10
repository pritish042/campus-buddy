#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# Campus Buddy - Google Cloud Shell Setup Script
# Safe to rerun idempotently.
# ==============================================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "📦 === Setting up Campus Buddy Environment in Cloud Shell ==="

# 1. Ensure Python 3.10+ is available
if ! command -v python3 &>/dev/null; then
    echo "❌ Error: python3 is not installed or not in PATH."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python version detected: ${PYTHON_VERSION}"

# 2. Create or reuse virtual environment
if [ ! -d ".venv" ]; then
    echo "🔨 Creating virtual environment in .venv..."
    python3 -m venv .venv
else
    echo "✅ Existing .venv virtual environment detected."
fi

# 3. Activate virtual environment
# shellcheck source=/dev/null
source .venv/bin/activate

# 4. Install / Update dependencies
echo "📥 Installing required dependencies (ADK, LiteLLM, Pytest)..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# 5. Disable ADK telemetry non-interactively
if command -v adk &>/dev/null; then
    adk telemetry disable &>/dev/null || true
fi

# 6. Check / Configure .env securely
if [ ! -f ".env" ] || ! grep -q "GROQ_API_KEY=gsk_" .env 2>/dev/null; then
    echo ""
    echo "🔑 === Groq API Key Configuration ==="
    echo "Campus Buddy uses Groq for ultra-fast agent inference."
    echo "Get a free API key at: https://console.groq.com/keys"
    echo ""
    read -r -s -p "Paste your Groq API key (starts with gsk_): " INPUT_KEY
    echo ""
    
    if [ -n "${INPUT_KEY}" ]; then
        cat <<EOF > .env
GROQ_API_KEY=${INPUT_KEY}
ADK_MODEL=groq/qwen/qwen3.8-27b
EOF
        chmod 600 .env
        echo "✅ .env created securely with permissions 600 (read/write owner only)."
    else
        echo "⚠️ No key provided. Created .env from .env.example (please edit .env before chatting)."
        cp .env.example .env
        chmod 600 .env
    fi
else
    echo "✅ .env is already configured with a Groq API key."
fi

echo ""
echo "✨ === Cloud Shell Setup Complete! ==="
echo "To start the development server, run:"
echo "   ./scripts/cloud_shell_run.sh"
echo "Then click 'Web Preview' -> 'Preview on port 8080' in Cloud Shell."
