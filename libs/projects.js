// libs/projects.js
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";
import { FontLoader } from "https://cdn.jsdelivr.net/npm/three@0.132.2/examples/jsm/loaders/FontLoader.js";
import { TextGeometry } from "https://cdn.jsdelivr.net/npm/three@0.132.2/examples/jsm/geometries/TextGeometry.js";

export const projects = [
  { name: "Pillow", url: "pillow.html" },
  { name: "Cyber Slingers", url: "cyberslingers.html" },
];


export function SetupProjectScene(scene, camera, renderer) {
  // Create a starfield for a galactic feel
  const starGeometry = new THREE.BufferGeometry();
  const starCount = 10000;
  const starPositions = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount * 3; i++) {
    starPositions[i] = (Math.random() - 0.5) * 2000; // Spread stars over a large volume
  }
  starGeometry.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));
  const starMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 1.5,
    sizeAttenuation: true,
  });
  const stars = new THREE.Points(starGeometry, starMaterial);
  scene.add(stars);
  console.log("Starfield added");

  // Add ambient light
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  // Parallax effect: move camera based on mouse movement
  let mouseX = 0;
  let mouseY = 0;
  const windowHalfX = window.innerWidth / 2;
  const windowHalfY = window.innerHeight / 2;
  document.addEventListener("mousemove", (event) => {
    mouseX = event.clientX - windowHalfX;
    mouseY = event.clientY - windowHalfY;
  });

  function animateGalactic() {
    camera.position.x += (mouseX * 0.001 - camera.position.x) * 0.05;
    camera.position.y += (-mouseY * 0.001 - camera.position.y) * 0.05;
    stars.rotation.y += 0.0005;
    renderer.render(scene, camera); // Ensure renderer is called
    requestAnimationFrame(animateGalactic);
  }
  animateGalactic();

  // Load font for text particles
  const fontLoader = new FontLoader();
  fontLoader.load("https://threejs.org/examples/fonts/helvetiker_regular.typeface.json", (font) => {
    console.log("Font loaded");

    const textParticleSystems = [];
    projects.forEach((project, index) => {
      // Create text geometry from the project name
      const textGeometry = new TextGeometry(project.name, {
        font: font,
        size: 1, // Adjusted size for better visibility
        height: 0.1,
        curveSegments: 10,
        bevelEnabled: false,
      });

      // Center the text
      textGeometry.computeBoundingBox();
      if (textGeometry.boundingBox) {
        const centerOffset = -0.5 * (textGeometry.boundingBox.max.x - textGeometry.boundingBox.min.x);
        textGeometry.translate(centerOffset, 0, 0);
      }

      // Create a Points material to render it as glowing particles
      const pointsMaterial = new THREE.PointsMaterial({
        color: 0x00ff00,
        size: 0.05, // Adjusted for better visibility
        transparent: true,
        opacity: 0.9,
      });

      const textPoints = new THREE.Points(textGeometry, pointsMaterial);

      // Position the text dynamically
      textPoints.position.x = index * 5 - ((projects.length - 1) * 2.5);
      textPoints.position.y = 0;
      textPoints.position.z = 0; // Ensure it's within the view

      scene.add(textPoints);
      console.log(`Text for "${project.name}" added at`, textPoints.position);

      textParticleSystems.push(textPoints);
    });

    // Interaction: when the mouse hovers over a text particle system, change its appearance
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    document.addEventListener("mousemove", (event) => {
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    });

    function animateText() {
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(textParticleSystems, true);
      console.log("Hovered objects:", intersects);

      textParticleSystems.forEach((points) => {
        if (intersects.find(intersect => intersect.object === points)) {
          points.material.color.set(0xff0000);
          points.material.size = 0.1; // Enlarged when hovered
        } else {
          points.material.color.set(0x00ff00);
          points.material.size = 0.05;
        }
      });
      requestAnimationFrame(animateText);
    }
    animateText();
  });
}
