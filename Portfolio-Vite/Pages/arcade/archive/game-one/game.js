
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js';

class InputManager {
  constructor() {
    this.keys = { forward: false, backward: false, left: false, right: false };
    window.addEventListener('keydown', (event) => this.onKeyDown(event));
    window.addEventListener('keyup', (event) => this.onKeyUp(event));
  }

  onKeyDown(event) {
    if (['w', 'ArrowUp'].includes(event.key)) this.keys.forward = true;
    if (['s', 'ArrowDown'].includes(event.key)) this.keys.backward = true;
    if (['a', 'ArrowLeft'].includes(event.key)) this.keys.left = true;
    if (['d', 'ArrowRight'].includes(event.key)) this.keys.right = true;
  }

  onKeyUp(event) {
    if (['w', 'ArrowUp'].includes(event.key)) this.keys.forward = false;
    if (['s', 'ArrowDown'].includes(event.key)) this.keys.backward = false;
    if (['a', 'ArrowLeft'].includes(event.key)) this.keys.left = false;
    if (['d', 'ArrowRight'].includes(event.key)) this.keys.right = false;
  }
}

class GameObject {
  constructor(mesh, body = null) {
    this.mesh = mesh;
    this.body = body;
  }

  syncFromPhysics() {
    if (this.body) {
      const translation = this.body.translation();
      this.mesh.position.set(translation.x, translation.y, translation.z);
    }
  }
}

class Game {
  constructor() {
    this.canvas = document.getElementById('game-canvas');
    this.status = document.getElementById('game-status');
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 200);
    this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.input = new InputManager();
    this.objects = [];
    this.physics = null;
    this.player = null;
    this.goal = null;
    this.story = null;
  }

  async init() {
    this.setupLighting();
    this.setupCamera();
    await this.loadStory();
    await this.initPhysics();
    this.buildScene();
    this.onResize();
    window.addEventListener('resize', () => this.onResize());
    this.animate();
  }

  setupLighting() {
    const ambient = new THREE.HemisphereLight(0x99bbff, 0x222233, 1.2);
    this.scene.add(ambient);
    const dirLight = new THREE.DirectionalLight(0xd3e9ff, 1.1);
    dirLight.position.set(5, 10, 5);
    this.scene.add(dirLight);
  }

  setupCamera() {
    this.camera.position.set(0, 8, 18);
    this.camera.lookAt(0, 0, 0);
  }

  async loadStory() {
    try {
      const response = await fetch('./story-structure.json');
      if (!response.ok) throw new Error('Could not load story-structure.json');
      this.story = await response.json();
      document.getElementById('story-text').textContent = JSON.stringify(this.story, null, 2);
    } catch (error) {
      document.getElementById('story-text').textContent = error.message;
    }
  }

  async initPhysics() {
    await Rapier.init();
    const gravity = new Rapier.Vector3(0.0, -9.81, 0.0);
    const world = new Rapier.World(gravity);
    this.physics = world;

    const groundDesc = Rapier.RigidBodyDesc.fixed();
    const groundBody = world.createRigidBody(groundDesc);
    groundBody.createCollider(Rapier.ColliderDesc.cuboid(30, 0.1, 30));
  }

  buildScene() {
    this.createGround();
    this.createPlayer();
    this.createGoal();
    this.createObstacles();
  }

  createGround() {
    const material = new THREE.MeshStandardMaterial({ color: 0x121a2a });
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), material);
    mesh.rotation.x = -Math.PI / 2;
    this.scene.add(mesh);
  }

  createPlayer() {
    const material = new THREE.MeshStandardMaterial({ color: 0x8bd8ff });
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), material);
    mesh.position.set(0, 0.5, 10);
    this.scene.add(mesh);

    const bodyDesc = Rapier.RigidBodyDesc.dynamic().setTranslation(0, 0.5, 10);
    const body = this.physics.createRigidBody(bodyDesc);
    body.createCollider(Rapier.ColliderDesc.cuboid(0.5, 0.5, 0.5));

    this.player = new GameObject(mesh, body);
    this.objects.push(this.player);
  }

  createGoal() {
    const material = new THREE.MeshStandardMaterial({ color: 0x6cff8a });
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(3, 0.2, 3), material);
    mesh.position.set(0, 0.1, -12);
    this.scene.add(mesh);
    this.goal = new GameObject(mesh, null);
  }

  createObstacles() {
    const obstacles = [
      { x: -6, z: -2 },
      { x: 6, z: -6 },
      { x: 0, z: -8 },
    ];

    obstacles.forEach((pos) => {
      const material = new THREE.MeshStandardMaterial({ color: 0xff8a5c });
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(3, 2, 3), material);
      mesh.position.set(pos.x, 1, pos.z);
      this.scene.add(mesh);

      const bodyDesc = Rapier.RigidBodyDesc.fixed().setTranslation(pos.x, 1, pos.z);
      const body = this.physics.createRigidBody(bodyDesc);
      body.createCollider(Rapier.ColliderDesc.cuboid(1.5, 1, 1.5));
      this.objects.push(new GameObject(mesh, body));
    });
  }

  updatePhysics() {
    this.physics.step();
    this.objects.forEach((object) => object.syncFromPhysics());
  }

  updatePlayer() {
    if (!this.player || !this.player.body) return;
    const direction = new Rapier.Vector3(0, 0, 0);
    const speed = 4.0;
    if (this.input.keys.forward) direction.z -= speed;
    if (this.input.keys.backward) direction.z += speed;
    if (this.input.keys.left) direction.x -= speed;
    if (this.input.keys.right) direction.x += speed;
    this.player.body.setLinvel(direction, true);
  }

  updateUI() {
    this.status.textContent = `Use WASD / arrows to move. Position: ${this.player.mesh.position.x.toFixed(1)}, ${this.player.mesh.position.z.toFixed(1)}`;
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    this.updatePlayer();
    this.updatePhysics();
    this.updateUI();
    this.camera.position.x = this.player.mesh.position.x;
    this.camera.position.z = this.player.mesh.position.z + 16;
    this.camera.lookAt(this.player.mesh.position);
    this.renderer.render(this.scene, this.camera);
  }

  onResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }
}

const game = new Game();
game.init();
