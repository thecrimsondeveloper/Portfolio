
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js';

const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
const dampFactor = (delta, sharpness) => 1 - Math.exp(-delta * sharpness);

class InputManager {
  constructor() {
	this.keys = { forward: false, backward: false, left: false, right: false };
	this.dashRequested = false;
	this.pulseRequested = false;
	window.addEventListener('keydown', (event) => this.onKeyDown(event));
	window.addEventListener('keyup', (event) => this.onKeyUp(event));
  }

  onKeyDown(event) {
	if (['w', 'ArrowUp'].includes(event.key)) this.keys.forward = true;
	if (['s', 'ArrowDown'].includes(event.key)) this.keys.backward = true;
	if (['a', 'ArrowLeft'].includes(event.key)) this.keys.left = true;
	if (['d', 'ArrowRight'].includes(event.key)) this.keys.right = true;
	if (event.key === 'Shift' && !event.repeat) this.dashRequested = true;
	if (event.key === ' ' && !event.repeat) {
	  this.pulseRequested = true;
	  event.preventDefault();
	}
  }

  onKeyUp(event) {
	if (['w', 'ArrowUp'].includes(event.key)) this.keys.forward = false;
	if (['s', 'ArrowDown'].includes(event.key)) this.keys.backward = false;
	if (['a', 'ArrowLeft'].includes(event.key)) this.keys.left = false;
	if (['d', 'ArrowRight'].includes(event.key)) this.keys.right = false;
  }

  consumeDash() {
	const requested = this.dashRequested;
	this.dashRequested = false;
	return requested;
  }

  consumePulse() {
	const requested = this.pulseRequested;
	this.pulseRequested = false;
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
	this.relics = [];
	this.enemies = [];
	this.hazards = [];
	this.rain = null;
	this.timeRemaining = 0;
	this.relicCount = 0;
		this.goalUnlocked = false;
		this.eventMessage = '';
		this.eventTimer = 0;
		this.template = 'arena_survival';
		this.score = 0;
	  }

