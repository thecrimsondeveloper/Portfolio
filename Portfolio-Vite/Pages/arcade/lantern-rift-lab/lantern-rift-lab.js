import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js';
const canvas = document.getElementById('game');
const overlay = document.getElementById('overlay');
const overlayTitle = document.getElementById('overlay-title');
const overlayCopy = document.getElementById('overlay-copy');
const actionButton = document.getElementById('action');
const hud = document.getElementById('hud');
let renderer, scene, camera, clock;
let pads = [];
let sequence = [];
let playerIndex = 0;
let revealSpeed = 0.9;
let revealing = false;
let stage = 1;
let score = 0;
let inPlay = false;
const keyMap = { Digit1: 0, Digit2: 1, Digit3: 2, Digit4: 3, q: 0, w: 1, a: 2, s: 3 };
const padColors = [0x5d7cff, 0x8fddff, 0xffde59, 0xff8a6f];
function initScene() {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 30);
  camera.position.set(0, 6, 8);
  camera.lookAt(0, 0, 0);
  const ambient = new THREE.HemisphereLight(0xd0f8ff, 0x0b1630, 1.2);
  scene.add(ambient);
  const floor = new THREE.Mesh(new THREE.CircleGeometry(3.8, 40), new THREE.MeshStandardMaterial({ color: 0x06182d, roughness: 0.8 }));
  floor.rotation.x = -Math.PI / 2;
  scene.add(floor);
  const group = new THREE.Group();
  const radius = 2.4;
  for (let i = 0; i < 4; i++) {
    const angle = (i / 4) * Math.PI * 2;
    const pad = new THREE.Mesh(
      new THREE.SphereGeometry(0.45, 24, 20),
      new THREE.MeshStandardMaterial({ color: padColors[i], emissive: 0x000000, roughness: 0.25, metalness: 0.4 })
    );
    pad.position.set(Math.cos(angle) * radius, 0.45, Math.sin(angle) * radius);
    pad.userData.index = i;
    pad.userData.defaultColor = padColors[i];
    pads.push(pad);
    group.add(pad);
  }
  scene.add(group);
  clock = new THREE.Clock(false);
}
function resize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener('resize', resize);
window.addEventListener('keydown', (event) => {
  if (!inPlay || revealing) return;
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
function resetPads() {
  pads.forEach((pad) => {
    const material = pad.material;
    material.color.setHex(pad.userData.defaultColor);
    material.emissive.setHex(0x000000);
  });
}
function setHud() {
  hud.innerHTML = `<div class="hud-row">Stage: ${stage}</div><div class="hud-row">Score: ${score}</div><div class="hud-row">Sequence length: ${sequence.length}</div><div class="hud-row">Reveal speed: ${revealSpeed.toFixed(2)}s</div>`;
}
function newSequence() {
  sequence.push(Math.floor(Math.random() * 4));
}
function highlightPad(index, intensity = 1) {
  const pad = pads[index];
  pad.material.emissive.setHex(0xffffff);
  pad.material.emissiveIntensity = intensity;
}
function clearHighlight(index) {
  const pad = pads[index];
  pad.material.emissive.setHex(0x000000);
}
async function playSequence() {
  revealing = true;
  playerIndex = 0;
  for (let i = 0; i < sequence.length; i++) {
    const index = sequence[i];
    await new Promise((resolve) => {
      highlightPad(index, 1.5);
      setTimeout(() => {
        clearHighlight(index);
        setTimeout(resolve, 140);
      }, revealSpeed * 500);
    });
  }
  revealing = false;
}
function handleInput(index) {
  const expected = sequence[playerIndex];
  highlightPad(index, 1.2);
  setTimeout(() => clearHighlight(index), 120);
  if (index !== expected) {
    inPlay = false;
    endRun('Pattern broken.');
    return;
  }
  playerIndex += 1;
  if (playerIndex >= sequence.length) {
    score += sequence.length * 12;
    if (score % 36 === 0) {
      stage += 1;
      revealSpeed = Math.max(0.35, revealSpeed - 0.08);
    }
    newSequence();
    setHud();
    playSequence();
  }
}
function endRun(message) {
  showOverlay('Lab Complete', `${message} Final score: ${score}`, 'Restart');
}
function startRun() {
  sequence = [];
  stage = 1;
  score = 0;
  revealSpeed = 0.9;
  inPlay = true;
  resetPads();
  newSequence();
  hideOverlay();
  setHud();
  playSequence();
}
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
actionButton.addEventListener('click', () => {
  if (!inPlay) startRun();
});
initScene();
resize();
showOverlay('Lantern Rift Lab', 'Repeat the glowing lantern sequence. Each stage speeds the reveal and lengthens the pattern.', 'Start Lab');
animate();
