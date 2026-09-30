from __future__ import annotations

import os
import platform
import shutil
import subprocess
import time
from datetime import datetime
from typing import Any, Dict, List

import psutil
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Charlie Core", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_COMMANDS = [
    "python",
    "node",
    "npm",
    "pip",
    "ls",
    "pwd",
    "whoami",
    "uname",
    "uptime",
    "date",
    "echo",
    "open",
    "start",
    "xdg-open",
]


class ListenRequest(BaseModel):
    text: str | None = None
    audio_url: str | None = None
    wake_word: str = "Hey Charlie"


class SpeakRequest(BaseModel):
    text: str


class ExecuteRequest(BaseModel):
    command: str
    timeout: int = 20
    shell: bool = True


@app.get("/health")
def health_check() -> Dict[str, Any]:
    return {
        "status": "online",
        "assistant": "Charlie",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.post("/api/listen")
def api_listen(payload: ListenRequest) -> Dict[str, Any]:
    transcript = (payload.text or payload.audio_url or "").strip()
    if not transcript:
        raise HTTPException(status_code=400, detail="No input was provided.")

    command = transcript.lower()
    response = {
        "assistant": "Charlie",
        "transcript": transcript,
        "heard_wake_word": "hey charlie" in command,
        "status": "processed",
    }

    if "weather" in command:
        response["intent"] = "weather"
        response["result"] = get_weather_summary()
    elif "system" in command or "metrics" in command:
        response["intent"] = "system_metrics"
        response["result"] = get_system_metrics()
    elif "note" in command:
        response["intent"] = "note"
        response["result"] = save_note(transcript)
    elif "open" in command and "browser" in command:
        response["intent"] = "browser_open"
        response["result"] = open_browser("https://www.google.com")
    else:
        response["intent"] = "general"
        response["result"] = "Charlie is online and ready. I can handle weather, system metrics, browser automation, and note-taking."

    return response


@app.post("/api/speak")
def api_speak(payload: SpeakRequest) -> Dict[str, Any]:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Speech payload cannot be empty.")

    return {
        "assistant": "Charlie",
        "text": text,
        "voice": "default",
        "status": "ready_to_speak",
        "response": f"Charlie says: {text}",
    }


@app.post("/api/execute")
def api_execute(payload: ExecuteRequest) -> Dict[str, Any]:
    command = payload.command.strip()
    if not command:
        raise HTTPException(status_code=400, detail="Command cannot be empty.")

    safe = False
    for allowed in ALLOWED_COMMANDS:
        if command.startswith(allowed):
            safe = True
            break

    if not safe:
        raise HTTPException(status_code=403, detail="Command blocked by Charlie’s execution policy.")

    try:
        result = subprocess.run(
            command,
            shell=payload.shell,
            capture_output=True,
            text=True,
            timeout=payload.timeout,
        )
        return {
            "assistant": "Charlie",
            "command": command,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": "completed",
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Command timed out while Charlie was executing it.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(exc)}")


@app.get("/api/weather")
def api_weather(city: str = "Boston") -> Dict[str, Any]:
    return get_weather_summary(city=city)


@app.get("/api/system")
def api_system() -> Dict[str, Any]:
    return get_system_metrics()


@app.post("/api/notes")
def api_note(content: str) -> Dict[str, Any]:
    return {"assistant": "Charlie", "result": save_note(content)}


def get_system_metrics() -> Dict[str, Any]:
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "assistant": "Charlie",
        "platform": platform.platform(),
        "cpu_percent": cpu,
        "memory": {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "used_gb": round(memory.used / (1024 ** 3), 2),
            "percent": memory.percent,
        },
        "disk": {
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
        },
    }


def save_note(content: str) -> str:
    note_dir = os.path.join(os.getcwd(), "notes")
    os.makedirs(note_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    file_path = os.path.join(note_dir, f"note_{timestamp}.txt")
    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(content)
    return f"Saved note to {file_path}"


def open_browser(url: str) -> str:
    try:
        if platform.system() == "Windows":
            os.startfile(url)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", url])
        else:
            subprocess.Popen(["xdg-open", url])
        return f"Charlie opened the browser to {url}"
    except Exception as exc:
        return f"Charlie failed to open the browser: {exc}"


def get_weather_summary(city: str = "Boston") -> Dict[str, Any]:
    try:
        # Use a free endpoint with no API key for local testing.
        api_url = "https://api.open-meteo.com/v1/forecast"
        response = requests.get(
            api_url,
            params={
                "latitude": 42.3601,
                "longitude": -71.0589,
                "current": "temperature_2m,weather_code",
                "timezone": "auto",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})
        return {
            "assistant": "Charlie",
            "location": city,
            "temperature_c": current.get("temperature_2m"),
            "weather_code": current.get("weather_code"),
            "status": "weather data retrieved",
        }
    except Exception as exc:
        return {
            "assistant": "Charlie",
            "location": city,
            "status": "weather lookup failed",
            "error": str(exc),
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
