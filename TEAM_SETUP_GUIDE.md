# Preply x Agora Hackathon - End-to-End Team Setup Guide

This guide captures the full machine setup we completed for a video AI agent with avatar, voice, LLM, and optional Thymia biomarker integration.

It is written so humans and coding agents (Codex, Claude Code, etc.) can follow it reliably.

## 1) What We Set Up

We prepared a working local stack with these components:

- `agent-samples` (main app stack: backend + React video avatar client)
- `server-custom-llm` (custom LLM proxy required for Thymia workflow)
- `preply-thymia-hackathon` (Thymia examples and docs)
- `hackathon-2026-03-20` (hackathon docs and guide)
- `skills` (Agora skill knowledge base for coding assistants)

Core flow:

1. React video client runs on `http://localhost:8084`
2. Python backend runs on `http://localhost:8082`
3. Backend starts Agora agent instances (`profile=VIDEO` or `profile=THYMIA`)
4. Optional custom LLM server runs on `http://localhost:8100`
5. Optional Thymia module streams biomarker analysis

## 2) Repositories Cloned

From `/Users/kmwg649/Desktop/repos`:

- `https://github.com/AgoraIO-Conversational-AI/agent-samples`
- `https://github.com/AgoraIO-Conversational-AI/server-custom-llm`
- `https://github.com/Hackathon-Preply/hackathon-2026-03-20`
- `https://github.com/thymia-ai/preply-thymia-hackathon`
- `https://github.com/agoraio/skills`

## 3) Local Tooling Installed / Verified

- Node.js: `v25.8.1` (works for these repos; recommended in docs is Node 20/22 depending on component)
- npm: `11.11.0`
- Python: `3.9.6`
- Homebrew installed
- Go installed via Homebrew: `go 1.26.1`

## 4) One-Time Install Steps Completed

### 4.1 `agent-samples/simple-backend`

```bash
cd /Users/kmwg649/Desktop/repos/agent-samples/simple-backend
python3 -m venv venv
./venv/bin/pip install -r requirements-local.txt
```

### 4.2 `agent-samples/react-video-client-avatar`

```bash
cd /Users/kmwg649/Desktop/repos/agent-samples/react-video-client-avatar
npm install --legacy-peer-deps
```

### 4.3 `server-custom-llm/node`

```bash
cd /Users/kmwg649/Desktop/repos/server-custom-llm/node
npm install --legacy-peer-deps
```

### 4.4 `server-custom-llm/go-audio-subscriber`

```bash
cd /Users/kmwg649/Desktop/repos/server-custom-llm/go-audio-subscriber/sdk
bash scripts/install_agora_sdk.sh

cd /Users/kmwg649/Desktop/repos/server-custom-llm/go-audio-subscriber
make build
```

Binary created:

- `/Users/kmwg649/Desktop/repos/server-custom-llm/go-audio-subscriber/bin/audio_subscriber`

## 5) Coding Assistant Skill Setup

Agora skill was linked into Codex skills:

- Source: `/Users/kmwg649/Desktop/repos/skills/skills/agora`
- Linked to: `/Users/kmwg649/.codex/skills/agora`

Command used:

```bash
ln -sfn /Users/kmwg649/Desktop/repos/skills/skills/agora /Users/kmwg649/.codex/skills/agora
```

Important: restart Codex/agent session after installing skills so it loads the new skill.

## 6) Configuration Files

## 6.1 Backend config

File:

- `/Users/kmwg649/Desktop/repos/agent-samples/simple-backend/.env`

This file now includes two profiles:

- `VIDEO_*` for avatar video client mode
- `THYMIA_*` for custom LLM + biomarker mode

### Required secret mapping (use your own team secrets)

Do not commit these to git. Share through your team secret manager.

- Agora:
  - `VIDEO_APP_ID`, `VIDEO_APP_CERTIFICATE`
  - `THYMIA_APP_ID`, `THYMIA_APP_CERTIFICATE`
- LLM:
  - `VIDEO_LLM_API_KEY`
  - `THYMIA_LLM_API_KEY`
- TTS (ElevenLabs in this setup):
  - `VIDEO_TTS_VENDOR=elevenlabs`
  - `VIDEO_TTS_KEY`, `VIDEO_TTS_VOICE_ID`
  - `THYMIA_TTS_VENDOR=elevenlabs`
  - `THYMIA_TTS_KEY`, `THYMIA_TTS_VOICE_ID`
