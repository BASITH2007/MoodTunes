// ── STATE ───────────────────────────────────────────────────
let stream = null;
let detectionInterval = null;
let currentEmotion = null;
let modelsLoaded = false;

let lastSavedEmotion = null;
let lastSavedTime = 0;

// ── TEXT KEYWORDS ───────────────────────────────────────────
const TEXT_KEYWORDS = {
  happy:     ['happy','joy','excited','great','amazing','awesome','wonderful','good','love','smile','laugh','fun','fantastic','excellent','thrilled','elated','cheerful','yay','blessed','grateful','glad','delighted'],
  sad:       ['sad','cry','depressed','unhappy','miserable','upset','hurt','pain','lonely','heartbroken','sorrow','grief','tears','down','blue','gloomy','crying','miss','lost','empty'],
  angry:     ['angry','mad','furious','hate','rage','annoyed','irritated','frustrated','outraged','livid','terrible','awful','stupid','ridiculous','unfair','ugh','argh'],
  fearful:   ['scared','afraid','fear','anxious','nervous','worried','panic','stress','terrified','anxiety','dread','overwhelmed','tense','uneasy','shaky'],
  surprised: ['surprised','shocked','wow','omg','unbelievable','unexpected','astonished','speechless','whoa','really','seriously','what','no way'],
  disgusted: ['disgusted','gross','nasty','sick','eww','yuck','revolting','horrible','awful','disgusting','hate','vile','awful'],
  neutral:   ['okay','fine','alright','normal','usual','nothing','meh','bored','whatever','average','so-so','just','kind of'],
};

// ── MODEL LOADING ───────────────────────────────────────────
async function loadModels() {
  const sub = document.getElementById('loaderSub');
  const title = document.getElementById('loaderTitle');
  const prog = document.getElementById('progressFill');

  // Use Django static models path if defined, fallback to CDN
  const localUrl = window.STATIC_MODELS_URL || '/static/detector/models/';
  const MODEL_URLS = [
    localUrl,
    'https://cdn.jsdelivr.net/gh/vladmandic/face-api/model',
  ];

  for (let i = 0; i < MODEL_URLS.length; i++) {
    const url = MODEL_URLS[i];
    const label = i === 0 ? 'local Django static folder' : `CDN source`;
    try {
      title.textContent = 'Loading AI Models';
      sub.textContent = `Trying ${label}...`;
      prog.style.width = `${10 + i * 40}%`;
      console.log(`[MoodTunes] Trying model URL: ${url}`);

      await faceapi.nets.tinyFaceDetector.loadFromUri(url);
      console.log('[MoodTunes] tinyFaceDetector loaded OK');
      prog.style.width = '70%';
      sub.textContent = 'Loading face expressions model...';

      await faceapi.nets.faceExpressionNet.loadFromUri(url);
      console.log('[MoodTunes] faceExpressionNet loaded OK');
      prog.style.width = '100%';

      modelsLoaded = true;
      sub.textContent = '✅ Models loaded successfully!';

      setTimeout(() => {
        document.getElementById('loadingOverlay').style.display = 'none';
      }, 500);

      document.getElementById('statusText').textContent = 'AI Ready ✅';
      document.getElementById('statusDot').className = 'dot';
      showToast('✅ AI ready! Click ▶ Start Camera to detect your emotion.');
      return; // success — stop trying

    } catch (err) {
      console.warn(`Source ${i+1} failed (${url}):`, err.message);
      sub.textContent = `Source ${i+1} failed, trying next...`;
    }
  }

  // ALL sources failed
  title.textContent = '⚠️ Models Need Setup';
  prog.style.width = '100%';
  prog.style.background = '#ef4444';
  sub.innerHTML = `
    <span style="color:#ef4444;font-size:1rem;font-weight:600;">Models Failed to Load</span><br><br>
    Please ensure the models are copied into the static directory or your device is online to reach the CDN.<br><br>
    <span style="color:#6b7280;font-size:0.8rem;">You can use the ✍️ Text tab in the meantime</span>
  `;
  document.getElementById('statusDot').className = 'dot red';
  document.getElementById('statusText').textContent = 'Loading Failed';

  setTimeout(() => {
    document.getElementById('loadingOverlay').style.display = 'none';
  }, 4000);
}

window.addEventListener('DOMContentLoaded', () => {
  loadModels();
  loadHistory();
});

// ── TABS ────────────────────────────────────────────────────
function switchTab(tab) {
  document.querySelectorAll('.tab').forEach((t, i) => {
    t.classList.toggle('active', ['camera','text'][i] === tab);
  });
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
  if (tab !== 'camera') stopCamera();
}

