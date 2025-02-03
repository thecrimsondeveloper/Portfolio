import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";

// Create Scene, Camera, and Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
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

// Create Boxes with Random Colors
const boxes = [];
const boxGeometry = new THREE.BoxGeometry(2, 2, 2);
const numBoxes = 5; // Number of boxes
for (let i = 0; i < numBoxes; i++) {
  const boxMaterial = new THREE.MeshStandardMaterial({
    color: Math.random() * 0xffffff, // Random color for each box
    metalness: 0.6,
    roughness: 0.4,
  });
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

// Raycaster for Box Hover Effects
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
document.addEventListener("mousemove", (event) => {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
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

  // Highlight boxes on hover
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(boxes);
  boxes.forEach((box) => {
    box.material.color.set(0xff6600); // Reset color
  });
  if (intersects.length > 0) {
    intersects[0].object.material.color.set(0x00ff00); // Highlight hovered box
  }

  // Rotate the starfield slightly
  starField.rotation.y += 0.0005;

  // Parallax camera effect
  const easeFactor = 0.05;
  camera.position.x += (mouseX * 5 - camera.position.x) * easeFactor;
  camera.position.y += (-mouseY * 5 - camera.position.y) * easeFactor;

  renderer.render(scene, camera);
}
animate();

// Handle Window Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Add Interaction Instructions
const instructions = document.createElement("div");
instructions.style.position = "absolute";
instructions.style.top = "20px";
instructions.style.left = "50%";
instructions.style.transform = "translateX(-50%)";
instructions.style.color = "white";
instructions.style.fontFamily = "Arial, sans-serif";
instructions.style.fontSize = "1.2em";
instructions.style.textAlign = "center";
instructions.textContent = "Move your mouse to interact with the floating boxes!";
document.body.appendChild(instructions);
