# Smart Onboard: End-to-End Delivery Plan (Hackathon, Mar 20-21 2026)

## Goal & Success Criteria
- Live demo: user speaks to avatar → onboarding flow completes → dashboard auto-refreshes with skill assessment, strengths/focus areas, and a retention confidence score.
- Judging alignment: show deep Agora ConvoAI use (+5 bonus) and clear relevance to Preply onboarding; no broken UX.
- Scope discipline: one scripted path (single language pair, single avatar) that is reliable under venue network constraints.

## Repos in this workspace (all under `/Users/kmwg649/Desktop/repos/preply-hackathon`)
- `hackathon-smart-kickoff` (this repo): submission hub, docs, dashboard UI, team assets.
- `agent-samples`: primary backend + React video/voice clients; base for avatar conversation.
- `server-custom-llm`: middleware for custom prompts, Thymia hook, JSON post-processing.
- `preply-thymia-hackathon`: reference Thymia examples/tests.
- `skills`: Codex/skills bundle (agora-intake etc.) — not part of demo but useful for assistants.

## Runtime Profiles & Flags
- `VIDEO`: Avatar conversation only (Anam + ConvoAI).
- `THYMIA`: Voice biomarkers via Thymia; no avatar.
- `VIDEO_THYMIA_SHEN`: Full stack (avatar + Thymia + optional Shen vitals). Feature flag `ENABLE_SHEN` controls Shen; must be safe when false.

## Environment & Secrets (no secrets here; store in env templates)
- Create `submissions/LosPerrazos/env-templates/` with `.env.video`, `.env.thymia`, `.env.video_thymia_shen`.
- Copy/symlink appropriate template to:
  - `agent-samples/.env`
  - `server-custom-llm/.env`
- Required keys per profile: `APP_ID`, `APP_CERTIFICATE`, `LLM_API_KEY/URL/MODEL`, `TTS_VENDOR/KEY/VOICE_ID`, `AVATAR_API_KEY/ID/VENDOR`, `THYMIA_API_KEY`, `ENABLE_SHEN` + `SHEN_API_KEY` (optional). Add a `scripts/env_sanity.sh` to print which keys are loaded (no secrets echoed).

## Architecture (high level)
1) Client (video sample) captures mic/camera, streams via ConvoAI (SD-RTN).
2) Backend (agent-samples or server-custom-llm) generates RTC tokens, starts agent, routes STT → LLM → TTS.
3) Middleware attaches Thymia analysis to audio segments; optionally forwards video frames to Shen.
4) After session ends (or on demand), backend emits a summary JSON matching the dashboard schema.
5) Dashboard fetches the latest JSON and renders learner/tutor views.

## Workstreams & Tasks
1) Conversation design & schema  
   - Finalize scripted flow (native warmup → goals → target-language probe → wrap-up) covering: target language, goals, timeline, inspiration, topic focus, current level, teaching style prefs, tutor country/language prefs, weekly availability, budget/price range, lesson frequency, lesson duration, prior experience, timezone.  
   - Author system/developer prompts and enforce JSON output schema (skills + CEFR badge, strengths, focus areas, motivation quote/tags, retention_confidence for internal use, sentiment, vitals, budget/frequency/duration, tutor_match preview with count + 3 teaser cards). Store in `submissions/LosPerrazos/prompts/`.

2) Backend & middleware  
   - Start from `agent-samples` backend; if custom prompts/tooling needed, route through `server-custom-llm`.  
   - Add post-processing hook to merge transcript + Thymia scores (+ Shen when enabled) → `latest-session.json` in submission folder.  
   - Timeouts + friendly fallback responses to avoid dead air.

3) Thymia integration  
   - Follow `agent-samples/recipes/thymia.md`; call Thymia REST on audio chunks.  
   - Map sentiment/stress to a `retention_confidence` heuristic; include raw scores in JSON.

4) Shen integration (optional but showcased if unblocked)  
   - If `SHEN_API_KEY` reachable, send video frames; parse vitals into JSON.  
   - If not available, keep `ENABLE_SHEN=false`; provide mocked vitals to keep UI stable and clearly label as simulated.

5) Client (avatar) updates  
   - Run Video AI Agent sample; confirm avatar render + bidirectional audio.  
   - Add a small UI control to request/refresh the summary JSON after a session.

6) Dashboard wiring  
   - Replace static `src/data/dashboard-data.json` with backend-generated JSON.  
   - Add fetch on load/refresh; keep existing styling and components.  
   - Render new sections: CEFR badge + per-skill bars, motivation/goal summary, editable chips (learning goals, tutor preferences, scheduling & budget), tutor match teaser (count + 3 blurred cards), and CTA “Find My Professor”.

7) Testing & resilience  
   - Health checks: token generation, ConvoAI join, Thymia call, (optional) Shen call.  
   - Prepare a 30s prerecorded audio fallback for demo if mic fails.  
   - Venue dry-run: verify on-site network; avoid tunnels unless required.

8) Documentation & submission  
   - Fill `HOW_WE_BUILT.md` with architecture, prompts, failures, iterations.  
   - Add an architecture diagram to team README.  
   - Update `TEAM_SETUP_GUIDE.md` with final flags/commands.  
   - Keep demo script in `submissions/LosPerrazos/demo-assets/` (steps + backup clip).

9) Branching & delivery  
   - Active branch: `dev-dani`; PR to `main` once end-to-end is green.  
   - Tag commit hash for the live demo.

## Risks & Mitigations
- Network/IT blocks (Zscaler, TLS, camera): keep Shen optional; have prerecorded audio; run everything over HTTPS without tunnels.  
- Provider latency/timeouts: set per-call timeouts + retry once; surface “Processing…” messages.  
- Env drift between repos: single source of truth env templates + sanity script.  
- Demo flakiness: backup clip, mock vitals, and a “reload dashboard” button.

## Milestones (relative)
- M1: Flow + schema frozen; env templates checked in.  
- M2: Backend running with Thymia integration; JSON emitted.  
- M3: Avatar client talking end-to-end; manual JSON fetch works.  
- M4: Dashboard auto-refreshes with live session data.  
- M5: Demo script rehearsed; HOW_WE_BUILT.md + README diagram done; PR ready.

## Definition of Done (for demo)
- Single command (per profile) starts backend + client with valid env.  
- Live conversation produces a summary JSON consumed by the dashboard without manual edits.  
- UI shows clear status when Shen is disabled and does not crash if Thymia is unreachable.  
- Docs updated: TEAM_SETUP_GUIDE, HOW_WE_BUILT, architecture diagram, demo script.