// ── CAMERA ──────────────────────────────────────────────────
async function startCamera() {
  if (!modelsLoaded) {
    showToast('⏳ AI models not loaded. Try Text mode instead.');
    return;
  }
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user', width: 640, height: 480 } });
    const video = document.getElementById('video');
    video.srcObject = stream;
    video.style.display = 'block';
    document.getElementById('camPlaceholder').style.display = 'none';
    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-flex';
    document.getElementById('snapBtn').style.display = 'inline-flex';
    document.getElementById('detectingBadge').classList.add('active');

    video.onloadedmetadata = () => {
      video.play();
      showToast('Camera ready! Look directly at the camera.');
      setTimeout(() => {
        detectionInterval = setInterval(detectEmotion, 1000);
      }, 1000);
    };

  } catch (e) {
    console.error('[MoodTunes] Camera error:', e);
    showToast('Camera access denied. Please allow camera in browser settings.');
  }
}

function stopCamera() {
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
  clearInterval(detectionInterval);
  const video = document.getElementById('video');
  video.style.display = 'none';
  document.getElementById('camPlaceholder').style.display = 'flex';
  document.getElementById('startBtn').style.display = 'inline-flex';
  document.getElementById('stopBtn').style.display = 'none';
  document.getElementById('snapBtn').style.display = 'none';
  document.getElementById('detectingBadge').classList.remove('active');
  
  // Clear face detection canvas box
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

async function detectEmotion() {
  const video = document.getElementById('video');
  if (!video.srcObject || video.readyState < 2) return;
  try {
    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions({ inputSize: 224, scoreThreshold: 0.3 }))
      .withFaceExpressions();

    const canvas = document.getElementById('canvas');
    const wrap = document.getElementById('cameraWrap');
    canvas.width = wrap.offsetWidth;
    canvas.height = wrap.offsetHeight;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (detections.length > 0) {
      const det = detections[0];
      const scaleX = canvas.width / video.videoWidth;
      const scaleY = canvas.height / video.videoHeight;
      const box = det.detection.box;
      const mx = canvas.width - (box.x + box.width) * scaleX;
      ctx.strokeStyle = '#7c3aed';
      ctx.lineWidth = 2;
      ctx.strokeRect(mx, box.y * scaleY, box.width * scaleX, box.height * scaleY);
      ctx.fillStyle = 'rgba(124,58,237,0.8)';
      ctx.fillRect(mx, box.y * scaleY - 24, 60, 24);
      ctx.fillStyle = '#fff';
      ctx.font = '12px DM Sans';
      ctx.fillText('Face ✓', mx + 5, box.y * scaleY - 7);
      
      updateEmotionDisplay(det.expressions, 'camera');
    }
  } catch (e) {
    console.error('[MoodTunes] Detection error:', e);
  }
}

async function snapEmotion() {
  await detectEmotion();
  showToast('📸 Emotion captured!');
}

// ── EMOTION DISPLAY & API INTEGRATION ────────────────────────
const EMOTION_EMOJIS = { happy:'😄', sad:'😢', angry:'😡', surprised:'😲', fearful:'😨', disgusted:'🤢', neutral:'😐' };
const EMOTION_COLORS = { happy:'var(--happy)', sad:'var(--sad)', angry:'var(--angry)', surprised:'var(--surprised)', fearful:'var(--fearful)', disgusted:'var(--disgusted)', neutral:'var(--neutral)' };
const EMOTION_ORDER = ['happy','sad','angry','surprised','fearful','disgusted','neutral'];

function updateEmotionDisplay(expressions, method) {
  const dominant = Object.entries(expressions).sort((a,b) => b[1]-a[1])[0];
  const name = dominant[0];
  const conf = (dominant[1]*100).toFixed(1);
  
  document.getElementById('waitingState').style.display = 'none';
  document.getElementById('emotionDisplay').style.display = 'block';
  document.getElementById('emotionEmoji').textContent = EMOTION_EMOJIS[name] || '🎭';
  document.getElementById('emotionName').textContent = name.charAt(0).toUpperCase()+name.slice(1);
  document.getElementById('emotionName').style.color = EMOTION_COLORS[name] || 'white';
  document.getElementById('emotionConf').textContent = `Confidence: ${conf}%`;
  
  const barsEl = document.getElementById('emotionBars');
  barsEl.innerHTML = '';
  EMOTION_ORDER.forEach(em => {
    const val = (expressions[em]||0)*100;
    const row = document.createElement('div');
    row.className = 'bar-row';
    row.innerHTML = `<div class="bar-label">${em}</div><div class="bar-track"><div class="bar-fill" style="width:${val.toFixed(1)}%;background:${EMOTION_COLORS[em]}"></div></div><div class="bar-val">${val.toFixed(0)}%</div>`;
    barsEl.appendChild(row);
  });
  
  if (name !== currentEmotion) { 
    currentEmotion = name; 
    updatePlaylist(name); 
  }

  // Rate-limited history saving to database
  const now = Date.now();
  const timeElapsed = now - lastSavedTime;
  const isDifferentEmotion = name !== lastSavedEmotion;

  if (isDifferentEmotion || timeElapsed > 15000) {
    lastSavedEmotion = name;
    lastSavedTime = now;
    saveDetection(name, dominant[1], method);
  }
}

