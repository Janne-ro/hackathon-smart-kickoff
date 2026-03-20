#!/bin/bash
# Smart Onboard — Setup Script
# Clones vendor repos, applies patches, symlinks our code, installs deps.
set -e

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENDOR="$REPO_ROOT/vendor"
SUBMISSION="$REPO_ROOT/submissions/LosPerrazos"

echo "=== Smart Onboard Setup ==="
echo "Repo root: $REPO_ROOT"

# 1. Clone vendor repos if missing
mkdir -p "$VENDOR"

if [ ! -d "$VENDOR/agent-samples" ]; then
  echo "Cloning agent-samples..."
  git clone https://github.com/AgoraIO-Conversational-AI/agent-samples.git "$VENDOR/agent-samples"
fi

if [ ! -d "$VENDOR/server-custom-llm" ]; then
  echo "Cloning server-custom-llm..."
  git clone https://github.com/AgoraIO-Conversational-AI/server-custom-llm.git "$VENDOR/server-custom-llm"
fi

# 2. Apply patches
echo "Applying custom-llm patch..."
cd "$VENDOR/server-custom-llm"
git checkout -- . 2>/dev/null || true
git apply "$SUBMISSION/patches/custom-llm.patch"

echo "Applying video-client patch..."
cd "$VENDOR/agent-samples"
git checkout -- . 2>/dev/null || true
git apply "$SUBMISSION/patches/video-client.patch"

# 3. Copy session_report.js into custom LLM server (symlinks break Node require resolution)
cp "$SUBMISSION/src/session-collector/session_report.js" "$VENDOR/server-custom-llm/node/session_report.js"

# 4. Symlink .env into backend
ln -sfn "$REPO_ROOT/.env" "$VENDOR/agent-samples/simple-backend/.env"

# 5. Install dependencies
echo "Installing backend dependencies..."
cd "$VENDOR/agent-samples/simple-backend"
python3 -m venv venv 2>/dev/null || true
./venv/bin/pip install -r requirements-local.txt -q

echo "Installing React client dependencies..."
cd "$VENDOR/agent-samples/react-video-client-avatar"
npm install --legacy-peer-deps --silent

echo "Installing custom LLM server dependencies..."
cd "$VENDOR/server-custom-llm/node"
npm install --legacy-peer-deps --silent

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To run, open 4 terminals:"
echo ""
echo "Terminal A (Backend):"
echo "  cd $VENDOR/agent-samples/simple-backend"
echo "  SSL_CERT_FILE=\$(./venv/bin/python -c 'import certifi; print(certifi.where())') PORT=8082 ./venv/bin/python -u local_server.py"
echo ""
echo "Terminal B (Frontend):"
echo "  cd $VENDOR/agent-samples/react-video-client-avatar"
echo "  npm run dev"
echo ""
echo "Terminal C (Custom LLM):"
echo "  cd $VENDOR/server-custom-llm/node"
echo "  PORT=8100 THYMIA_ENABLED=true node custom_llm.js"
echo ""
echo "Terminal D (Tunnel):"
echo "  cloudflared tunnel --url http://localhost:8100"
echo "  # Then set THYMIA_LLM_URL in .env to the tunnel URL + /chat/completions"
