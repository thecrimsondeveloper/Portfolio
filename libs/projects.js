import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.module.js";
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.132.2/examples/jsm/loaders/GLTFLoader.js";

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

  // GLTFLoader setup
  const loader = new GLTFLoader();
  const clickableMeshes = []; // Collect meshes for raycasting
  const models = []; // Store models for animation

  projects.forEach((project, index) => {
    loader.load(
      "./models/BeveledCube.glb", // Path to your .glb model
      (gltf) => {
        const model = gltf.scene;

        // Calculate offset and position
        const xOffset = projects.length / 2;
        model.position.x = index * 2 - xOffset;
        model.position.z = -2;

        // Traverse the model to extract child meshes
        model.traverse((child) => {
          if (child.isMesh) {
            clickableMeshes.push(child); // Add child meshes for raycasting
          }
        });

        // Add model to the scene
        scene.add(model);
        models.push({ model, project });
      },
      undefined,
      (error) => {
        console.error("Error loading model:", error);
      }
    );
  });

  // Add click event listener
  window.addEventListener("click", (event) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // Update raycaster with camera and mouse position
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(clickableMeshes, true); // Intersect all clickable meshes
    if (intersects.length > 0) {
      const clickedMesh = intersects[0].object; // The first intersected mesh
      const clickedProject = models.find(({ model }) =>
        model.children.includes(clickedMesh)
      )?.project;

      if (clickedProject) {
        window.location.href = "projects/" + clickedProject.url;
      }
    }
  });

  // Animate models
  function animateModels() {
    const time = Date.now() * 0.001;
    models.forEach(({ model }) => {
      model.position.y = Math.sin(time) * 0.1;
      model.lookAt(camera.position); // Ensure models always look at the camera
    });

    requestAnimationFrame(animateModels);
  }
  animateModels();
}
