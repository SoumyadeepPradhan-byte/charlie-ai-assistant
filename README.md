# Charlie: Local Voice-Controlled AI Assistant

Charlie is a local, voice-controlled AI assistant inspired by JARVIS. This repository establishes the autonomous development plan, team structure, and working project scaffolding for a desktop-like voice assistant with a dark, high-tech interface and a Python FastAPI backend.

## /teamwork Protocol

Role allocation:
- Lead Architect: Defines the system architecture, safety constraints, persona rules, and execution boundaries.
- Backend Engineer: Implements FastAPI endpoints, secure local automation, weather, metrics, and task orchestration.
- Frontend/Audio Engineer: Implements wake-word UX, live visual orb, audio controls, STT/TTS integration, and web UI.

## Project Goals

1. Identity and character: Charlie is an autonomous assistant with a confident, professional, witty, proactive tone. All responses refer to the assistant as Charlie.
2. Voice control: Real-time wake-word detection for "Hey Charlie", STT/TTS support, and a responsive dark-mode conversation UI.
3. Local automation: System metrics, browser opening, weather lookup, note-taking, and command execution with safe policies.
4. Memory architecture: A persistent persona and operational memory file in `.agents/agents.md`.
5. Execution isolation: The entire build environment is isolated under `app_build/`.

## Repository Layout

- `.agents/agents.md` — persistent persona rules and memory.
- `app_build/` — execution-isolated environment configuration and build notes.
- `backend/` — FastAPI backend and automation skills.
- `frontend/` — HTML/CSS/JS voice assistant UI.
- `README.md` — project overview and run instructions.
- `.gitignore` — standard Python ignores.

## Quick Start

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:

Open `frontend/index.html` directly in a browser, or serve it with a simple static host:

```bash
cd frontend
python -m http.server 8080
```

Then open:
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:8080

## Architecture Overview

- Frontend: Browser UI with wake-word detection, orb animation, STT/TTS, and command forms.
- Backend: FastAPI service with `/api/listen`, `/api/speak`, `/api/execute`, and automation helpers.
- Skills: Browser open, weather lookup, metrics, note-taking, and secure local execution.
- Memory: `.agents/agents.md` defines Charlie’s persona, safety boundaries, and operating model.

## Security

Charlie uses strict allow-list validation for local commands and only permits safe, local execution patterns. No arbitrary shell execution is allowed outside the defined policy set.

## Current Status

This repository is initialized as a foundation for the full Charlie build. It includes the persona memory, architecture plan, backend skeleton, and frontend UI scaffold. Local verification steps are included in the build docs and can be run in a development environment.

---

Charlie is online and ready to assist.
