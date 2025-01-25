import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";

// Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById("threejs-scene").appendChild(renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5); // Soft light
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5); // Position the light
scene.add(directionalLight);

// Cube setup
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cubes = [];

const projects = [
  { name: "Pillow", url: "pillow.html" },
  { name: "Cyber Slingers", url: "cyberslingers.html" },
];

// Raycaster and Mouse
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

// SetupCube Function
function SetupCube(project, index) {
  const cube = new THREE.Mesh(geometry, material);
  cube.position.x = index * 2; // Space cubes out
  cube.position.z = -2; // Start slightly farther back
  scene.add(cube);
  cubes.push(cube);

  // Add click event listener for the cube
  window.addEventListener("click", (event) => {
    // Calculate mouse position in normalized device coordinates
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // Update raycaster with camera and mouse position
    raycaster.setFromCamera(mouse, camera);

    // Check if this cube is clicked
    const intersects = raycaster.intersectObject(cube);
    if (intersects.length > 0) {
      // Redirect to project URL
      window.location.href = "projects/" + project.url;
    }
  });
}

// Initialize all cubes for projects
projects.forEach((project, index) => {
  SetupCube(project, index);
});

// Camera Position
camera.position.z = 5;

// Mouse Movement Handler for Object Attraction
window.addEventListener("mousemove", (event) => {
  // Calculate mouse position in normalized device coordinates
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
});

// Animation Loop
function animate() {
  requestAnimationFrame(animate);

  // Move cubes toward the mouse position
  cubes.forEach((cube) => {
    // Calculate movement toward the mouse position
    cube.position.x += (mouse.x * 5 - cube.position.x) * 0.05; // Smoothly move on X-axis
    cube.position.y += (mouse.y * 5 - cube.position.y) * 0.05; // Smoothly move on Y-axis
  });

  // Keep camera rotation on X-axis only
  camera.rotation.x += (mouse.y * 0.5 - camera.rotation.x) * 0.1; // Smooth transition

  renderer.render(scene, camera);
}
animate();
