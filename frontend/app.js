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
    addLine(`Charlie: ${result.result}`);
    setStatus('Ready');
    setOrbState('speaking');
    await speakText(result.result);
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
    const result = await fetch(`${backendBase}/api/system`);
    const data = await result.json();
    addLine(`Charlie: ${JSON.stringify(data)}`);
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