// ── TEXT ANALYSIS ───────────────────────────────────────────
function analyzeText() {
  const text = document.getElementById('moodText').value.toLowerCase();
  if (!text.trim()) { showToast('✍️ Please type something first!'); return; }
  const scores = {};
  Object.entries(TEXT_KEYWORDS).forEach(([emotion, words]) => {
    scores[emotion] = words.filter(w => text.includes(w)).length;
  });
  const best = Object.entries(scores).sort((a,b)=>b[1]-a[1])[0];
  const emotion = best[1]>0 ? best[0] : 'neutral';
  const total = Math.max(Object.values(scores).reduce((a,b)=>a+b,0), 1);
  const expressions = {};
  EMOTION_ORDER.forEach(e => { expressions[e] = (scores[e]||0)/total; });
  if (best[1]===0) expressions.neutral = 1;
  
  updateEmotionDisplay(expressions, 'text');
  showToast(`🎭 Mood detected: ${emotion.charAt(0).toUpperCase()+emotion.slice(1)}!`);
}

// ── DJANGO API CONNECTORS ────────────────────────────────────

// Fetch recommended songs from Django database
async function updatePlaylist(emotion) {
  try {
    const response = await fetch(`/api/recommend-songs/?emotion=${emotion}`);
    if (!response.ok) throw new Error('API failure');
    const data = await response.json();
    
    document.getElementById('playlistWaiting').style.display = 'none';
    document.getElementById('playlistSection').style.display = 'block';
    
    const badge = document.getElementById('playlistBadge');
    badge.textContent = emotion.charAt(0).toUpperCase()+emotion.slice(1);
    
    // Set badge style based on emotion color
    const color = EMOTION_COLORS[emotion] || 'var(--neutral)';
    badge.style.background = `${color}22`;
    badge.style.color = color;
    badge.style.border = `1px solid ${color}44`;
    
    const grid = document.getElementById('tracksGrid');
    grid.innerHTML = '';
    
    data.tracks.forEach(track => {
      const a = document.createElement('a');
      a.href = track.url; 
      a.target = '_blank'; 
      a.rel = 'noopener noreferrer'; 
      a.className = 'track-card';
      a.innerHTML = `
        <div class="track-thumb" style="background:${color}22">${track.emoji}</div>
        <div class="track-info">
          <div class="track-title">${track.title}</div>
          <div class="track-artist">${track.artist}</div>
        </div>
        <div class="track-action" style="background:${color}">▶</div>
      `;
      grid.appendChild(a);
    });
  } catch (err) {
    console.error('[MoodTunes] Error fetching playlist:', err);
    showToast('❌ Failed to load playlist from server');
  }
}

// Save detection history to Django database
async function saveDetection(mood, confidence, method) {
  try {
    const response = await fetch('/api/save-detection/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        mood: mood,
        confidence: confidence,
        detection_method: method
      })
    });
    if (response.ok) {
      console.log(`[MoodTunes] Detection saved: ${mood} (${method})`);
      loadHistory(); // Reload history section asynchronously
    }
  } catch (err) {
    console.error('[MoodTunes] Error saving detection:', err);
  }
}

// Fetch and render detection history list
async function loadHistory() {
  try {
    const response = await fetch('/api/get-history/');
    if (!response.ok) throw new Error('History fetch failed');
    const data = await response.json();
    
    const historyList = document.getElementById('historyList');
    if (!historyList) return;
    
    if (data.history.length === 0) {
      historyList.innerHTML = `<div class="history-empty">No detections recorded yet. Detections will appear here in real-time.</div>`;
      return;
    }
    
    historyList.innerHTML = '';
    data.history.forEach(item => {
      const emoji = EMOTION_EMOJIS[item.mood] || '🎭';
      const color = EMOTION_COLORS[item.mood] || 'var(--neutral)';
      const confPercent = (item.confidence * 100).toFixed(0);
      
      const div = document.createElement('div');
      div.className = 'history-item';
      div.innerHTML = `
        <div class="history-meta">
          <span style="font-size: 1.5rem;">${emoji}</span>
          <div>
            <div class="history-mood-name" style="color: ${color}">${item.mood} (${confPercent}%)</div>
            <div class="history-time">${item.timestamp}</div>
          </div>
        </div>
        <span class="history-method ${item.detection_method}">${item.detection_method}</span>
      `;
      historyList.appendChild(div);
    });
  } catch (err) {
    console.error('[MoodTunes] Error loading history:', err);
  }
}

// ── TOAST ───────────────────────────────────────────────────
let toastTimeout;
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => t.classList.remove('show'), 3500);
}
