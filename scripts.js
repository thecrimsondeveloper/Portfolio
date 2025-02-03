import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";

// Get all project links from the HTML
const projectLinks = document.querySelectorAll(".project-link");
const numBoxes = projectLinks.length;

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
  starPositions[i] = (Math.random() - 0.5) * 1000;
}
starGeometry.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));
const starMaterial = new THREE.PointsMaterial({
  color: 0xffffff,
  size: 0.5,
});
const starField = new THREE.Points(starGeometry, starMaterial);
scene.add(starField);

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

// Handle Button Animation and Click
projectLinks.forEach((link) => {
  link.addEventListener("mouseover", () => {
    link.classList.add("progressing");
    const animationDuration = parseFloat(getComputedStyle(link).getPropertyValue("--progress-duration")) * 1000;
    setTimeout(() => {
      if (link.classList.contains("progressing")) {
        window.location.href = link.href; // Navigate after animation
      }
    }, animationDuration);
  });

  link.addEventListener("mouseout", () => {
    link.classList.remove("progressing");
  });

  link.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent default navigation
    link.classList.add("clicked");
    window.location.href = link.href; // Navigate on click
  });
});

// Animate Scene
function animate() {
  requestAnimationFrame(animate);

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
