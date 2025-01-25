import * as THREE from "./libs/three.module.js";

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
const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(10, 10, 10);
scene.add(directionalLight);

// Project Data (Only Pillow)
const projects = [
  { name: "Pillow", link: "projects/pillow.html", color: 0xffff00 },
];

// Generate a cube for Pillow
const projectCubes = []; // Store project cubes

projects.forEach((project, index) => {
  const geometry = new THREE.BoxGeometry();
  const material = new THREE.MeshBasicMaterial({ color: project.color });
  const cube = new THREE.Mesh(geometry, material);

  // Position the cube in the center
  cube.position.set(index * 3, 0, 0);
  cube.userData = { link: project.link }; // Link to Pillow project

  scene.add(cube);
  projectCubes.push(cube);
});

// Animation Loop
function animate() {
  requestAnimationFrame(animate);
  projectCubes.forEach((cube) => {
    cube.rotation.x += 0.01; // Rotate along X-axis
    cube.rotation.y += 0.01; // Rotate along Y-axis
  });
  renderer.render(scene, camera);
}
animate();

// Handle Click Events
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

window.addEventListener("click", (event) => {
  // Convert mouse position to normalized device coordinates
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  // Detect intersected objects
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(projectCubes);

  if (intersects.length > 0) {
    const clickedObject = intersects[0].object;
    if (clickedObject.userData && clickedObject.userData.link) {
      window.location.href = clickedObject.userData.link; // Navigate to Pillow
    }
  }
});

// Adjust for Window Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
