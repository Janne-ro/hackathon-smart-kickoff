# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Hackathon workspace for the Preply x Agora Hackathon (March 20-21, 2026). The repo contains hackathon docs, our team submission, and cloned tool repos under `vendor/` (gitignored). The theme is **AI Agents for NextGen Language Learning** using Agora ConvoAI, OpenAI, Anam avatars, and Thymia voice biomarkers.

## Dependency Management

Use `uv` for all Python dependency management. When setting up a new Python environment:

```bash
uv venv
uv pip install -r requirements.txt
```

For Node.js projects, use `npm install --legacy-peer-deps` (required by agent-samples deps).

## Repository Layout

```
hackathon-smart-kickoff/
├── .env                     # All API keys (symlinked into vendor/agent-samples/simple-backend/.env)
├── submissions/             # Our hackathon code goes here
├── vendor/                  # Gitignored — cloned tool repos (do not commit)
│   ├── agent-samples/       # Agora backend + React frontends
│   ├── server-custom-llm/   # Custom LLM proxy (Thymia, RAG, tools)
│   ├── preply-thymia-hackathon/  # Thymia examples/docs
│   └── skills/              # Agora skill knowledge base
```

## Running the Stack

Three services need to run simultaneously. Each in its own terminal.

### Terminal A — Python Backend (port 8082)

```bash
cd vendor/agent-samples/simple-backend
PORT=8082 ./venv/bin/python -u local_server.py
```

The `-u` flag is critical — without it Python buffers stdout and logs don't appear.

### Terminal B — React Video Client (port 8084)

```bash
cd vendor/agent-samples/react-video-client-avatar
npm run dev
```

Opens at http://localhost:8084. Sends `?profile=VIDEO` by default. Override via the "Server Profile" field in the UI.

### Terminal C — Custom LLM Server (port 8100, only for THYMIA profile)

```bash
cd vendor/server-custom-llm/node
PORT=8100 THYMIA_ENABLED=true node custom_llm.js
```

### Health Checks

```bash
curl -s http://127.0.0.1:8082/health
curl -s -i http://127.0.0.1:8100/ping
curl -I -s http://127.0.0.1:8084
```

### Start an Agent

```bash
# VIDEO profile (avatar)
curl -s -i "http://127.0.0.1:8082/start-agent?channel=test01&profile=VIDEO"

# THYMIA profile (biomarkers, requires Terminal C running)
curl -s -i "http://127.0.0.1:8082/start-agent?channel=test02&profile=THYMIA"
```

Expected: HTTP 200, `agent_response.success=true`. A `TaskConflict` means an agent is already running on that channel — use a different channel name.

## Configuration System

The backend uses **profile-prefixed environment variables**. All keys in `.env` follow `{PROFILE}_{VARIABLE}` format:

- `VIDEO_*` — Avatar video client mode (Anam avatar + ElevenLabs TTS + OpenAI LLM)
- `THYMIA_*` — Custom LLM + Thymia biomarker mode

When the client sends `?profile=VIDEO`, the backend loads all `VIDEO_*` vars. Profile names are case-insensitive.

The `.env` at repo root is symlinked to `vendor/agent-samples/simple-backend/.env`. Edit it in the root — changes propagate automatically.

The React client's `.env.local` is at `vendor/agent-samples/react-video-client-avatar/.env.local` with feature flags (`NEXT_PUBLIC_ENABLE_THYMIA`, `NEXT_PUBLIC_ENABLE_SHEN`).

## Architecture

```
Browser (React, port 8084)
    ↕ audio/video via Agora SD-RTN
AI Agent Instance (Agora cloud, managed)
    ↕ STT → LLM → TTS pipeline
Python Backend (port 8082)
    → Agora REST API to start/stop agents
    → Token generation from APP_CERTIFICATE
Custom LLM Server (port 8100, optional)
    → Intercepts LLM calls for Thymia biomarkers, RAG, tool calling
    → Go audio subscriber captures RTC audio for Thymia analysis
```

## Key Files to Read

- `vendor/agent-samples/AGENT.md` — Complete backend config guide, profile system, MLLM modes
- `vendor/agent-samples/simple-backend/core/agent.py` — How agent payloads are built
- `vendor/agent-samples/simple-backend/core/config.py` — Profile-based config loading
- `vendor/server-custom-llm/node/custom_llm.js` — Custom LLM server with Thymia/tool integration
- `vendor/agent-samples/react-video-client-avatar/components/VideoAvatarClient.tsx` — Main frontend component

## Go Audio Subscriber

Pre-built binary at `vendor/server-custom-llm/go-audio-subscriber/bin/audio_subscriber`. To rebuild:

```bash
cd vendor/server-custom-llm/go-audio-subscriber
make build
```

Requires `DYLD_LIBRARY_PATH` pointing to the Agora SDK dylibs when running on macOS.

## Submission Structure

Our team code goes in `submissions/<team-name>/`:

```
submissions/<team-name>/
├── README.md           # Project description (required)
├── HOW_WE_BUILT.md     # AI development process (recommended)
├── demo.mp4            # Demo video (required)
├── src/                # Source code
└── docs/               # Documentation/screenshots
```
