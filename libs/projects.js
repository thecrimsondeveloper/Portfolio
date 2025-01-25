import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";

export const projects = [
  { name: "Pillow", url: "pillow.html" },
  { name: "Cyber Slingers", url: "cyberslingers.html" },
];

export function SetupProjectScene(scene, camera, renderer) {
  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(5, 5, 5);
  scene.add(directionalLight);

  // Raycaster and Mouse
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  // Cube setup
  const geometry = new THREE.BoxGeometry();
  const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
  const cubes = [];

  projects.forEach((project, index) => {
    const cube = new THREE.Mesh(geometry, material);

    let xOffset = projects.length / 2;

    cube.position.x = index * 2 - xOffset;
    cube.position.z = -2;
    scene.add(cube);
    cubes.push(cube);

    // Add click event listener
    window.addEventListener("click", (event) => {
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObject(cube);
      if (intersects.length > 0) {
        window.location.href = "projects/" + project.url;
      }
    });
  });

  // Animate cubes
  function animateCubes() {
    const time = Date.now() * 0.001;
    cubes.forEach((cube, index) => {
      cube.position.y = Math.sin(time + index) * 0.1;
      //make the cube look at the camera
      cube.lookAt(camera.position);
    });

    //make the cube look at the camera

    requestAnimationFrame(animateCubes);
  }
  animateCubes();
}
