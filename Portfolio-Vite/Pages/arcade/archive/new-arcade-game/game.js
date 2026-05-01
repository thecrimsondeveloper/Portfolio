
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js';

const canvas = document.getElementById('game-canvas');
const status = document.getElementById('game-status');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 200);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

const ambient = new THREE.HemisphereLight(0x99bbff, 0x222233, 1.2);
scene.add(ambient);
const dirLight = new THREE.DirectionalLight(0xd3e9ff, 1.1);
dirLight.position.set(5, 10, 5);
scene.add(dirLight);

const player = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({ color: 0x8bd8ff }));
scene.add(player);

const environment = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshStandardMaterial({ color: 0x121a2a }));
environment.rotation.x = -Math.PI / 2;
scene.add(environment);

const gate = new THREE.Mesh(new THREE.BoxGeometry(2, 3, 0.4), new THREE.MeshStandardMaterial({ color: 0xff8a5c }));
gate.position.set(0, 1.5, -12);
scene.add(gate);

const goal = new THREE.Mesh(new THREE.BoxGeometry(3, 0.2, 3), new THREE.MeshStandardMaterial({ color: 0x6cff8a }));
goal.position.set(0, 0.1, -18);
scene.add(goal);

player.position.set(0, 0.5, 8);
camera.position.set(0, 5, 15);
camera.lookAt(player.position);

const keys = { forward: false, backward: false, left: false, right: false };
window.addEventListener('keydown', (event) => {
  if (['w','ArrowUp'].includes(event.key)) keys.forward = true;
  if (['s','ArrowDown'].includes(event.key)) keys.backward = true;
  if (['a','ArrowLeft'].includes(event.key)) keys.left = true;
  if (['d','ArrowRight'].includes(event.key)) keys.right = true;
});
window.addEventListener('keyup', (event) => {
  if (['w','ArrowUp'].includes(event.key)) keys.forward = false;
  if (['s','ArrowDown'].includes(event.key)) keys.backward = false;
  if (['a','ArrowLeft'].includes(event.key)) keys.left = false;
  if (['d','ArrowRight'].includes(event.key)) keys.right = false;
});

let score = 0;
let finished = false;
const targetZ = -18;

function updatePlayer() {
  const speed = 0.18;
  if (keys.forward) player.position.z -= speed;
  if (keys.backward) player.position.z += speed;
  if (keys.left) player.position.x -= speed;
  if (keys.right) player.position.x += speed;
  player.position.x = Math.max(-18, Math.min(18, player.position.x));
  player.position.z = Math.max(-18, Math.min(18, player.position.z));

  if (!finished && player.position.distanceTo(goal.position) < 1.5) {
    finished = true;
    status.textContent = 'Level complete! You reached the goal.';
  } else if (!finished) {
    status.textContent = `Move to the green goal. X: ${player.position.x.toFixed(1)}, Z: ${player.position.z.toFixed(1)}`;
  }
}

function animate() {
  requestAnimationFrame(animate);
  updatePlayer();
  camera.position.x = player.position.x;
  camera.position.z = player.position.z + 12;
  camera.lookAt(player.position);
  renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

async function loadStory() {
  try {
    const response = await fetch('./story-structure.json');
    if (!response.ok) throw new Error('Could not load story-structure.json');
    const story = await response.json();
    document.getElementById('story-text').textContent = JSON.stringify(story, null, 2);
  } catch (error) {
    document.getElementById('story-text').textContent = error.message;
  }
}

async function initPhysics() {
  await Rapier.init();
  const gravity = new Rapier.Vector3(0.0, -9.81, 0.0);
  const world = new Rapier.World(gravity);

  const groundDesc = Rapier.RigidBodyDesc.fixed();
  const groundBody = world.createRigidBody(groundDesc);
  groundBody.createCollider(Rapier.ColliderDesc.cuboid(20, 0.1, 20));

  const playerBodyDesc = Rapier.RigidBodyDesc.dynamic().setTranslation(0.0, 1.0, 8.0);
  const playerBody = world.createRigidBody(playerBodyDesc);
  playerBody.createCollider(Rapier.ColliderDesc.cuboid(0.5, 0.5, 0.5));

  return { world, playerBody };
}

let physics = null;
let playerBody = null;

async function start() {
  const result = await initPhysics();
  physics = result.world;
  playerBody = result.playerBody;
  loadStory();
  animate();
}

function updatePlayer() {
  if (!playerBody) return;
  const velocity = new Rapier.Vector3(0, 0, 0);
  const speed = 4.0;
  if (keys.forward) velocity.z -= speed;
  if (keys.backward) velocity.z += speed;
  if (keys.left) velocity.x -= speed;
  if (keys.right) velocity.x += speed;
  playerBody.setLinvel(velocity, true);
  physics.step();
  const translation = playerBody.translation();
  player.position.set(translation.x, translation.y - 0.5, translation.z);

  if (!finished && player.position.distanceTo(goal.position) < 1.5) {
    finished = true;
    status.textContent = 'Level complete! You reached the goal.';
  } else if (!finished) {
    status.textContent = `Move to the green goal. X: ${player.position.x.toFixed(1)}, Z: ${player.position.z.toFixed(1)}`;
  }
}

function animate() {
  requestAnimationFrame(animate);
  updatePlayer();
  camera.position.x = player.position.x;
  camera.position.z = player.position.z + 12;
  camera.lookAt(player.position);
  renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

start();
