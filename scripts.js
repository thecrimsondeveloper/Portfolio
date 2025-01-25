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

// Cube setup
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cubes = [];

const projects = [
  {
    name: "Pillow",
    url: "pillow.html",
  },
  {
    name: "Cyber Slingers",
    url: "cyberslingers.html",
  },
];

// Raycaster and Mouse
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

// SetupCube Function
function SetupCube(project, index, offset) {
  const cube = new THREE.Mesh(geometry, material);
  cube.position.x = index * 2 - offset; // Space cubes out, centered
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

// Calculate the offset to center cubes
const offset = projects.length > 1 ? projects.length - 1 : 0;

// Initialize all cubes for projects
projects.forEach((project, index) => {
  SetupCube(project, index, offset);
});

// Camera Position
camera.position.z = 5;

// Camera look animation variables
let cameraLookAngle = 0;
let lookDirection = 1; // 1 for right, -1 for left

// Animation Loop
function animate() {
  requestAnimationFrame(animate);

  // Rotate each cube
  cubes.forEach((cube) => {
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
  });

  // Subtle camera look left and right
  cameraLookAngle += 0.005 * lookDirection; // Adjust speed if necessary
  if (cameraLookAngle > 0.1 || cameraLookAngle < -0.1) {
    lookDirection *= -1; // Reverse direction at boundaries
  }
  camera.rotation.y = cameraLookAngle; // Update camera rotation

  renderer.render(scene, camera);
}
animate();
