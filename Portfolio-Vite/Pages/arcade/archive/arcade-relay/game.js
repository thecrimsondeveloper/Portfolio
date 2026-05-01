
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
    this.sceneConfig = null;
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
    if (!this.sceneConfig || !this.sceneConfig.camera) {
      this.camera.position.set(0, 8, 18);
      this.camera.lookAt(0, 0, 0);
      return;
    }
    const offset = this.sceneConfig.camera.offset || { x: 0, y: 8, z: 16 };
    this.camera.position.set(offset.x, offset.y, offset.z);
    this.camera.lookAt(0, 0, 0);
  }

  async loadStory() {
    try {
      const response = await fetch('./story-structure.json');
      if (!response.ok) throw new Error('Could not load story-structure.json');
      this.story = await response.json();
      this.sceneConfig = this.story.scene || {};
      document.getElementById('story-text').textContent = JSON.stringify(this.story, null, 2);
    } catch (error) {
      document.getElementById('story-text').textContent = error.message;
      this.sceneConfig = {};
    }
  }

  async initPhysics() {
    await Rapier.init();
    const gravity = new Rapier.Vector3(0.0, -9.81, 0.0);
    const world = new Rapier.World(gravity);
    this.physics = world;

    const groundDesc = Rapier.RigidBodyDesc.fixed();
    const groundBody = world.createRigidBody(groundDesc);
    const halfWidth = (this.sceneConfig.ground?.width || 60) / 2;
    const halfDepth = (this.sceneConfig.ground?.depth || 60) / 2;
    groundBody.createCollider(Rapier.ColliderDesc.cuboid(halfWidth, 0.1, halfDepth));
  }

  buildScene() {
    this.createGround();
    this.createPlayer();
    this.createGoal();
    this.createObstacles();
  }

  createGround() {
    const ground = this.sceneConfig.ground || { width: 60, depth: 60, color: '#121a2a' };
    const material = new THREE.MeshStandardMaterial({ color: new THREE.Color(ground.color) });
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(ground.width, ground.depth), material);
    mesh.rotation.x = -Math.PI / 2;
    this.scene.add(mesh);
  }

  createPlayer() {
    const player = this.sceneConfig.player || { start: { x: 0, y: 0.5, z: 10 }, size: { x: 1, y: 1, z: 1 }, color: '#8bd8ff', speed: 4.0 };
    const material = new THREE.MeshStandardMaterial({ color: new THREE.Color(player.color) });
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(player.size.x, player.size.y, player.size.z), material);
    mesh.position.set(player.start.x, player.start.y, player.start.z);
    this.scene.add(mesh);

    const bodyDesc = Rapier.RigidBodyDesc.dynamic().setTranslation(player.start.x, player.start.y, player.start.z);
    const body = this.physics.createRigidBody(bodyDesc);
    body.createCollider(Rapier.ColliderDesc.cuboid(player.size.x / 2, player.size.y / 2, player.size.z / 2));

    this.player = new GameObject(mesh, body);
    this.objects.push(this.player);
  }

  createGoal() {
    const goal = this.sceneConfig.goal || { position: { x: 0, y: 0.1, z: -12 }, size: { x: 3, y: 0.2, z: 3 }, color: '#6cff8a' };
    const material = new THREE.MeshStandardMaterial({ color: new THREE.Color(goal.color) });
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(goal.size.x, goal.size.y, goal.size.z), material);
    mesh.position.set(goal.position.x, goal.position.y, goal.position.z);
    this.scene.add(mesh);
    this.goal = new GameObject(mesh, null);
  }

  createObstacles() {
    const obstacles = this.sceneConfig.obstacles || [];
    obstacles.forEach((item) => {
      const material = new THREE.MeshStandardMaterial({ color: new THREE.Color(item.color || '#ff8a5c') });
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(item.size.x, item.size.y, item.size.z), material);
      const position = item.position || { x: 0, y: item.size.y / 2, z: 0 };
      mesh.position.set(position.x, position.y, position.z);
      this.scene.add(mesh);

      const bodyDesc = Rapier.RigidBodyDesc.fixed().setTranslation(position.x, position.y, position.z);
      const body = this.physics.createRigidBody(bodyDesc);
      body.createCollider(Rapier.ColliderDesc.cuboid(item.size.x / 2, item.size.y / 2, item.size.z / 2));
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
    const speed = this.sceneConfig.player?.speed || 4.0;
    if (this.input.keys.forward) direction.z -= speed;
    if (this.input.keys.backward) direction.z += speed;
    if (this.input.keys.left) direction.x -= speed;
    if (this.input.keys.right) direction.x += speed;
    this.player.body.setLinvel(direction, true);
  }

  updateUI() {
    if (!this.player) return;
    const goalText = this.sceneConfig.rules?.statusMessage || 'Use WASD / arrows to move.';
    this.status.textContent = `${goalText} Position: ${this.player.mesh.position.x.toFixed(1)}, ${this.player.mesh.position.z.toFixed(1)}`;
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    this.updatePlayer();
    this.updatePhysics();
    this.updateUI();
    if (this.player) {
      this.camera.position.x = this.player.mesh.position.x;
      this.camera.position.z = this.player.mesh.position.z + (this.sceneConfig.camera?.offset?.z || 16);
      this.camera.lookAt(this.player.mesh.position);
    }
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
