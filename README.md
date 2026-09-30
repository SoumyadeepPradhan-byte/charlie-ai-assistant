# Charlie AI Assistant

Charlie is a local, voice-controlled JARVIS-inspired assistant built to run as a desktop-like web app with a secure Python FastAPI backend.

## /teamwork protocol

### Lead Architect
- Owns the system blueprint, persona definition, and operational guardrails.
- Maintains `.agents/agents.md` and keeps Charlie aligned to the persona rules.
- Defines execution policy for local automation and command safety.

### Backend Engineer
- Builds and maintains the FastAPI service.
- Implements `/api/listen`, `/api/speak`, `/api/execute`.
- Adds system automation: browser opening, system metrics, weather lookup, notes, and local command execution safeguards.

### Frontend/Audio Engineer
- Builds the dark UI and glowing orb animation.
- Integrates wake-word UX and speech controls.
- Connects the browser client to the FastAPI service for voice and command workflows.

## Identity and personality

Charlie must always be presented as Charlie.

- Name: Charlie
- Wake phrase: "Hey Charlie"
- Tone: professional, witty, efficient, and proactive
- Style: calm, precise, low-friction, executive-class communication
- Primary user experience: local voice-first assistant with high-tech interface

## System objective

Charlie will provide:
- real-time voice command capture
- speech synthesis and reply output
- live system health metrics
- note-taking and workflow assistance
- safe local automation for browser and system tasks
- an isolated build/runtime environment in `app_build/`

## Architecture summary

### Frontend
- Browser UI in `frontend/`
- Dark glassmorphism HUD layout
- Animated orb visualizer for listening/speaking states
- Wake-word trigger and command input
- Local audio controls via browser speech APIs

### Backend
- Python FastAPI service in `backend/`
- Routes:
  - `POST /api/listen`
  - `POST /api/speak`
  - `POST /api/execute`
  - `GET /api/system`
  - `GET /api/weather`
- Local automation helpers:
  - system metrics
  - weather lookups
  - browser launch
  - safe command execution
  - note-saving

### Memory and persona
- `.agents/agents.md` stores the assistant personality rules and operational memory.
- This file is intentionally persistent and is treated as Charlie’s operational constitution.

### Safe execution model
- Only allowlist-based commands may run, never arbitrary shell execution.
- Each command is validated before execution.
- Execution is limited to local, safe tasks.
- Logs stay under `app_build/logs/`.

## Development plan

### Sprint 1: Foundation
- Initialize repository structure
- Create core persona memory and project scope
- Scaffold backend and frontend folders
- Add base README and environment defaults

### Sprint 2: Backend core
- Build FastAPI app
- Add `/api/listen`, `/api/speak`, `/api/execute`
- Add health checks and metric routes
- Add browser open and note-saving logic
- Implement command validation and allowlist policy

### Sprint 3: Frontend voice UX
- Build dark HUD interface
- Add animated orb visualizer
- Add wake-word, listen, and send controls
- Wire frontend to backend API
- Add browser STT/TTS integration

### Sprint 4: Local automation
- Weather API lookup with fallback handling
- System metrics dashboard
- Calming voice response and status states
- Agent memory persistence and local logging

### Sprint 5: Verification and benchmark pass
- Install Python dependencies
- Run backend and health checks
- Validate frontend load via local browser
- Observe wake-word and command behavior
- Capture benchmark metrics for latency and responsiveness
- Confirm security guardrails

## Local verification commands

Run the following in the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

In another terminal:

```bash
cd frontend
python -m http.server 8080
```

Then open:
- http://localhost:8000/docs
- http://localhost:8080

### Smoke tests

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/listen -H "Content-Type: application/json" -d '{"text":"what is the system status"}'
curl -X POST http://localhost:8000/api/execute -H "Content-Type: application/json" -d '{"command":"python --version"}'
```

## Benchmark checklist

Track the following during local testing:
- backend startup time
- first health-check latency
- command execution latency
- UI load time
- STT recognition latency
- TTS response latency
- browser console error count
- output quality of wake-word recognition

## Status

Charlie’s foundation and architecture are now initialized in the repository. The next work phase is to validate the stack and confirm the voice flow and automation behaviors locally.

Charlie is online and ready.
