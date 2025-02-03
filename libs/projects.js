// libs/projects.js
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";

export function SetupProjectScene(scene, camera, renderer) {
  // Create a starfield for a galactic feel
  const starGeometry = new THREE.BufferGeometry();
  const starCount = 10000;
  const starPositions = new Float32Array(starCount * 3);

  for (let i = 0; i < starCount * 3; i++) {
    // Spread stars across a large volume
    starPositions[i] = (Math.random() - 0.5) * 2000;
  }
  starGeometry.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));

  const starMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 1.5,
    sizeAttenuation: true,
  });

  const stars = new THREE.Points(starGeometry, starMaterial);
  scene.add(stars);

  // Add subtle ambient lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  // Parallax effect: shift the camera slightly based on mouse movement
  let mouseX = 0;
  let mouseY = 0;
  const windowHalfX = window.innerWidth / 2;
  const windowHalfY = window.innerHeight / 2;

  document.addEventListener("mousemove", (event) => {
    mouseX = event.clientX - windowHalfX;
    mouseY = event.clientY - windowHalfY;
  });

  function animateGalactic() {
    // Smoothly adjust camera position based on mouse movement
    camera.position.x += (mouseX * 0.001 - camera.position.x) * 0.05;
    camera.position.y += (-mouseY * 0.001 - camera.position.y) * 0.05;

    // Slowly rotate the starfield for a dynamic space-travel feel
    stars.rotation.y += 0.0005;

    requestAnimationFrame(animateGalactic);
  }
  animateGalactic();
}
