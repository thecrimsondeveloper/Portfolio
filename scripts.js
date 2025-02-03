import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";

// Create Scene, Camera, and Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75, window.innerWidth / window.innerHeight, 0.1, 1000
);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById("threejs-scene").appendChild(renderer.domElement);

// Set Camera Position
camera.position.z = 20;

// Create Starfield
const starGeometry = new THREE.BufferGeometry();
const starCount = 5000;
const starPositions = new Float32Array(starCount * 3);
for (let i = 0; i < starCount * 3; i++) {
  starPositions[i] = (Math.random() - 0.5) * 1000; // Spread stars across a large space
}
starGeometry.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));

const starMaterial = new THREE.PointsMaterial({
  color: 0xffffff,
  size: 0.5,
});

const starField = new THREE.Points(starGeometry, starMaterial);
scene.add(starField);

// Create Boxes
const boxes = [];
const boxGeometry = new THREE.BoxGeometry(2, 2, 2);
const boxMaterial = new THREE.MeshStandardMaterial({
  color: 0xff6600,
  metalness: 0.6,
  roughness: 0.4,
});

const numBoxes = 5; // Number of boxes
for (let i = 0; i < numBoxes; i++) {
  const box = new THREE.Mesh(boxGeometry, boxMaterial);
  box.position.x = (Math.random() - 0.5) * 20;
  box.position.y = (Math.random() - 0.5) * 10;
  box.position.z = (Math.random() - 0.5) * 5;
  scene.add(box);
  boxes.push(box);
}

// Add Light
const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(10, 10, 10);
scene.add(directionalLight);

// Mouse Movement Variables
let mouseX = 0;
let mouseY = 0;
document.addEventListener("mousemove", (event) => {
  mouseX = (event.clientX / window.innerWidth - 0.5) * 2;
  mouseY = (event.clientY / window.innerHeight - 0.5) * 2;
});

// Animate
function animate() {
  requestAnimationFrame(animate);

  // Rotate and float the boxes
  boxes.forEach((box, index) => {
    box.rotation.x += 0.01 + index * 0.001;
    box.rotation.y += 0.01 + index * 0.001;
    box.position.y += Math.sin(Date.now() * 0.001 + index) * 0.01;
  });

  // Rotate the starfield slightly
  starField.rotation.y += 0.0005;

  // Parallax camera effect
  camera.position.x += (mouseX * 5 - camera.position.x) * 0.05;
  camera.position.y += (-mouseY * 5 - camera.position.y) * 0.05;

  renderer.render(scene, camera);
}
animate();

// Handle Window Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
