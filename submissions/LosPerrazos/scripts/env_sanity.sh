#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/.env" >&2
  exit 1
fi

ENV_FILE="$1"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing env file: $ENV_FILE" >&2
  exit 1
fi

required_keys=(
  APP_ID
  APP_CERTIFICATE
  LLM_API_KEY
  LLM_MODEL
  TTS_VENDOR
  TTS_KEY
  TTS_VOICE_ID
  AVATAR_VENDOR
  AVATAR_API_KEY
  AVATAR_ID
)

missing=0
for key in "${required_keys[@]}"; do
  if ! grep -E "^${key}=" "$ENV_FILE" >/dev/null; then
    echo "Missing: $key"
    ((missing++))
  fi
done

if [[ $missing -eq 0 ]]; then
  echo "Env looks complete."
else
  echo "Env missing $missing keys."
  exit 1
fi
