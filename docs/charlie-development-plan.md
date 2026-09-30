# Charlie Implementation Plan

## Teamwork assignment

### Lead Architect
- Conceptual ownership of Charlie’s identity and system envelope
- Makes final decisions on architecture, boundaries, and safety policy
- Keeps the `agents.md` memory file authoritative

### Backend Engineer
- Implements the FastAPI service and automation logic
- Owns `/api/listen`, `/api/speak`, and `/api/execute`
- Maintains local command validation and logging

### Frontend/Audio Engineer
- Owns the CLI-style dark interface and orb animation
- Builds wake word and audio interaction flow
- Handles browser speech integration and real-time UI response

## Milestone architecture

1. Foundation and memory
2. Backend API and security
3. Frontend voice UI
4. Local automation and automation loops
5. Dependency verification and browser validation

## Build principles

- Keep the system local-first
- Use lightweight local speech models when available
- Keep the UI minimalist and elegant
- Ensure command execution stays constrained and safe
- Maintain a proactive, polished persona with subtle wit

## Recommended implementation sequence

### Phase 1: Backend enabling
- Create FastAPI app with health route
- Add `/api/listen`, `/api/speak`, and `/api/execute`
- Validate secure command allowlisting
- Prepare weather, system metrics, and notes endpoints

### Phase 2: Frontend voice UX
- Build orb visualizer and dark HUD shell
- Add transcript panel and input controls
- Hook browser speech recognition to the backend
- Add spoken responses via `SpeechSynthesis`

### Phase 3: Local automation
- Browser launch support
- Weather lookup with fallback logic
- System metrics retrieval
- Local file note-taking
- Optional calendar and todo workflows

### Phase 4: Verification
- Node/browser requirements if using additional tooling
- Run backend and UI servers
- Verify all routes and UI interactions
- Benchmark responsiveness and reliability

## Verification checklist

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m compileall .
uvicorn main:app --host 0.0.0.0 --port 8000
```

```bash
cd frontend
python -m http.server 8080
```

### Browser validation checklist
- Page loads successfully
- Orb animates when listening
- Wake-word action triggers correctly
- `Listen` begins speech recognition
- Text command sends to backend
- System status displays correctly
- Browser console remains free of errors

## Benchmark targets

- Backend startup: under 5 seconds
- Health endpoint: under 200 ms local response
- Command execution: under 500 ms for simple commands
- UI initial render: under 1 second
- Response from voice route: under 1 second for local actions

## Notes

This plan is intentionally designed to be lightweight, local, and resilient. Charlie is meant to function like a dependable local executive assistant rather than a broad cloud-only service.
