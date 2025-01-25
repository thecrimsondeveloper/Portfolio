import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";

const cameraPanSpeed = 0.1; // Camera panning speed

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

// Initial Mouse Offset
let initialOffsetX = mouse.x; // Initial X offset
let initialOffsetY = mouse.y; // Initial Y offset

// Decay rate for the offset normalization
const offsetDecayRate = 0.02;

// SetupCube Function
function SetupCube(project, index) {
  const cube = new THREE.Mesh(geometry, material);
  cube.position.x = index * 2; // Space cubes out
  cube.position.z = -2; // Fixed Z position
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

// Mouse Movement Handler for Inverse Camera Rotation
let currentCameraRotationY = 0;

window.addEventListener("mousemove", (event) => {
  const mouseX = (event.clientX / window.innerWidth) * 2 - 1;
  const mouseY = -(event.clientY / window.innerHeight) * 2 + 1;

  // Update target rotation values based on mouse position
  currentCameraRotationY = -mouseX * 0.2; // Inverse X-axis rotation
});

// Animation Loop
function animate() {
  requestAnimationFrame(animate);

  // Rotate each cube
  cubes.forEach((cube) => {
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
  });

  // Normalize initial offset toward zero
  if (Math.abs(initialOffsetX) > 0.01 || Math.abs(initialOffsetY) > 0.01) {
    initialOffsetX *= 1 - offsetDecayRate; // Slowly reduce offset
    initialOffsetY *= 1 - offsetDecayRate; // Slowly reduce offset
  } else {
    initialOffsetX = 0; // Snap to zero when small enough
    initialOffsetY = 0; // Snap to zero when small enough
  }

  camera.rotation.y +=
    (currentCameraRotationY + initialOffsetX - camera.rotation.y) *
    cameraPanSpeed;

  renderer.render(scene, camera);
}
animate();
