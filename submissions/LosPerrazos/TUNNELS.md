# Tunnel Setup for Remote Demo

Exposes all local services via Cloudflare tunnels so another computer can access the demo.

## Prerequisites

- All 4 terminals running (backend, React client, custom LLM server, static file server)
- `cloudflared` installed (`brew install cloudflare/cloudflare/cloudflared`)

## Step 1: Start tunnels

Run each in a separate terminal (or background them):

```bash
# Port 8000 — Static HTML (entry point for the demo)
cloudflared tunnel --url http://localhost:8000

# Port 8082 — Python backend
cloudflared tunnel --url http://localhost:8082

# Port 8084 — React video client
cloudflared tunnel --url http://localhost:8084

# Port 8100 — Custom LLM server (you likely already have this one running)
cloudflared tunnel --url http://localhost:8100
```

Each command prints a URL like `https://random-words.trycloudflare.com`. Note all four.

## Step 2: Update hardcoded URLs

Replace `localhost` references with the tunnel URLs in these files:

### `submissions/LosPerrazos/src/preply-clone.html`

- `http://localhost:8084/` → tunnel URL for port 8084
- `http://localhost:8100` (2 occurrences) → tunnel URL for port 8100

### `vendor/agent-samples/react-video-client-avatar/components/VideoAvatarClient.tsx`

- `http://localhost:8082` (line 32, DEFAULT_BACKEND_URL) → tunnel URL for port 8082

### `.env`

- `THYMIA_LLM_URL` should already point to the port 8100 tunnel URL + `/chat/completions`

## Step 3: Restart

- **Terminal A** (Python backend) — restart if `.env` changed
- **Terminal B** (React client) — restart to pick up the TSX change (`npm run dev`)
- Terminals C and D don't need restarts (static files + Node reads no changed files)

## Step 4: Share

Send the **port 8000 tunnel URL** + `/preply-clone.html` to the other person:

```
https://<your-8000-tunnel>.trycloudflare.com/preply-clone.html
```

## Reverting to localhost

To go back to local development, undo the URL changes:

- `preply-clone.html`: restore `http://localhost:8084/` and `http://localhost:8100`
- `VideoAvatarClient.tsx`: restore `http://localhost:8082`
