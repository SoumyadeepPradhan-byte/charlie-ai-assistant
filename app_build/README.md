# App Build Environment

This folder isolates Charlie’s execution environment and build packaging from the workspace root.

## Structure

- `bin/` — helper scripts and startup commands
- `config/` — environment defaults and deployment config
- `logs/` — local execution logs
- `tmp/` — temporary data and debug payloads

## Purpose

The `app_build/` directory provides a sandbox for local automation, package build workflows, and operational isolation. This prevents direct workspace pollution while keeping Charlie executable in a controlled environment.

## Recommended Commands

```bash
mkdir -p app_build/bin app_build/config app_build/logs app_build/tmp
```

Charlie is configured to stay inside this build footprint for local-system execution tasks.
