import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js';
const canvas = document.getElementById('game');
const overlay = document.getElementById('overlay');
const overlayTitle = document.getElementById('overlay-title');
const overlayCopy = document.getElementById('overlay-copy');
const actionButton = document.getElementById('action');
const hud = document.getElementById('hud');
let renderer, scene, camera, boat, clock;
let laneIndex = 1;
let beacons = [];
let score = 0;
let startTime = 0;
let lastSpawn = 0;
let gameOver = true;
let bonusStage = false;
let pressureWave = false;
const lanes = [-2.4, 0, 2.4];
const colors = { normal: 0x7ce8ff, bonus: 0xffd86c, boat: 0x7cc8ff };
function initScene() {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 50);
  camera.position.set(0, 4.8, 9.5);
  camera.lookAt(0, 0.75, 0);
  const ambient = new THREE.HemisphereLight(0x99aaff, 0x1b2a4a, 1.1);
  const dir = new THREE.DirectionalLight(0xffffff, 0.9);
  dir.position.set(-5, 8, 10);
  scene.add(ambient, dir);
  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 30),
    new THREE.MeshStandardMaterial({ color: 0x06141f, roughness: 0.9, metalness: 0.1 })
  );
  floor.rotation.x = -Math.PI / 2;
  scene.add(floor);
  boat = new THREE.Mesh(
    new THREE.BoxGeometry(1.2, 0.4, 2.4),
    new THREE.MeshStandardMaterial({ color: colors.boat, emissive: 0x1c86ff, metalness: 0.2, roughness: 0.4 })
  );
  boat.position.set(lanes[laneIndex], 0.25, 4.2);
  scene.add(boat);
  const glow = new THREE.PointLight(0x80d9ff, 1.6, 6);
  boat.add(glow);
  clock = new THREE.Clock();
}
function resize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener('resize', resize);
window.addEventListener('keydown', (event) => {
  if (gameOver) return;
  if (event.key === 'ArrowLeft' || event.key.toLowerCase() === 'a') {
    laneIndex = Math.max(0, laneIndex - 1);
    boat.position.x = lanes[laneIndex];
  }
  if (event.key === 'ArrowRight' || event.key.toLowerCase() === 'd') {
    laneIndex = Math.min(2, laneIndex + 1);
    boat.position.x = lanes[laneIndex];
  }
});
function spawnBeacon(time) {
  const lane = lanes[Math.floor(Math.random() * lanes.length)];
  const isBonus = bonusStage || Math.random() < 0.22;
  const material = new THREE.MeshStandardMaterial({ color: isBonus ? colors.bonus : colors.normal, emissive: isBonus ? 0xffb64f : 0x52e7ff, metalness: 0.1, roughness: 0.25 });
  const beacon = new THREE.Mesh(new THREE.TorusGeometry(0.7, 0.18, 16, 32), material);
  beacon.position.set(lane, 1.4, -10);
  beacon.userData = { speed: 8 + (pressureWave ? 3 : 0) + score * 0.03, type: isBonus ? 'bonus' : 'normal' };
  scene.add(beacon);
  beacons.push(beacon);
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
function setHud() {
  const elapsed = Math.floor(clock.getElapsedTime());
  hud.innerHTML = `<div class="hud-row">Score: ${score}</div><div class="hud-row">Time: ${elapsed}s</div><div class="hud-row">${bonusStage ? 'Bonus lane active' : 'Bonus lane locked'}</div>${pressureWave ? '<div class="hud-row">Pressure wave</div>' : ''}`;
}
function endRun(message) {
  gameOver = true;
  showOverlay('Run Complete', `${message} Final score: ${score}`, 'Restart');
}
function update(delta) {
  const elapsed = clock.getElapsedTime();
  if (!gameOver && elapsed > 18) bonusStage = true;
  if (!gameOver && elapsed > 28) pressureWave = true;
  if (!gameOver && elapsed - lastSpawn > 1.15 - Math.min(0.5, elapsed * 0.01)) {
    spawnBeacon(elapsed);
    lastSpawn = elapsed;
  }
  const speedMultiplier = 1 + Math.min(1.2, elapsed * 0.04);
  beacons.forEach((beacon, index) => {
    beacon.position.z += beacon.userData.speed * delta * speedMultiplier;
    if (beacon.position.z > 8) {
      scene.remove(beacon);
      beacons.splice(index, 1);
      return;
    }
    if (beacon.position.distanceTo(boat.position) < 1.1 && Math.abs(beacon.position.x - boat.position.x) < 0.5) {
      if (beacon.userData.type === 'bonus') {
        score += 28;
      } else {
        gameOver = true;
        endRun('You hit a beacon gate.');
      }
      scene.remove(beacon);
      beacons.splice(index, 1);
    }
  });
  setHud();
}
function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();
  if (!gameOver) update(delta);
  renderer.render(scene, camera);
}
function startRun() {
  beacons.forEach((beacon) => scene.remove(beacon));
  beacons = [];
  laneIndex = 1;
  boat.position.x = lanes[laneIndex];
  score = 0;
  gameOver = false;
  bonusStage = false;
  pressureWave = false;
  clock.start();
  lastSpawn = 0;
  hideOverlay();
}
actionButton.addEventListener('click', () => {
  if (gameOver) {
    clock = new THREE.Clock();
    startRun();
  }
});
initScene();
resize();
showOverlay('Aurora Beacon Run', 'Pilot the glow boat through beacon windows. Survive the harbor surge and collect bonus gates.', 'Launch Run');
animate();
