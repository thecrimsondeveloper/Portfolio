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

// Project Data
const projects = [
  { name: "Pillow", link: "projects/pillow.html", color: 0xffff00 },
  // Add more projects here if needed
];

// Generate cubes dynamically for each project
const projectCubes = []; // Array to store generated cubes

projects.forEach((project, index) => {
  const geometry = new THREE.BoxGeometry();
  const material = new THREE.MeshBasicMaterial({ color: project.color });
  const cube = new THREE.Mesh(geometry, material);

  // Position cubes dynamically in a row
  cube.position.set(index * 3, 0, 0); // Spread cubes along the X-axis
  cube.userData = { link: project.link }; // Store project link in cube metadata

  scene.add(cube); // Add the cube to the scene
  projectCubes.push(cube); // Add the cube to the array
});

// Animation loop
function animate() {
  requestAnimationFrame(animate);

  // Rotate all cubes
  projectCubes.forEach((cube) => {
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
  });

  renderer.render(scene, camera);
}
animate();

// Handle mouse clicks on cubes
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onMouseClick(event) {
  // Convert mouse position to normalized device coordinates
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  // Raycast to detect intersected objects
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(projectCubes);

  if (intersects.length > 0) {
    const clickedObject = intersects[0].object;

    // Check if the clicked object has a link
    if (clickedObject.userData && clickedObject.userData.link) {
      window.location.href = clickedObject.userData.link; // Navigate to the link
    }
  }
}

window.addEventListener("click", onMouseClick);

// Handle window resizing
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
