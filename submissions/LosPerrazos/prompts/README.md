# Smart Onboard Prompts & Schema

This folder holds the conversation prompts and the contract for the session summary JSON that powers the dashboard.

Key files:
- `system_prompt.md` — system/developer guidance for the agent (onboarding flow + style).
- `session_summary_schema.json` — canonical shape of the summary the backend should emit after a session.
- `examples/latest-session.example.json` — example payload that matches the schema.

Usage:
1) Load `system_prompt.md` into the LLM middleware (e.g., server-custom-llm) for the VIDEO/THYMIA profiles.
2) After each session, merge transcript + Thymia (+ Shen if enabled) into a JSON matching `session_summary_schema.json` and write it to `submissions/LosPerrazos/src/data/latest-session.json` (or serve it via an endpoint the dashboard can fetch).
3) The dashboard first tries `latest-session.json`; if missing, it falls back to `dashboard-data.json`.