  async init() {
	await this.loadStory();
	this.applyVisualTheme();
	this.createArena();
	this.createPlayer();
	this.createGoal();
	this.createRelics();
	this.createHazards();
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
	  this.overlayHint.textContent = 'Press Enter to deploy. Use WASD or Arrow keys to move, Shift to dash, Space to pulse. Press R to restart after a wipe.';
	}
  }

  showIntroOverlay() {
	this.state = 'menu';
	this.overlay.classList.add('visible');
  }

  startRun() {
	this.overlay.classList.remove('visible');
	this.state = 'running';
	this.setStatus(this.config.rules.statusMessage || 'Collect relics and unlock the exit.', 2.2);
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

	const rimLight = new THREE.PointLight(0x7df9ff, 7, 70, 2.1);
	rimLight.position.set(-18, 14, -8);
	this.scene.add(rimLight);
  }

  createArena() {
	const arena = this.config.arena;
	const floor = new THREE.Mesh(
	  new THREE.PlaneGeometry(arena.width, arena.depth),
	  new THREE.MeshStandardMaterial({ color: arena.groundColor, metalness: 0.15, roughness: 0.88 })
	);
	floor.rotation.x = -Math.PI / 2;
	floor.receiveShadow = true;
	this.scene.add(floor);

	const water = new THREE.Mesh(
	  new THREE.CircleGeometry(Math.max(arena.width, arena.depth) * 0.72, 64),
	  new THREE.MeshBasicMaterial({ color: 0x06101d, transparent: true, opacity: 0.85 })
	);
	water.rotation.x = -Math.PI / 2;
	water.position.y = -0.03;
	this.scene.add(water);

	const grid = new THREE.GridHelper(arena.width, 18, arena.accentColor, arena.laneColor);
	grid.position.y = 0.02;
	this.scene.add(grid);

	const boundary = new THREE.Mesh(
	  new THREE.RingGeometry(arena.width * 0.46, arena.width * 0.49, 64),
	  new THREE.MeshBasicMaterial({ color: arena.accentColor, transparent: true, opacity: 0.16, side: THREE.DoubleSide })
	);
	boundary.rotation.x = -Math.PI / 2;
	boundary.position.y = 0.03;
	this.scene.add(boundary);
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
	  dashCooldown: 0,
	  pulseCooldown: 0,
	  invulnerability: 0,
	  maxHealth: playerConfig.maxHealth,
	  health: playerConfig.maxHealth,
	};
  }

  createGoal() {
	const goalConfig = this.config.goal;
	const group = new THREE.Group();
	const ring = new THREE.Mesh(
	  new THREE.TorusGeometry(goalConfig.radius, 0.18, 16, 40),
	  new THREE.MeshStandardMaterial({ color: 0x24415f, emissive: 0x112235, emissiveIntensity: 0.45 })
	);
	ring.rotation.x = Math.PI / 2;
	group.add(ring);

	const beacon = new THREE.Mesh(
	  new THREE.CylinderGeometry(0.38, 0.38, 4.5, 12),
	  new THREE.MeshStandardMaterial({ color: goalConfig.color, emissive: 0x1a3840, emissiveIntensity: 0.8 })
	);
	beacon.position.y = 2.2;
	beacon.castShadow = true;
	group.add(beacon);

	group.position.set(goalConfig.position.x, goalConfig.position.y, goalConfig.position.z);
	this.scene.add(group);
	this.goal = { mesh: group, ring, beacon, radius: goalConfig.radius, unlockRelics: goalConfig.unlockRelics };
  }

  createRelics() {
	this.relics = this.config.relics.map((config, index) => {
	  const mesh = new THREE.Mesh(
		new THREE.OctahedronGeometry(0.7 + (index % 2) * 0.1, 0),
		new THREE.MeshStandardMaterial({ color: config.color, emissive: 0x19304a, emissiveIntensity: 0.75, roughness: 0.2 })
	  );
	  mesh.position.set(config.position.x, config.position.y, config.position.z);
	  mesh.castShadow = true;
	  this.scene.add(mesh);
	  return { mesh, label: config.label, baseY: config.position.y, collected: false };
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
	this.enemies = this.config.enemies.map((config, index) => {
	  const group = new THREE.Group();
	  const body = new THREE.Mesh(
		new THREE.DodecahedronGeometry(config.radius, 0),
		new THREE.MeshStandardMaterial({ color: config.color, emissive: 0x21111b, emissiveIntensity: 0.4, roughness: 0.35 })
	  );
	  body.castShadow = true;
	  group.add(body);
	  const fin = new THREE.Mesh(
		new THREE.ConeGeometry(config.radius * 0.55, config.radius * 1.45, 8),
		new THREE.MeshStandardMaterial({ color: 0xfff2d8, emissive: 0x281a12, emissiveIntensity: 0.22 })
	  );
	  fin.rotation.x = Math.PI;
	  fin.position.y = config.radius * 0.95;
	  group.add(fin);
	  group.position.set(config.position.x, config.position.y, config.position.z);
	  this.scene.add(group);
	  return {
		mesh: group,
		name: config.name,
		role: config.role,
		speed: config.speed,
		radius: config.radius,
		pursuitRange: config.pursuitRange,
		anchor: new THREE.Vector3(config.position.x, config.position.y, config.position.z),
		velocity: new THREE.Vector3(),
		stun: 0,
		hitCooldown: 0,
		phase: index * 0.7,
	  };
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
	const playerConfig = this.config.player;
	this.player.mesh.position.set(playerConfig.start.x, playerConfig.start.y, playerConfig.start.z);
	this.player.velocity.set(0, 0, 0);
	this.player.health = this.player.maxHealth;
	this.player.dashCooldown = 0;
	this.player.pulseCooldown = 0;
	this.player.invulnerability = 0;
		this.goalUnlocked = false;
		this.relicCount = 0;
		this.score = 0;
		this.timeRemaining = this.config.rules.timeLimitSeconds;
	this.state = 'running';
	this.elapsed = 0;
	this.overlay.classList.remove('visible');
	this.setStatus(this.config.rules.statusMessage || 'Collect relics and unlock the exit.', 2.2);

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
	if (this.player.pulseCooldown > 0 || this.state !== 'running') return;
	const radius = this.config.player.pulseRadius;
	this.player.pulseCooldown = this.config.player.pulseCooldown;
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
	this.setStatus('Pulse burst cleared breathing room.', 1.0);
  }

  updatePlayer(delta) {
	const move = new THREE.Vector3(
	  (this.input.keys.right ? 1 : 0) - (this.input.keys.left ? 1 : 0),
	  0,
	  (this.input.keys.backward ? 1 : 0) - (this.input.keys.forward ? 1 : 0)
	);
	if (move.lengthSq() > 0) move.normalize();

	if (this.input.consumeDash() && this.player.dashCooldown <= 0) {
	  const dashDirection = move.lengthSq() > 0 ? move.clone() : new THREE.Vector3(0, 0, -1);
	  this.player.velocity.add(dashDirection.multiplyScalar(this.config.player.dashSpeed));
	  this.player.dashCooldown = this.config.player.dashCooldown;
	  this.setStatus('Dash burst engaged.', 0.8);
	}

	if (this.input.consumePulse()) {
	  this.triggerPulse();
	}

		const desiredVelocity = move.multiplyScalar(this.config.player.speed);
		this.player.velocity.lerp(desiredVelocity, dampFactor(delta, 12));
		if (this.template === 'route_runner' && this.state === 'running') {
		  this.player.velocity.z -= 1.6;
		}
		this.player.mesh.position.addScaledVector(this.player.velocity, delta);
	this.player.velocity.multiplyScalar(0.92);

	const halfWidth = this.config.arena.width * 0.5 - 1.8;
	const halfDepth = this.config.arena.depth * 0.5 - 1.8;
	this.player.mesh.position.x = clamp(this.player.mesh.position.x, -halfWidth, halfWidth);
	this.player.mesh.position.z = clamp(this.player.mesh.position.z, -halfDepth, halfDepth);
	this.player.mesh.rotation.y = Math.atan2(this.player.velocity.x || move.x, this.player.velocity.z || move.z);
  }

  updateEnemies(delta) {
	this.enemies.forEach((enemy) => {
	  enemy.hitCooldown = Math.max(0, enemy.hitCooldown - delta);
	  if (enemy.stun > 0) {
		enemy.stun = Math.max(0, enemy.stun - delta);
		enemy.mesh.rotation.y += delta * 6;
		enemy.velocity.multiplyScalar(0.94);
	  } else {
		const chase = this.player.mesh.position.clone().sub(enemy.mesh.position);
		chase.y = 0;
		const distance = chase.length();
		let desiredVelocity = new THREE.Vector3();
			if (this.template === 'stealth_patrol') {
			  const patrol = new THREE.Vector3(Math.sin(this.elapsed * 0.8 + enemy.phase), 0, Math.cos(this.elapsed * 0.6 + enemy.phase));
			  desiredVelocity = distance < enemy.pursuitRange ? chase.normalize().multiplyScalar(enemy.speed * 3.2) : patrol.multiplyScalar(enemy.speed * 1.45);
			} else if (this.template === 'route_runner') {
			  desiredVelocity.set(Math.sin(this.elapsed * 1.6 + enemy.phase), 0, Math.cos(this.elapsed * 0.4 + enemy.phase) * 0.35).multiplyScalar(enemy.speed * 2.4);
			  if (distance < enemy.pursuitRange) desiredVelocity.add(chase.normalize().multiplyScalar(enemy.speed * 1.7));
			} else if (this.template === 'relay_chain') {
			  desiredVelocity = distance < enemy.pursuitRange ? chase.normalize().multiplyScalar(enemy.speed * 3.5) : enemy.anchor.clone().sub(enemy.mesh.position).setY(0).multiplyScalar(0.25);
			} else {
			  if (distance < enemy.pursuitRange) {
				desiredVelocity = chase.normalize().multiplyScalar(enemy.speed * 4.3);
			  } else {
				desiredVelocity.set(Math.sin(this.elapsed + enemy.phase), 0, Math.cos(this.elapsed * 0.8 + enemy.phase)).multiplyScalar(enemy.speed * 1.8);
			  }
			}
		enemy.velocity.lerp(desiredVelocity, dampFactor(delta, 4.8));
	  }

	  enemy.mesh.position.addScaledVector(enemy.velocity, delta);
	  enemy.mesh.position.x = clamp(enemy.mesh.position.x, -24, 24);
	  enemy.mesh.position.z = clamp(enemy.mesh.position.z, -24, 24);
	  enemy.mesh.lookAt(this.player.mesh.position.x, enemy.mesh.position.y, this.player.mesh.position.z);

	  const distanceToPlayer = enemy.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
	  if (distanceToPlayer < enemy.radius + this.player.radius && enemy.hitCooldown <= 0) {
		enemy.hitCooldown = 1.1;
		this.applyDamage(12, `${enemy.name} broke through the route.`);
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
			const scoreGain = this.template === 'relay_chain' ? 150 : this.template === 'stealth_patrol' ? 125 : 100;
			this.score += scoreGain;
			const scoreLabel = this.config.rules.scoreLabel || 'Relic';
			this.setStatus(`${scoreLabel} ${relic.label} secured. Exit charge increased.`, 1.0);
		if (!this.goalUnlocked && this.relicCount >= this.goal.unlockRelics) {
		  this.goalUnlocked = true;
		  this.goal.ring.material.color.set(0x7df9ff);
		  this.goal.ring.material.emissive?.set?.(0x0f3340);
		  this.goal.beacon.material.emissiveIntensity = 1.35;
		  this.setStatus('Exit gate unlocked. Reach the beacon.', 1.4);
		}
	  }
	});
  }

  updateHazards(delta) {
	this.hazards.forEach((hazard, index) => {
	  const pulse = 1 + Math.sin(this.elapsed * 2.2 + index) * 0.08;
	  hazard.outline.scale.setScalar(pulse);
	  const distance = hazard.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
	  if (distance < hazard.radius) {
		this.applyDamage(hazard.damagePerSecond * delta, `${hazard.name} chewed through the route.`);
	  }
	});
  }

  updateGoal() {
	const bob = Math.sin(this.elapsed * 2.8) * 0.16;
	this.goal.beacon.position.y = 2.2 + bob;
	this.goal.ring.rotation.z += 0.01;
	if (!this.goalUnlocked) return;
		const distance = this.goal.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
		if (distance < this.goal.radius) {
		  const winCopy = {
			arena_survival: ['Route Cleared', 'The exit gate is live and the relic chain is stable. Press R to run it again.'],
			route_runner: ['Finish Lane Cleared', 'The route gates are behind you and the sprint line is open. Press R to run it again.'],
			stealth_patrol: ['Extraction Quiet', 'The patrol grid never fully locked on and the intel is secure. Press R to run it again.'],
			relay_chain: ['Signal Chain Live', 'Every relay is linked and the final beacon is transmitting. Press R to run it again.'],
			extraction_maze: ['Maze Extracted', 'The artifact route is mapped and the exit is open. Press R to run it again.'],
		  }[this.template] || ['Route Cleared', 'The exit gate is live. Press R to run it again.'];
		  this.finishRun(winCopy[0], winCopy[1]);
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
	const offset = this.config.camera.offset;
	const targetPosition = new THREE.Vector3(
	  this.player.mesh.position.x + offset.x,
	  offset.y,
	  this.player.mesh.position.z + offset.z
	);
	this.camera.position.lerp(targetPosition, dampFactor(delta, 3.5));
	this.camera.lookAt(this.player.mesh.position.x, 0.8, this.player.mesh.position.z - 2);
  }

  updateHud(delta) {
	this.timeRemaining = Math.max(0, this.timeRemaining - delta);
	this.player.dashCooldown = Math.max(0, this.player.dashCooldown - delta);
	this.player.pulseCooldown = Math.max(0, this.player.pulseCooldown - delta);
	this.player.invulnerability = Math.max(0, this.player.invulnerability - delta);
	this.player.ring.scale.lerp(new THREE.Vector3(1, 1, 1), dampFactor(delta, 6));

	if (this.timeRemaining <= 0 && this.state === 'running') {
	  this.finishRun('Window Closed', 'The storm sealed the route before extraction. Press R to try again.');
	}

	if (this.eventTimer > 0) {
	  this.eventTimer = Math.max(0, this.eventTimer - delta);
		}
		const activeMessage = this.eventTimer > 0 ? this.eventMessage : this.config.rules.statusMessage;
		this.status.textContent = activeMessage;
		const templateLabel = (this.config.rules.mechanicFamily || this.template).replace(/_/g, ' ');
		const scoreLabel = this.config.rules.scoreLabel || 'Relics';
		this.metrics.textContent = `${templateLabel} | Health ${Math.ceil(this.player.health)} | ${scoreLabel} ${this.relicCount}/${this.goal.unlockRelics} | Score ${this.score} | Time ${Math.ceil(this.timeRemaining)}s | Dash ${this.player.dashCooldown > 0 ? this.player.dashCooldown.toFixed(1) + 's' : 'ready'} | Pulse ${this.player.pulseCooldown > 0 ? this.player.pulseCooldown.toFixed(1) + 's' : 'ready'}`;
	  }

  update(delta) {
	if (this.state !== 'running') {
	  this.updateRain(delta);
	  this.updateCamera(delta);
	  return;
	}
	this.elapsed += delta;
	this.updatePlayer(delta);
	this.updateEnemies(delta);
	this.updateRelics(delta);
	this.updateHazards(delta);
	this.updateGoal();
	this.updateRain(delta);
	this.updateCamera(delta);
	this.updateHud(delta);
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
