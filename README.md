const backendBase = 'http://localhost:8000';
const orbCore = document.getElementById('orb-core');
const statusPill = document.getElementById('status-pill');
const transcriptBox = document.getElementById('transcript-box');
const commandInput = document.getElementById('command-input');
const wakeButton = document.getElementById('wake-button');
const listenButton = document.getElementById('listen-button');
const speakButton = document.getElementById('speak-button');
const systemButton = document.getElementById('system-button');
const sendButton = document.getElementById('send-button');
const taskButton = document.getElementById('task-button');

const cpuValue = document.getElementById('cpu-value');
const memValue = document.getElementById('mem-value');
const weatherValue = document.getElementById('weather-value');
const uptimeValue = document.getElementById('uptime-value');

let recognition = null;

function setStatus(text) {
  statusPill.textContent = text;
}

function addLine(text, type = 'system') {
  const p = document.createElement('p');
  p.className = 'prompt';
  p.textContent = type === 'user' ? `You: ${text}` : text;
  transcriptBox.appendChild(p);
  transcriptBox.scrollTop = transcriptBox.scrollHeight;
}

function setOrbState(state) {
  orbCore.classList.remove('listening', 'speaking');
  if (state === 'listening') orbCore.classList.add('listening');
  if (state === 'speaking') orbCore.classList.add('speaking');
}

function renderSystemMetrics(data) {
  const cpu = data?.cpu_percent ?? '--';
  const memory = data?.memory?.percent ?? '--';
  const uptime = data?.uptime_seconds ? `${Math.round(data.uptime_seconds / 3600)}h` : '--';
  cpuValue.textContent = `${cpu}%`;
  memValue.textContent = `${memory}%`;
  uptimeValue.textContent = uptime;
}

async function fetchWeather() {
  try {
    const res = await fetch(`${backendBase}/api/weather?city=Boston`);
    const data = await res.json();
    const temp = data?.temperature_c ?? '--';
    weatherValue.textContent = `${temp}°C`;
  } catch (err) {
    weatherValue.textContent = 'N/A';
  }
}

async function fetchMetrics() {
  try {
    const res = await fetch(`${backendBase}/api/system`);
    const data = await res.json();
    renderSystemMetrics(data);
  } catch (err) {
    cpuValue.textContent = 'N/A';
    memValue.textContent = 'N/A';
    uptimeValue.textContent = 'N/A';
  }
}

async function callAssistant(endpoint, payload) {
  const response = await fetch(`${backendBase}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Charlie failed to respond.');
  }

  return response.json();
}

async function sendTextCommand(text) {
  addLine(text, 'user');
  setStatus('Processing');
  setOrbState('listening');

  try {
    const result = await callAssistant('/api/listen', { text });
    const responseText = typeof result.result === 'string' ? result.result : JSON.stringify(result.result);
    addLine(`Charlie: ${responseText}`);
    setStatus('Ready');
    setOrbState('speaking');
    await speakText(responseText);
  } catch (err) {
    addLine(`Charlie: ${err.message}`);
    setStatus('Alert');
  } finally {
    setOrbState('');
  }
}

function speakText(text) {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1.1;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  }
  return Promise.resolve();
}

function initializeSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    addLine('Charlie: Browser voice recognition is unavailable in this environment. Use the text field to continue.');
    return;
  }

  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.lang = 'en-US';

  recognition.onstart = () => {
    setStatus('Listening');
    setOrbState('listening');
    addLine('Charlie: Listening for your command.');
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    addLine(transcript, 'user');
    const lower = transcript.toLowerCase();
    if (lower.includes('hey charlie')) {
      const cleaned = transcript.replace(/hey charlie/gi, '').trim();
      if (cleaned) {
        sendTextCommand(cleaned);
      } else {
        addLine('Charlie: I’m ready for your next command.');
      }
    } else {
      sendTextCommand(transcript);
    }
  };

  recognition.onerror = (event) => {
    addLine(`Charlie: Voice capture error: ${event.error}`);
    setStatus('Standby');
    setOrbState('');
  };

  recognition.onend = () => {
    setStatus('Ready');
    setOrbState('');
  };
}

wakeButton.addEventListener('click', () => {
  addLine('Charlie: Wake phrase detected. "Hey Charlie"');
  setStatus('Listening');
  setOrbState('listening');
  setTimeout(() => setOrbState(''), 1200);
});

listenButton.addEventListener('click', () => {
  if (!recognition) initializeSpeechRecognition();
  if (recognition) recognition.start();
});

speakButton.addEventListener('click', () => {
  const text = commandInput.value.trim() || 'Charlie is online and ready.';
  speakText(text);
  addLine(`Charlie: ${text}`);
});

systemButton.addEventListener('click', async () => {
  try {
    const res = await fetch(`${backendBase}/api/system`);
    const data = await res.json();
    renderSystemMetrics(data);
    addLine(`Charlie: ${JSON.stringify(data)}`);
  } catch (err) {
    addLine(`Charlie: ${err.message}`);
  }
});

taskButton.addEventListener('click', async () => {
  const title = prompt('Charlie task title:');
  if (!title) return;
  const description = prompt('Task description:') || '';

  try {
    const res = await fetch(`${backendBase}/api/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description }),
    });
    const data = await res.json();
    addLine(`Charlie: Task created — ${data.task.title}`);
  } catch (err) {
    addLine(`Charlie: ${err.message}`);
  }
});

sendButton.addEventListener('click', () => {
  const text = commandInput.value.trim();
  if (text) {
    sendTextCommand(text);
    commandInput.value = '';
  }
});

commandInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    const text = commandInput.value.trim();
    if (text) {
      sendTextCommand(text);
      commandInput.value = '';
    }
  }
});

initializeSpeechRecognition();
setStatus('Standby');
fetchMetrics();
fetchWeather();
setInterval(() => {
  fetchMetrics();
  fetchWeather();
}, 15000);
