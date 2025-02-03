// libs/projects.js
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";

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
    requestAnimationFrame(animateGalactic);
  }
  animateGalactic();

  // Create particle text for each project menu option
  const fontLoader = new THREE.FontLoader();
  // Using the helvetiker font from Three.js examples
  fontLoader.load("https://threejs.org/examples/fonts/helvetiker_regular.typeface.json", (font) => {
    const textParticleSystems = [];
    projects.forEach((project, index) => {
      // Create text geometry from the project name
      const textGeometry = new THREE.TextGeometry(project.name, {
        font: font,
        size: 2,
        height: 0.2,
        curveSegments: 12,
        bevelEnabled: false,
      });
      // Center the geometry
      textGeometry.computeBoundingBox();
      if (textGeometry.boundingBox) {
        const centerOffset = -0.5 * (textGeometry.boundingBox.max.x - textGeometry.boundingBox.min.x);
        textGeometry.translate(centerOffset, 0, 0);
      }
      // The TextGeometry in newer Three.js is already a BufferGeometry.
      // Create a Points material to render it as particles.
      const pointsMaterial = new THREE.PointsMaterial({
        color: 0x00ff00,
        size: 0.1,
      });
      const textPoints = new THREE.Points(textGeometry, pointsMaterial);
      // Position each text particle system along the x-axis (spread out) and a fixed z-depth.
      textPoints.position.x = index * 5 - ((projects.length - 1) * 2.5);
      textPoints.position.y = 0;
      textPoints.position.z = -10;
      scene.add(textPoints);
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
      // Check for intersections with any text particle systems
      const intersects = raycaster.intersectObjects(textParticleSystems, true);
      textParticleSystems.forEach((points) => {
        // If the raycaster is over this Points object, enlarge particles and change color
        if (intersects.find(intersect => intersect.object === points)) {
          points.material.color.set(0xff0000);
          points.material.size = 0.2;
        } else {
          points.material.color.set(0x00ff00);
          points.material.size = 0.1;
        }
      });
      requestAnimationFrame(animateText);
    }
    animateText();
  });
}
