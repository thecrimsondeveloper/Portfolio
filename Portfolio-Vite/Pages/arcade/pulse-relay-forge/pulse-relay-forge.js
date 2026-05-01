const canvas = document.getElementById('game');
const overlay = document.getElementById('overlay');
const overlayTitle = document.getElementById('overlay-title');
const overlayCopy = document.getElementById('overlay-copy');
const actionButton = document.getElementById('action');
const hud = document.getElementById('hud');
const ctx = canvas.getContext('2d');
let width = 0;
let height = 0;
let nodePositions = [];
let currentTarget = null;
let score = 0;
let combo = 0;
let timeout = 1400;
let nextExpire = 0;
let gameOver = true;
let inPlay = false;
const keyMap = {
  Digit1: 0,
  Digit2: 1,
  Digit3: 2,
  Digit4: 3,
  q: 0,
  w: 1,
  a: 2,
  s: 3
};
function resize() {
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
  const radius = Math.min(width, height) * 0.18;
  nodePositions = [
    { x: width * 0.3, y: height * 0.32, label: '1' },
    { x: width * 0.7, y: height * 0.32, label: '2' },
    { x: width * 0.3, y: height * 0.68, label: '3' },
    { x: width * 0.7, y: height * 0.68, label: '4' }
  ];
}
window.addEventListener('resize', resize);
window.addEventListener('keydown', (event) => {
  if (!inPlay || gameOver) return;
  const index = keyMap[event.key];
  if (index !== undefined) handleInput(index);
});
function showOverlay(title, copy, action) {
  overlayTitle.textContent = title;
  overlayCopy.textContent = copy;
  actionButton.textContent = action;
  overlay.style.display = 'flex';
}
function hideOverlay() {
  overlay.style.display = 'none';
}
function randomTarget() {
  let next = Math.floor(Math.random() * 4);
  while (next === currentTarget) {
    next = Math.floor(Math.random() * 4);
  }
  return next;
}
function startRun() {
  score = 0;
  combo = 0;
  timeout = 1400;
  currentTarget = randomTarget();
  nextExpire = performance.now() + timeout;
  inPlay = true;
  gameOver = false;
  hideOverlay();
}
function endRun(message) {
  inPlay = false;
  gameOver = true;
  showOverlay('Forge Offline', `${message} Final score: ${score}`, 'Reforge');
}
function handleInput(index) {
  if (index !== currentTarget) {
    endRun('Relay broken.');
    return;
  }
  score += 10 + combo * 2;
  combo += 1;
  if (combo % 5 === 0) {
    timeout = Math.max(700, timeout - 80);
  }
  currentTarget = randomTarget();
  nextExpire = performance.now() + timeout;
}
function drawBackground() {
  const gradient = ctx.createLinearGradient(0, 0, 0, height);
  gradient.addColorStop(0, '#071721');
  gradient.addColorStop(1, '#081b2d');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);
}
function drawNodes() {
  nodePositions.forEach((node, index) => {
    const isActive = index === currentTarget && inPlay && !gameOver;
    ctx.beginPath();
    ctx.arc(node.x, node.y, 58, 0, Math.PI * 2);
    ctx.fillStyle = isActive ? '#ffd96f' : '#2c5267';
    ctx.fill();
    ctx.lineWidth = 6;
    ctx.strokeStyle = isActive ? '#ffb84c' : '#36506c';
    ctx.stroke();
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 32px Inter, system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(node.label, node.x, node.y);
  });
}
function drawChain() {
  ctx.lineWidth = 4;
  ctx.strokeStyle = 'rgba(124, 234, 255, 0.28)';
  ctx.beginPath();
  nodePositions.forEach((node, index) => {
    if (index === 0) ctx.moveTo(node.x, node.y);
    else ctx.lineTo(node.x, node.y);
  });
  ctx.stroke();
}
function drawHud() {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
  ctx.fillRect(20, 20, 260, 110);
  ctx.fillStyle = '#b9f1ff';
  ctx.font = '18px Inter, system-ui, sans-serif';
  ctx.fillText(`Score: ${score}`, 36, 50);
  ctx.fillText(`Combo: ${combo}`, 36, 78);
  ctx.fillText(`Timeout: ${(timeout / 1000).toFixed(2)}s`, 36, 106);
  const timeLeft = inPlay ? Math.max(0, nextExpire - performance.now()) / timeout : 0;
  ctx.fillStyle = '#32d6ff';
  ctx.fillRect(24, 122, 252 * timeLeft, 10);
}
function update() {
  if (!inPlay || gameOver) return;
  if (performance.now() > nextExpire) {
    endRun('Node pulse timed out.');
  }
}
function draw() {
  drawBackground();
  drawChain();
  drawNodes();
  drawHud();
  if (!inPlay || gameOver) {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.fillRect(0, 0, width, height);
  }
}
function animate() {
  update();
  draw();
  requestAnimationFrame(animate);
}
actionButton.addEventListener('click', () => {
  if (!inPlay || gameOver) {
    startRun();
  }
});
resize();
showOverlay('Pulse Relay Forge', 'Keep the pulse chain alive, hit the next relay node fast, and prevent overload.', 'Start Relay');
animate();
