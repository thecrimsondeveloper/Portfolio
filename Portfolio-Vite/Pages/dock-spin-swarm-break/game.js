
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js';

const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
const dampFactor = (delta, sharpness) => 1 - Math.exp(-delta * sharpness);

class InputManager {
  constructor() {
	this.keys = { forward: false, backward: false, left: false, right: false };
	this.surgeRequested = false;
	window.addEventListener('keydown', (event) => this.onKeyDown(event));
	window.addEventListener('keyup', (event) => this.onKeyUp(event));
  }

  onKeyDown(event) {
	const key = event.key.toLowerCase();
	if (['w', 'arrowup'].includes(key)) this.keys.forward = true;
	if (['s', 'arrowdown'].includes(key)) this.keys.backward = true;
	if (['a', 'arrowleft'].includes(key)) this.keys.left = true;
	if (['d', 'arrowright'].includes(key)) this.keys.right = true;
	if (key === ' ' && !event.repeat) {
	  this.surgeRequested = true;
	  event.preventDefault();
	}
  }

  onKeyUp(event) {
	const key = event.key.toLowerCase();
	if (['w', 'arrowup'].includes(key)) this.keys.forward = false;
	if (['s', 'arrowdown'].includes(key)) this.keys.backward = false;
	if (['a', 'arrowleft'].includes(key)) this.keys.left = false;
	if (['d', 'arrowright'].includes(key)) this.keys.right = false;
  }

  consumeSurge() {
	const requested = this.surgeRequested;
	this.surgeRequested = false;
	return requested;
  }
}