- Avatar (Anam in this setup):
  - `VIDEO_AVATAR_VENDOR=anam`
  - `VIDEO_AVATAR_API_KEY`, `VIDEO_AVATAR_ID`
  - `THYMIA_AVATAR_VENDOR=anam`
  - `THYMIA_AVATAR_API_KEY`, `THYMIA_AVATAR_ID`
- Thymia:
  - `THYMIA_THYMIA_API_KEY`

### Important THYMIA custom-LLM setting

For local testing:

```bash
THYMIA_LLM_URL=http://localhost:8100/chat/completions
```

For actual cloud-reachable agent traffic, this URL must be public (for example Cloudflare tunnel URL).

## 6.2 React client feature flags

File created:

- `/Users/kmwg649/Desktop/repos/agent-samples/react-video-client-avatar/.env.local`

Contents:

```bash
NEXT_PUBLIC_ENABLE_THYMIA=true
NEXT_PUBLIC_ENABLE_SHEN=false
```

## 7) Run Commands (End-to-End)

Open 3 terminals.

### Terminal A - Backend

```bash
cd /Users/kmwg649/Desktop/repos/agent-samples/simple-backend
PORT=8082 ./venv/bin/python -u local_server.py
```

### Terminal B - Video Client

```bash
cd /Users/kmwg649/Desktop/repos/agent-samples/react-video-client-avatar
npm run dev
```

### Terminal C - Custom LLM (for THYMIA profile)

```bash
cd /Users/kmwg649/Desktop/repos/server-custom-llm/node
PORT=8100 THYMIA_ENABLED=true node custom_llm.js
```

## 8) Validation Commands

### Health checks

```bash
curl -s http://127.0.0.1:8082/health
curl -s -i http://127.0.0.1:8100/ping
curl -I -s http://127.0.0.1:8084
```

### Start agent (VIDEO)

```bash
curl -s -i "http://127.0.0.1:8082/start-agent?channel=video_ready_check_01&profile=VIDEO"
```

Expected: HTTP 200 and `agent_response.success=true`.

### Start agent (THYMIA)

```bash
curl -s -i "http://127.0.0.1:8082/start-agent?channel=thymia_ready_check_01&profile=THYMIA"
```

Expected: HTTP 200 and `agent_response.success=true`.

## 9) Known Issues and Meaning

- `TaskConflict` in response body:
  - Agent already running for that channel.
  - Fix: use a new channel name or hang up existing agent.

- `TTS_VENDOR must be set`:
  - Missing `*_TTS_VENDOR` for that profile.

- `AVATAR_API_KEY is required when AVATAR_VENDOR=...`:
  - Missing profile-prefixed avatar key for that profile.

- Thymia data not appearing:
  - Confirm `THYMIA_ENABLED=true` on custom-LLM process.
  - Confirm `THYMIA_THYMIA_API_KEY` is set.
  - Confirm `audio_subscriber` binary exists.

- Custom LLM unreachable from Agora cloud:
  - `THYMIA_LLM_URL` must be public for real cloud calls.
  - Use Cloudflare tunnel in local development.

## 10) Agent Studio vs Local Stack (Quick Clarification)

- Agent Studio "Deploy Agent":
  - Publishes a managed agent configuration in Agora cloud.
- Local `agent-samples` backend:
  - Starts agents via REST API at runtime using your `.env` profile values.

Both are valid. For this project, we are using the local backend profiles (`VIDEO`, `THYMIA`) as the source of truth.

## 11) Security Rules for Team

- Never commit `.env` or `.env.local` with real keys.
- Rotate any key that has been shared in chat or screenshots.
- Use a team secret manager for key exchange.
- Prefer per-person API keys for traceability and revocation.

## 12) Suggested Prompt for Any Coding Agent

```text
Clone these repos into /Users/<you>/Desktop/repos:
- AgoraIO-Conversational-AI/agent-samples
- AgoraIO-Conversational-AI/server-custom-llm
- thymia-ai/preply-thymia-hackathon
- Hackathon-Preply/hackathon-2026-03-20
- agoraio/skills

Read AGENT.md in agent-samples first.
Set up a VIDEO profile and THYMIA profile in simple-backend/.env using profile-prefixed keys.
Install dependencies for simple-backend, react-video-client-avatar, and server-custom-llm/node.
Install Agora SDK libs and build go-audio-subscriber.
Start backend on :8082, client on :8084, custom LLM on :8100.
Run curl health checks and start-agent checks for both VIDEO and THYMIA profiles.
Report any missing credentials or runtime blockers.
```

