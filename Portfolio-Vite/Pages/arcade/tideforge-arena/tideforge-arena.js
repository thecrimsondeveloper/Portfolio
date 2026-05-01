const canvas = document.getElementById('game');
const overlay = document.getElementById('overlay');
const overlayTitle = document.getElementById('overlay-title');
const overlayCopy = document.getElementById('overlay-copy');
const actionButton = document.getElementById('action');
const hud = document.getElementById('hud');
const ctx = canvas.getContext('2d');
let width = 0;
let height = 0;
let arena = { x: 0, y: 0, radius: 0 };
let player = { x: 0, y: 0, radius: 16, speed: 280 };
let keys = {};
let currentWaves = [];
let shards = [];
let lastSpawn = 0;
let score = 0;
let gameOver = true;
let inPlay = false;
let startTime = 0;
const shardCount = 3;
window.addEventListener('keydown', (event) => {
  keys[event.key.toLowerCase()] = true;
});
window.addEventListener('keyup', (event) => {
  keys[event.key.toLowerCase()] = false;
});
window.addEventListener('resize', resize);
function resize() {
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
  arena.x = width / 2;
  arena.y = height / 2;
  arena.radius = Math.min(width, height) * 0.37;
  player.x = arena.x;
  player.y = arena.y;
}
function showOverlay(title, copy, action) {
  overlayTitle.textContent = title;
  overlayCopy.textContent = copy;
  actionButton.textContent = action;
  overlay.style.display = 'flex';
}
function hideOverlay() {
  overlay.style.display = 'none';
}
function spawnShard() {
  const angle = Math.random() * Math.PI * 2;
  const distance = arena.radius * 0.65;
  shards.push({
    x: arena.x + Math.cos(angle) * distance,
    y: arena.y + Math.sin(angle) * distance,
    radius: 12,
    pulse: 0
  });
}
function spawnWave() {
  const edge = Math.floor(Math.random() * 4);
  const angle = edge * (Math.PI / 2) + Math.PI / 4;
  const speed = 140 + (score * 0.5);
  const origin = {
    x: arena.x + Math.cos(angle) * (arena.radius + 80),
    y: arena.y + Math.sin(angle) * (arena.radius + 80)
  };
  const dx = arena.x - origin.x;
  const dy = arena.y - origin.y;
  const len = Math.sqrt(dx * dx + dy * dy);
  currentWaves.push({
    x: origin.x,
    y: origin.y,
    vx: (dx / len) * speed,
    vy: (dy / len) * speed,
    radius: 18,
    created: performance.now()
  });
}
function resetArena() {
  currentWaves = [];
  shards = [];
  for (let i = 0; i < shardCount; i += 1) spawnShard();
  lastSpawn = performance.now();
  score = 0;
  player.x = arena.x;
  player.y = arena.y;
}
function distance(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return Math.sqrt(dx * dx + dy * dy);
}
function clampPlayer() {
  const dx = player.x - arena.x;
  const dy = player.y - arena.y;
  const dist = Math.sqrt(dx * dx + dy * dy);
  if (dist + player.radius > arena.radius) {
    const normal = (arena.radius - player.radius) / dist;
    player.x = arena.x + dx * normal;
    player.y = arena.y + dy * normal;
  }
}
function update(delta) {
  if (!inPlay || gameOver) return;
  const velocity = player.speed * delta;
  if (keys.arrowup || keys.w) player.y -= velocity;
  if (keys.arrowdown || keys.s) player.y += velocity;
  if (keys.arrowleft || keys.a) player.x -= velocity;
  if (keys.arrowright || keys.d) player.x += velocity;
  clampPlayer();
  const now = performance.now();
  if (now - lastSpawn > 1900) {
    spawnWave();
    lastSpawn = now;
  }
  currentWaves.forEach((wave, index) => {
    wave.x += wave.vx * delta;
    wave.y += wave.vy * delta;
    if (distance(wave, player) < wave.radius + player.radius) {
      endRun('Pulled apart by a tide pulse.');
    }
    if (distance(wave, arena) > arena.radius + 180) {
      currentWaves.splice(index, 1);
    }
  });
  shards.forEach((shard, index) => {
    shard.pulse += delta * 2;
    if (distance(shard, player) < shard.radius + player.radius) {
      score += 18;
      shards.splice(index, 1);
      spawnShard();
    }
  });
  score += delta * 12;
}
function drawBackground() {
  const grd = ctx.createRadialGradient(arena.x, arena.y, 0, arena.x, arena.y, arena.radius);
  grd.addColorStop(0, '#0b1d31');
  grd.addColorStop(1, '#071118');
  ctx.fillStyle = grd;
  ctx.fillRect(0, 0, width, height);
}
function drawArena() {
  ctx.beginPath();
  ctx.arc(arena.x, arena.y, arena.radius, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(7, 27, 45, 0.9)';
  ctx.fill();
  ctx.lineWidth = 4;
  ctx.strokeStyle = '#1f5a84';
  ctx.stroke();
}
function drawShards() {
  shards.forEach((shard) => {
    const pulse = 0.8 + Math.sin(shard.pulse) * 0.18;
    ctx.beginPath();
    ctx.arc(shard.x, shard.y, shard.radius * pulse, 0, Math.PI * 2);
    ctx.fillStyle = '#fad96f';
    ctx.fill();
    ctx.strokeStyle = '#ffe8a0';
    ctx.lineWidth = 3;
    ctx.stroke();
  });
}
function drawWaves() {
  currentWaves.forEach((wave) => {
    ctx.beginPath();
    ctx.arc(wave.x, wave.y, wave.radius, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(76, 188, 255, 0.7)';
    ctx.fill();
  });
}
function drawPlayer() {
  ctx.beginPath();
  ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
  ctx.fillStyle = '#93ebff';
  ctx.fill();
  ctx.lineWidth = 4;
  ctx.strokeStyle = '#c4f7ff';
  ctx.stroke();
}
function drawHud() {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
  ctx.fillRect(24, 24, 260, 90);
  ctx.fillStyle = '#d8f3ff';
  ctx.font = '18px Inter, system-ui, sans-serif';
  ctx.fillText(`Score: ${Math.floor(score)}`, 40, 52);
  ctx.fillText(`Shards: ${shards.length}`, 40, 80);
  ctx.fillText(`Waves: ${currentWaves.length}`, 40, 108);
}
function endRun(message) {
  inPlay = false;
  gameOver = true;
  showOverlay('Arena Offline', `${message} Final score: ${Math.floor(score)}`, 'Restart');
}
function draw() {
  drawBackground();
  drawArena();
  drawShards();
  drawWaves();
  drawPlayer();
  drawHud();
  if (!inPlay || gameOver) {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
    ctx.fillRect(0, 0, width, height);
  }
}
function animate() {
  const now = performance.now();
  const delta = Math.min(0.033, (now - (tideforgeArena.lastTime || now)) / 1000);
  tideforgeArena.lastTime = now;
  update(delta);
  draw();
  requestAnimationFrame(animate);
}
const tideforgeArena = { lastTime: performance.now() };
actionButton.addEventListener('click', () => {
  if (!inPlay || gameOver) {
    resetArena();
    startTime = performance.now();
    inPlay = true;
    gameOver = false;
    hideOverlay();
  }
});
resize();
showOverlay('Tideforge Arena', 'Survive the arena pulse waves, collect forge shards, and stay inside the tidal ring.', 'Enter Arena');
animate();