class ArenaGame {
  constructor() {
	this.canvas = document.getElementById('game-canvas');
	this.status = document.getElementById('game-status');
	this.metrics = document.getElementById('game-metrics');
	this.objective = document.getElementById('game-objective');
	this.storyText = document.getElementById('story-text');
	this.overlay = document.getElementById('game-overlay');
	this.overlayTitle = document.getElementById('overlay-title');
	this.overlayBody = document.getElementById('overlay-body');
	this.overlayHint = document.getElementById('overlay-hint');
	this.scene = new THREE.Scene();
	this.camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 220);
	this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true });
	this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
	this.renderer.outputColorSpace = THREE.SRGBColorSpace;
	this.renderer.shadowMap.enabled = true;
	this.clock = new THREE.Clock();
	this.input = new InputManager();
	this.story = null;
	this.config = null;
	this.elapsed = 0;
	this.state = 'loading';
	this.player = null;
	this.goal = null;
	this.disks = [];
	this.activeDiskIndex = 0;
	this.relics = [];
	this.enemies = [];
	this.hazards = [];
	this.rain = null;
	this.timeRemaining = 0;
	this.relicCount = 0;
	this.goalUnlocked = false;
	this.eventMessage = '';
	this.eventTimer = 0;
	this.template = 'boss_rush';
	this.score = 0;
	this.airborne = false;
	this.jumpVelocity = 0;
  }

  async init() {
	await this.loadStory();
	this.applyVisualTheme();
	this.createArena();
	this.createPlayer();
	this.createGoal();
	this.createRelics();
	this.createEnemies();
	this.createRain();
	this.resetRun();
	this.showIntroOverlay();
	this.onResize();
	window.addEventListener('resize', () => this.onResize());
	window.addEventListener('keydown', (event) => {
	  const key = event.key.toLowerCase();
	  if (key === 'enter' && this.state === 'menu') {
		this.startRun();
	  }
	  if (key === 'r' && this.state !== 'running') {
		this.resetRun();
	  }
	});
	this.animate();
  }

  async loadStory() {
	const response = await fetch('./story-structure.json');
	if (!response.ok) {
	  throw new Error('Could not load story-structure.json');
	}
		this.story = await response.json();
		this.config = this.story.scene;
		this.template = this.config?.rules?.runtimeTemplate || this.story?.gameDesignProfile?.runtimeTemplate || 'arena_survival';
		const pitch = this.story?.brainstorm?.oneLinePitch || this.story?.hook || 'Arcade run loaded.';
	const coreLoop = this.story?.brainstorm?.finalSpec?.coreLoop || [];
	this.overlayTitle.textContent = this.story?.title || 'Arcade Run';
	this.overlayBody.textContent = this.story?.description || pitch;
	this.storyText.textContent = [pitch, '', ...coreLoop.slice(0, 3)].join('\n');
	this.objective.textContent = this.story.objective || pitch;
	if (this.overlayHint) {
	  this.overlayHint.textContent = 'Press Enter to deploy. WASD to move, Space to Surge (dash + pulse). Reach the final beacon to extract. Press R to restart.';
	}
  }

  showIntroOverlay() {
	this.state = 'menu';
	this.overlay.classList.add('visible');
  }

  startRun() {
	this.overlay.classList.remove('visible');
	this.state = 'running';
	this.setStatus('Boss Rush Mode — Reach the Beacon.', 2.2);
  }

  applyVisualTheme() {
	const arena = this.config.arena;
	this.scene.background = new THREE.Color(arena.skyColor || '#050813');
	this.scene.fog = new THREE.Fog(arena.fogColor || '#091120', 24, 92);

	const hemi = new THREE.HemisphereLight(0x93cfff, 0x071120, 1.15);
	this.scene.add(hemi);

	const keyLight = new THREE.DirectionalLight(0xe6fbff, 1.4);
	keyLight.position.set(14, 24, 12);
	keyLight.castShadow = true;
	keyLight.shadow.mapSize.set(2048, 2048);
	this.scene.add(keyLight);
  }

  createArena() {
	const diskCount = 8;
	const diskRadius = 14;
	const gap = 12;
	
	for (let i = 0; i < diskCount; i++) {
	  const diskGroup = new THREE.Group();
	  const posZ = i * -(diskRadius * 2 + gap);
	  diskGroup.position.set(0, 0, posZ);
	  
	  // Create wedges for the disk
	  const wedgeCount = 12;
	  const wedges = [];
	  for (let j = 0; j < wedgeCount; j++) {
		const startAngle = (j / wedgeCount) * Math.PI * 2;
		const endAngle = ((j + 1) / wedgeCount) * Math.PI * 2;
		const wedgeGeo = new THREE.Shape();
		wedgeGeo.moveTo(0, 0);
		wedgeGeo.absarc(0, 0, diskRadius, startAngle, endAngle, false);
		wedgeGeo.lineTo(0, 0);
		
		const geometry = new THREE.ShapeGeometry(wedgeGeo);
		const material = new THREE.MeshStandardMaterial({ 
		  color: i % 3 === 0 ? 0x1a2a3a : 0x0a1a2a,
		  emissive: 0x00ffff,
		  emissiveIntensity: 0.05,
		  metalness: 0.8,
		  roughness: 0.2,
		  side: THREE.DoubleSide
		});
		
		const mesh = new THREE.Mesh(geometry, material);
		mesh.rotation.x = -Math.PI / 2;
		mesh.receiveShadow = true;
		diskGroup.add(mesh);
		wedges.push({ 
		  mesh, 
		  state: 'idle', 
		  timer: 0,
		  originalColor: material.color.clone() 
		});
	  }
	  
	  this.scene.add(diskGroup);
	  this.disks.push({ group: diskGroup, wedges, radius: diskRadius, index: i });
	}

	// Skybox and Fog
	this.scene.background = new THREE.Color(0x020408);
	this.scene.fog = new THREE.FogExp2(0x050810, 0.012);

	const coreLight = new THREE.PointLight(0x00ffff, 500, 300);
	coreLight.position.set(0, 50, -100);
	this.scene.add(coreLight);
  }

  createPlayer() {
	const playerConfig = this.config.player;
	const group = new THREE.Group();
	const body = new THREE.Mesh(
	  new THREE.IcosahedronGeometry(playerConfig.radius, 3),
	  new THREE.MeshStandardMaterial({ color: playerConfig.color, emissive: 0x164865, emissiveIntensity: 0.4, roughness: 0.25 })
	);
	body.castShadow = true;
	group.add(body);

	const ring = new THREE.Mesh(
	  new THREE.TorusGeometry(playerConfig.radius + 0.26, 0.08, 12, 32),
	  new THREE.MeshBasicMaterial({ color: 0x7df9ff, transparent: true, opacity: 0.65 })
	);
	ring.rotation.x = Math.PI / 2;
	ring.position.y = -playerConfig.radius * 0.5;
	group.add(ring);

	group.position.set(playerConfig.start.x, playerConfig.start.y, playerConfig.start.z);
	this.scene.add(group);
	this.player = {
	  mesh: group,
	  body,
	  ring,
	  radius: playerConfig.radius,
	  velocity: new THREE.Vector3(),
	  surgeCooldown: 0,
	  invulnerability: 0,
	  maxHealth: playerConfig.maxHealth,
	  health: playerConfig.maxHealth,
	  verticalVelocity: 0,
	  isJumping: false
	};
  }

  createGoal() {
	const lastDisk = this.disks[this.disks.length - 1];
	const group = new THREE.Group();
	const ring = new THREE.Mesh(
	  new THREE.TorusGeometry(3.5, 0.4, 16, 40),
	  new THREE.MeshStandardMaterial({ color: 0x00ffff, emissive: 0x004444, emissiveIntensity: 1.0 })
	);
	ring.rotation.x = Math.PI / 2;
	group.add(ring);

	const beacon = new THREE.Mesh(
	  new THREE.CylinderGeometry(0.5, 0.5, 12, 12),
	  new THREE.MeshStandardMaterial({ color: 0x00ffff, emissive: 0x00ffff, emissiveIntensity: 2.0, transparent: true, opacity: 0.6 })
	);
	beacon.position.y = 6;
	group.add(beacon);

	group.position.copy(lastDisk.group.position);
	group.position.y = 0.1;
	this.scene.add(group);
	this.goal = { mesh: group, ring, beacon, radius: 4 };
  }

  createRelics() {
	this.relics = [];
	this.disks.forEach((disk, dIdx) => {
	  if (dIdx === 0) return;
	  for (let i = 0; i < 2; i++) {
		const angle = Math.random() * Math.PI * 2;
		const r = Math.random() * disk.radius * 0.7;
		const mesh = new THREE.Mesh(
		  new THREE.OctahedronGeometry(0.8, 0),
		  new THREE.MeshStandardMaterial({ color: 0x00ffff, emissive: 0x008888, emissiveIntensity: 0.8, roughness: 0.1 })
		);
		const pos = new THREE.Vector3(Math.cos(angle) * r, 1.2, Math.sin(angle) * r).add(disk.group.position);
		mesh.position.copy(pos);
		mesh.castShadow = true;
		this.scene.add(mesh);
		this.relics.push({ mesh, baseY: 1.2, collected: false, diskIndex: dIdx });
	  }
	});
  }

  createHazards() {
	this.hazards = this.config.hazards.map((config) => {
	  const mesh = new THREE.Mesh(
		new THREE.CylinderGeometry(config.radius, config.radius, 0.14, 32),
		new THREE.MeshBasicMaterial({ color: config.color, transparent: true, opacity: 0.22 })
	  );
	  mesh.position.set(config.position.x, config.position.y, config.position.z);
	  this.scene.add(mesh);
	  const outline = new THREE.Mesh(
		new THREE.TorusGeometry(config.radius, 0.08, 12, 32),
		new THREE.MeshBasicMaterial({ color: config.color, transparent: true, opacity: 0.42 })
	  );
	  outline.rotation.x = Math.PI / 2;
	  outline.position.copy(mesh.position);
	  outline.position.y += 0.08;
	  this.scene.add(outline);
	  return { ...config, mesh, outline };
	});
  }

  createEnemies() {
	this.enemies = [];
	this.disks.forEach((disk, dIdx) => {
	  if (dIdx === 0) return;
	  const enemyCount = dIdx % 3 === 0 ? 3 : 1;
	  for (let i = 0; i < enemyCount; i++) {
		const group = new THREE.Group();
		const body = new THREE.Mesh(
		  new THREE.DodecahedronGeometry(0.9, 0),
		  new THREE.MeshStandardMaterial({ color: 0xff0055, emissive: 0x440000, emissiveIntensity: 0.5, roughness: 0.3 })
		);
		body.castShadow = true;
		group.add(body);
		
		const angle = Math.random() * Math.PI * 2;
		const r = disk.radius * 0.5;
		const pos = new THREE.Vector3(Math.cos(angle) * r, 0.9, Math.sin(angle) * r).add(disk.group.position);
		group.position.copy(pos);
		this.scene.add(group);
		
		this.enemies.push({
		  mesh: group,
		  name: 'Swarm Unit',
		  speed: 1.2 + dIdx * 0.1,
		  radius: 0.9,
		  pursuitRange: 18,
		  diskIndex: dIdx,
		  anchor: pos.clone(),
		  velocity: new THREE.Vector3(),
		  stun: 0,
		  hitCooldown: 0,
		  phase: Math.random() * 10
		});
	  }
	});
  }

  createRain() {
	const density = this.config.weather?.rainDensity || 220;
	const positions = new Float32Array(density * 3);
	const halfWidth = this.config.arena.width * 0.5;
	const halfDepth = this.config.arena.depth * 0.5;
	for (let index = 0; index < density; index += 1) {
	  positions[index * 3] = (Math.random() - 0.5) * this.config.arena.width;
	  positions[index * 3 + 1] = Math.random() * 18 + 3;
	  positions[index * 3 + 2] = (Math.random() - 0.5) * this.config.arena.depth;
	}
	const geometry = new THREE.BufferGeometry();
	geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
	const material = new THREE.PointsMaterial({ color: 0x8bd8ff, size: 0.12, transparent: true, opacity: 0.75 });
	this.rain = {
	  points: new THREE.Points(geometry, material),
	  halfWidth,
	  halfDepth,
	};
	this.scene.add(this.rain.points);
  }

  resetRun() {
	this.player.mesh.position.set(0, 0, 0);
	this.player.velocity.set(0, 0, 0);
	this.player.verticalVelocity = 0;
	this.player.isJumping = false;
	this.player.health = this.player.maxHealth;
	this.player.surgeCooldown = 0;
	this.player.invulnerability = 0;
	this.activeDiskIndex = 0;
	this.goalUnlocked = false;
	this.relicCount = 0;
	this.score = 0;
	this.timeRemaining = 120;
	this.state = 'running';
	this.elapsed = 0;
	this.overlay.classList.remove('visible');
	this.setStatus('Rush initiated. Reach the beacon.', 2.2);
	
	this.relics.forEach((relic) => {
	  relic.collected = false;
	  relic.mesh.visible = true;
	});

	this.enemies.forEach((enemy) => {
	  enemy.mesh.position.copy(enemy.anchor);
	  enemy.velocity.set(0, 0, 0);
	  enemy.stun = 0;
	  enemy.hitCooldown = 0;
	});
	this.updateHud(0);
  }

  setStatus(message, ttl = 1.2) {
	this.eventMessage = message;
	this.eventTimer = ttl;
  }

  finishRun(title, body) {
	this.state = 'complete';
	this.overlayTitle.textContent = title;
	this.overlayBody.textContent = body;
	if (this.overlayHint) {
	  this.overlayHint.textContent = 'Press R to restart the run.';
	}
	this.overlay.classList.add('visible');
  }

  applyDamage(amount, reason) {
	if (this.player.invulnerability > 0 || this.state !== 'running') return;
	this.player.health = Math.max(0, this.player.health - amount);
	this.player.invulnerability = 0.7;
	this.setStatus(reason, 0.8);
	if (this.player.health <= 0) {
	  this.finishRun('Route Interrupted', 'The route collapsed under pressure. Press R to run it again.');
	}
  }

  triggerPulse() {
	const radius = this.config.player.pulseRadius || 8;
	this.player.ring.scale.setScalar(1.7);
	this.enemies.forEach((enemy) => {
	  const offset = enemy.mesh.position.clone().sub(this.player.mesh.position);
	  offset.y = 0;
	  const distance = offset.length();
	  if (distance < radius) {
		const direction = offset.normalize();
		enemy.velocity.add(direction.multiplyScalar(9));
		enemy.stun = 1.3;
	  }
	});
	this.setStatus('Pulse burst!', 1.0);
  }

  updatePlayer(delta) {
	const move = new THREE.Vector3(
	  (this.input.keys.right ? 1 : 0) - (this.input.keys.left ? 1 : 0),
	  0,
	  (this.input.keys.backward ? 1 : 0) - (this.input.keys.forward ? 1 : 0)
	);
	if (move.lengthSq() > 0) move.normalize();

	const activeDisk = this.disks[this.activeDiskIndex];
	const distToCenter = new THREE.Vector3(this.player.mesh.position.x, 0, this.player.mesh.position.z)
	  .sub(new THREE.Vector3(activeDisk.group.position.x, 0, activeDisk.group.position.z))
	  .length();

	const isOffDisk = distToCenter > activeDisk.radius;

	if (this.input.consumeSurge() && this.player.surgeCooldown <= 0) {
	  if (isOffDisk) {
		const jumpDir = move.lengthSq() > 0 ? move.clone() : new THREE.Vector3(0, 0, -1);
		this.player.velocity.add(jumpDir.multiplyScalar(22));
		this.player.verticalVelocity = 12;
		this.player.isJumping = true;
		this.setStatus('Vaulting the Void!', 0.8);
	  } else {
		const dashDirection = move.lengthSq() > 0 ? move.clone() : new THREE.Vector3(0, 0, -1);
		this.player.velocity.add(dashDirection.multiplyScalar(28));
		this.triggerPulse();
		this.setStatus('Surge Burst!', 0.8);
	  }
	  this.player.surgeCooldown = 1.2;
	  this.player.invulnerability = 0.6;
	}

	if (this.player.isJumping || isOffDisk) {
	  this.player.verticalVelocity -= delta * 30;
	  this.player.mesh.position.y += this.player.verticalVelocity * delta;
	  
	  if (this.player.mesh.position.y < -20) {
		this.applyDamage(100, 'Fell into the Void.');
	  }
	  
	  const nextDiskIndex = this.activeDiskIndex + 1;
	  const nextDisk = this.disks[nextDiskIndex];
	  if (nextDisk) {
		const distToNext = new THREE.Vector3(this.player.mesh.position.x, 0, this.player.mesh.position.z)
		  .sub(new THREE.Vector3(nextDisk.group.position.x, 0, nextDisk.group.position.z))
		  .length();
		if (distToNext < nextDisk.radius && this.player.mesh.position.y <= 0 && this.player.mesh.position.y > -2) {
		  this.player.mesh.position.y = 0;
		  this.player.verticalVelocity = 0;
		  this.player.isJumping = false;
		  this.activeDiskIndex = nextDiskIndex;
		  this.setStatus(`Disk ${nextDiskIndex + 1} Secured.`, 1.0);
		}
	  }
	} else {
	  this.player.mesh.position.y = 0;
	}

	const desiredVelocity = move.multiplyScalar(15);
	this.player.velocity.lerp(desiredVelocity, dampFactor(delta, 10));
	this.player.mesh.position.addScaledVector(this.player.velocity, delta);
	this.player.velocity.multiplyScalar(0.95);

	if (move.lengthSq() > 0) {
	  const targetRot = Math.atan2(move.x, move.z);
	  this.player.mesh.rotation.y = targetRot;
	}
  }

  updateEnemies(delta) {
	this.enemies.forEach((enemy) => {
	  enemy.hitCooldown = Math.max(0, enemy.hitCooldown - delta);
	  const disk = this.disks[enemy.diskIndex];
	  
	  if (enemy.stun > 0) {
		enemy.stun = Math.max(0, enemy.stun - delta);
		enemy.mesh.rotation.y += delta * 6;
		enemy.velocity.multiplyScalar(0.94);
	  } else {
		const chase = this.player.mesh.position.clone().sub(enemy.mesh.position);
		chase.y = 0;
		const distanceToPlayer = chase.length();
		
		let desiredVelocity = new THREE.Vector3();
		if (this.activeDiskIndex === enemy.diskIndex && distanceToPlayer < enemy.pursuitRange) {
		  desiredVelocity = chase.normalize().multiplyScalar(enemy.speed * 4.0);
		} else {
		  const patrolPos = new THREE.Vector3(Math.sin(this.elapsed + enemy.phase) * 5, 0, Math.cos(this.elapsed * 0.8 + enemy.phase) * 5).add(disk.group.position);
		  desiredVelocity = patrolPos.sub(enemy.mesh.position).normalize().multiplyScalar(enemy.speed * 1.5);
		}
		enemy.velocity.lerp(desiredVelocity, dampFactor(delta, 4.0));
	  }

	  enemy.mesh.position.addScaledVector(enemy.velocity, delta);
	  
	  const localPos = enemy.mesh.position.clone().sub(disk.group.position);
	  if (localPos.length() > disk.radius - 1) {
		localPos.setLength(disk.radius - 1);
		enemy.mesh.position.copy(localPos.add(disk.group.position));
	  }
	  
	  enemy.mesh.lookAt(this.player.mesh.position.x, enemy.mesh.position.y, this.player.mesh.position.z);

	  const distToPlayer = enemy.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
	  if (distToPlayer < enemy.radius + this.player.radius && enemy.hitCooldown <= 0) {
		enemy.hitCooldown = 1.1;
		this.applyDamage(15, `Swarm Unit collision.`);
	  }
	});
  }

  updateRelics(delta) {
	this.relics.forEach((relic, index) => {
	  if (relic.collected) return;
	  relic.mesh.rotation.y += delta * (1.5 + index * 0.15);
	  relic.mesh.position.y = relic.baseY + Math.sin(this.elapsed * 2 + index) * 0.18;
	  const distance = relic.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
	  if (distance < 1.65) {
		relic.collected = true;
		relic.mesh.visible = false;
		this.relicCount += 1;
		this.score += 100;
		this.setStatus(`Relic secured.`, 1.0);
	  }
	});
  }

  updateHazards(delta) {
	this.hazards.forEach((hazard, index) => {
	  const pulse = 1 + Math.sin(this.elapsed * 2.2 + index) * 0.08;
	  hazard.outline.scale.setScalar(pulse);
	  const distance = hazard.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
	  if (distance < hazard.radius) {
		this.applyDamage(5 * delta, `Hazard hit.`);
	  }
	});
  }

  updateGoal() {
	const bob = Math.sin(this.elapsed * 2.8) * 0.16;
	this.goal.beacon.position.y = 2.2 + bob;
	this.goal.ring.rotation.z += 0.01;
	const distance = this.goal.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
	if (distance < this.goal.radius) {
	  this.finishRun('Extraction Complete', 'The final beacon was reached.');
	}
  }

  updateRain(delta) {
	if (!this.rain) return;
	const attribute = this.rain.points.geometry.getAttribute('position');
	for (let index = 0; index < attribute.count; index += 1) {
	  attribute.array[index * 3 + 1] -= delta * 18;
	  attribute.array[index * 3] += delta * 0.7;
	  if (attribute.array[index * 3 + 1] < 0) {
		attribute.array[index * 3] = (Math.random() - 0.5) * this.config.arena.width;
		attribute.array[index * 3 + 1] = Math.random() * 18 + 6;
		attribute.array[index * 3 + 2] = (Math.random() - 0.5) * this.config.arena.depth;
	  }
	}
	attribute.needsUpdate = true;
  }

  updateCamera(delta) {
	const activeDisk = this.disks[this.activeDiskIndex];
	const targetPosition = activeDisk.group.position.clone().add(new THREE.Vector3(0, 22, 28));
	targetPosition.x += this.player.mesh.position.x * 0.3;
	this.camera.position.lerp(targetPosition, dampFactor(delta, 2.5));
	this.camera.lookAt(activeDisk.group.position);
  }

  updateHud(delta) {
	this.timeRemaining = Math.max(0, this.timeRemaining - delta);
	this.player.surgeCooldown = Math.max(0, this.player.surgeCooldown - delta);
	this.player.invulnerability = Math.max(0, this.player.invulnerability - delta);
	this.player.ring.scale.lerp(new THREE.Vector3(1, 1, 1), dampFactor(delta, 6));

	if (this.timeRemaining <= 0 && this.state === 'running') {
	  this.finishRun('Run Expired', 'The void consumed the route. Press R to restart.');
	}

	if (this.eventTimer > 0) {
	  this.eventTimer = Math.max(0, this.eventTimer - delta);
	}
	const activeMessage = this.eventTimer > 0 ? this.eventMessage : 'Boss Rush Mode';
	this.status.textContent = activeMessage;
	this.metrics.textContent = `Disk ${this.activeDiskIndex + 1}/${this.disks.length} | Health ${Math.ceil(this.player.health)} | Score ${this.score} | Time ${Math.ceil(this.timeRemaining)}s | Surge ${this.player.surgeCooldown > 0 ? this.player.surgeCooldown.toFixed(1) + 's' : 'READY'}`;
  }

  update(delta) {
	if (this.state !== 'running') {
	  this.updateCamera(delta);
	  return;
	}
	this.elapsed += delta;
	this.updatePlayer(delta);
	this.updateSlices(delta);
	this.updateEnemies(delta);
	this.updateRelics(delta);
	this.updateGoal();
	this.updateCamera(delta);
	this.updateHud(delta);
  }

  updateSlices(delta) {
	this.disks.forEach((disk, dIdx) => {
	  disk.wedges.forEach((wedge, wIdx) => {
		if (wedge.state === 'hazardous') {
		  wedge.timer -= delta;
		  const flash = Math.sin(this.elapsed * 15) * 0.5 + 0.5;
		  wedge.mesh.material.emissive.setRGB(1, 0, 0);
		  wedge.mesh.material.emissiveIntensity = 0.2 + flash * 0.8;
		  
		  // Damage check
		  if (dIdx === this.activeDiskIndex) {
			const playerPos = this.player.mesh.position.clone().sub(disk.group.position);
			const angle = Math.atan2(playerPos.x, playerPos.z);
			const normalizedAngle = (angle + Math.PI) / (Math.PI * 2);
			const wedgeAngleIdx = Math.floor(normalizedAngle * disk.wedges.length);
			if (wedgeAngleIdx === wIdx) {
			  this.applyDamage(20 * delta, 'Slice electrified!');
			}
		  }

		  if (wedge.timer <= 0) {
			wedge.state = 'idle';
			wedge.mesh.material.emissive.setHex(0x00ffff);
			wedge.mesh.material.emissiveIntensity = 0.05;
		  }
		} else if (Math.random() < 0.001) {
		  // Random hazard trigger
		  wedge.state = 'hazardous';
		  wedge.timer = 3.0;
		}
	  });
	});
  }

  animate() {
	requestAnimationFrame(() => this.animate());
	const delta = Math.min(this.clock.getDelta(), 0.05);
	this.update(delta);
	this.renderer.render(this.scene, this.camera);
  }

  onResize() {
	const width = this.canvas.clientWidth || window.innerWidth;
	const height = this.canvas.clientHeight || window.innerHeight * 0.68;
	this.camera.aspect = width / height;
	this.camera.updateProjectionMatrix();
	this.renderer.setSize(width, height, false);
  }
}

const game = new ArenaGame();
game.init().catch((error) => {
  const storyText = document.getElementById('story-text');
  const status = document.getElementById('game-status');
  if (storyText) storyText.textContent = error.message;
  if (status) status.textContent = 'Game bootstrap failed.';
  console.error(error);
});
