import * as THREE from "three";

// Create Scene, Camera, and Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75, window.innerWidth / window.innerHeight, 0.1, 1000
);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById("threejs-scene").appendChild(renderer.domElement);

// Set Camera Position
camera.position.z = 10;

// Parallax effect variables
let mouseX = 0;
let mouseY = 0;
document.addEventListener("mousemove", (event) => {
  mouseX = (event.clientX / window.innerWidth - 0.5) * 2;
  mouseY = (event.clientY / window.innerHeight - 0.5) * 2;
});

// Create Floating Text
const fontLoader = new THREE.FontLoader();
fontLoader.load("https://threejs.org/examples/fonts/helvetiker_regular.typeface.json", (font) => {
  const projectNames = [
    { name: "Pillow", url: "projects/pillow.html" },
    { name: "Cyber Slingers", url: "projects/cyberslingers.html" }
  ];

  projectNames.forEach((project, index) => {
    const textGeometry = new THREE.TextGeometry(project.name, {
      font: font,
      size: 2,
      height: 0.1,
      curveSegments: 12,
    });

    textGeometry.computeBoundingBox();
    const textMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const textMesh = new THREE.Mesh(textGeometry, textMaterial);

    // Position text dynamically
    textMesh.position.x = index * 6 - ((projectNames.length - 1) * 3);
    textMesh.position.y = 0;
    textMesh.position.z = 0;

    scene.add(textMesh);
  });

  animate();
});

// Animate the scene
function animate() {
  requestAnimationFrame(animate);

  // Smooth camera parallax effect
  camera.position.x += (mouseX * 2 - camera.position.x) * 0.05;
  camera.position.y += (-mouseY * 2 - camera.position.y) * 0.05;
  
  renderer.render(scene, camera);
}

// Handle Window Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
