
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
		this.alertLevel = 0;
		this.playerSpottedThisFrame = false;
		this.extractionProgress = 0;
		this.alertOverloadCooldown = 0;
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
			this.overlayHint.textContent = 'Press Enter to deploy. Use WASD or Arrow keys to move, tap Shift to crash through a patrol window, press Space to pulse and break detection, and press R to restart after a wipe.';
		}
	}

	showIntroOverlay() {
		this.state = 'menu';
		this.overlay.classList.add('visible');
	}

	startRun() {
		this.overlay.classList.remove('visible');
		this.state = 'running';
		this.setStatus(this.config.rules.statusMessage, 2.0);
	}

	applyVisualTheme() {
		const arena = this.config.arena;
		this.scene.background = new THREE.Color(arena.skyColor || '#050813');
		this.scene.fog = new THREE.Fog(arena.fogColor || '#091120', 24, 92);

		const hemi = new THREE.HemisphereLight(0x93cfff, 0x071120, 1.15);
		this.scene.add(hemi);

		const keyLight = new THREE.DirectionalLight(0xe6fbff, 1.35);
		keyLight.position.set(14, 24, 12);
		keyLight.castShadow = true;
		keyLight.shadow.mapSize.set(2048, 2048);
		this.scene.add(keyLight);

		const rimLight = new THREE.PointLight(0x7df9ff, 6.5, 70, 2.1);
		rimLight.position.set(-18, 14, -8);
		this.scene.add(rimLight);
	}

	createArena() {
		const arena = this.config.arena;
		const floor = new THREE.Mesh(
			new THREE.PlaneGeometry(arena.width, arena.depth),
			new THREE.MeshStandardMaterial({ color: arena.groundColor, metalness: 0.15, roughness: 0.9 })
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

		const coverPositions = [
			[-12, -8],
			[10, -12],
			[-14, 10],
			[8, 16],
			[0, -2],
		];
		coverPositions.forEach(([x, z], index) => {
			const block = new THREE.Mesh(
				new THREE.BoxGeometry(index % 2 === 0 ? 3.4 : 2.2, 2.8, index % 2 === 0 ? 1.4 : 3.6),
				new THREE.MeshStandardMaterial({ color: 0x10211a, roughness: 0.78, metalness: 0.08 })
			);
			block.position.set(x, 1.4, z);
			block.castShadow = true;
			block.receiveShadow = true;
			this.scene.add(block);
		});
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
			new THREE.TorusGeometry(playerConfig.radius + 0.28, 0.08, 12, 32),
			new THREE.MeshBasicMaterial({ color: 0x7df9ff, transparent: true, opacity: 0.7 })
		);
		ring.rotation.x = Math.PI / 2;
		ring.position.y = -playerConfig.radius * 0.52;
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
			crashTimer: 0,
			invulnerability: 0,
			maxHealth: playerConfig.maxHealth,
			health: playerConfig.maxHealth,
		};
	}

	createGoal() {
		const goalConfig = this.config.goal;
		const group = new THREE.Group();
		const ring = new THREE.Mesh(
			new THREE.TorusGeometry(goalConfig.radius, 0.2, 16, 40),
			new THREE.MeshStandardMaterial({ color: 0x24415f, emissive: 0x112235, emissiveIntensity: 0.38 })
		);
		ring.rotation.x = Math.PI / 2;
		group.add(ring);

		const beacon = new THREE.Mesh(
			new THREE.CylinderGeometry(0.42, 0.42, 4.8, 12),
			new THREE.MeshStandardMaterial({ color: goalConfig.color, emissive: 0x183542, emissiveIntensity: 0.7 })
		);
		beacon.position.y = 2.4;
		beacon.castShadow = true;
		group.add(beacon);

		group.position.set(goalConfig.position.x, goalConfig.position.y, goalConfig.position.z);
		this.scene.add(group);
		this.goal = { mesh: group, ring, beacon, radius: goalConfig.radius, unlockRelics: goalConfig.unlockRelics };
	}

	createRelics() {
		this.relics = this.config.relics.map((config, index) => {
			const group = new THREE.Group();
			const base = new THREE.Mesh(
				new THREE.CylinderGeometry(1.2, 1.2, 0.28, 24),
				new THREE.MeshStandardMaterial({ color: 0x122318, roughness: 0.82, metalness: 0.08 })
			);
			base.position.y = 0.16;
			group.add(base);

			const core = new THREE.Mesh(
				new THREE.OctahedronGeometry(0.62 + (index % 2) * 0.08, 0),
				new THREE.MeshStandardMaterial({ color: config.color, emissive: 0x19304a, emissiveIntensity: 0.82, roughness: 0.24 })
			);
			core.position.y = 1.28;
			core.castShadow = true;
			group.add(core);

			const ring = new THREE.Mesh(
				new THREE.TorusGeometry(config.radius || 2.5, 0.08, 12, 40),
				new THREE.MeshBasicMaterial({ color: config.color, transparent: true, opacity: 0.36 })
			);
			ring.rotation.x = Math.PI / 2;
			ring.position.y = 0.12;
			group.add(ring);

			group.position.set(config.position.x, 0, config.position.z);
			this.scene.add(group);
			return {
				mesh: group,
				core,
				ring,
				label: config.label,
				baseY: core.position.y,
				radius: config.radius || 2.5,
				holdSeconds: config.holdSeconds || 1.6,
				captureProgress: 0,
				collected: false,
			};
		});
	}

	createHazards() {
		this.hazards = this.config.hazards.map((config, index) => {
			const mesh = new THREE.Mesh(
				new THREE.CylinderGeometry(config.radius, config.radius, 0.14, 32),
				new THREE.MeshBasicMaterial({ color: config.color, transparent: true, opacity: 0.2 })
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

			const beacon = new THREE.Mesh(
				new THREE.CylinderGeometry(0.18, 0.18, 2.8, 8),
				new THREE.MeshStandardMaterial({ color: config.color, emissive: 0x1a2026, emissiveIntensity: 0.8 })
			);
			beacon.position.set(config.position.x, 1.4, config.position.z);
			beacon.castShadow = true;
			this.scene.add(beacon);

			return { ...config, mesh, outline, beacon, phase: index * 1.2 };
		});
	}

	buildDefaultRoute(anchor, index) {
		const size = 6 + index * 2;
		return [
			new THREE.Vector3(anchor.x - size, anchor.y, anchor.z - size),
			new THREE.Vector3(anchor.x + size, anchor.y, anchor.z - size),
			new THREE.Vector3(anchor.x + size, anchor.y, anchor.z + size),
			new THREE.Vector3(anchor.x - size, anchor.y, anchor.z + size),
		];
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

			const visionMesh = new THREE.Mesh(
				new THREE.CircleGeometry(config.visionRange || config.pursuitRange + 3, 28, -(config.visionAngle || 0.9) / 2, config.visionAngle || 0.9),
				new THREE.MeshBasicMaterial({ color: config.color, transparent: true, opacity: 0.12, side: THREE.DoubleSide })
			);
			visionMesh.rotation.x = -Math.PI / 2;
			visionMesh.position.y = 0.04;
			group.add(visionMesh);

			group.position.set(config.position.x, config.position.y, config.position.z);
			this.scene.add(group);

			const anchor = new THREE.Vector3(config.position.x, config.position.y, config.position.z);
			const routePoints = (config.route || []).map((point) => new THREE.Vector3(point.x, point.y, point.z));
			const patrolRoute = routePoints.length > 1 ? routePoints : this.buildDefaultRoute(anchor, index);
			const routeLine = new THREE.LineLoop(
				new THREE.BufferGeometry().setFromPoints(patrolRoute.map((point) => new THREE.Vector3(point.x, 0.06, point.z))),
				new THREE.LineBasicMaterial({ color: config.color, transparent: true, opacity: 0.18 })
			);
			this.scene.add(routeLine);

			return {
				mesh: group,
				body,
				fin,
				visionMesh,
				routeLine,
				name: config.name,
				role: config.role,
				speed: config.speed,
				radius: config.radius,
				pursuitRange: config.pursuitRange,
				visionRange: config.visionRange || config.pursuitRange + 3,
				visionAngle: config.visionAngle || 0.9,
				disableSeconds: config.disableSeconds || 4,
				alertGain: config.alertGain || 24,
				anchor,
				route: patrolRoute,
				routeIndex: 0,
				velocity: new THREE.Vector3(),
				disableTimer: 0,
				alertedTimer: 0,
				hitCooldown: 0,
				sightedTimer: 0,
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
		this.player.crashTimer = 0;
		this.player.invulnerability = 0;
		this.goalUnlocked = false;
		this.relicCount = 0;
		this.score = 0;
		this.alertLevel = 0;
		this.extractionProgress = 0;
		this.timeRemaining = this.config.rules.timeLimitSeconds;
		this.alertOverloadCooldown = 0;
		this.state = 'running';
		this.elapsed = 0;
		this.overlay.classList.remove('visible');
		this.setStatus(this.config.rules.statusMessage, 2.2);

		this.goal.ring.material.color.set(0x24415f);
		this.goal.ring.material.emissive.set(0x112235);
		this.goal.beacon.material.emissiveIntensity = 0.8;

		this.relics.forEach((relic) => {
			relic.collected = false;
			relic.captureProgress = 0;
			relic.mesh.visible = true;
			relic.ring.material.opacity = 0.36;
			relic.core.material.emissiveIntensity = 0.82;
			relic.core.material.color.set(relic.core.material.color);
		});

		this.enemies.forEach((enemy) => {
			enemy.mesh.position.copy(enemy.anchor);
			enemy.velocity.set(0, 0, 0);
			enemy.routeIndex = 0;
			enemy.disableTimer = 0;
			enemy.alertedTimer = 0;
			enemy.hitCooldown = 0;
			enemy.sightedTimer = 0;
			enemy.visionMesh.material.opacity = 0.12;
			enemy.routeLine.material.opacity = 0.18;
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
			this.finishRun('Route Interrupted', 'The patrol grid collapsed onto the route. Press R to run it again.');
		}
	}

	triggerPulse() {
		if (this.player.pulseCooldown > 0 || this.state !== 'running') return;
		const radius = this.config.player.pulseRadius;
		this.player.pulseCooldown = this.config.player.pulseCooldown;
		this.player.ring.scale.setScalar(1.9);
		this.alertLevel = Math.max(0, this.alertLevel - 18);
		this.enemies.forEach((enemy) => {
			const offset = enemy.mesh.position.clone().sub(this.player.mesh.position);
			offset.y = 0;
			const distance = offset.length();
			if (distance < radius + enemy.radius) {
				enemy.disableTimer = Math.max(enemy.disableTimer, 1.6);
				enemy.alertedTimer = 0;
				enemy.velocity.multiplyScalar(0.2);
			}
		});
		this.setStatus('Pulse blackout broke the patrol lock.', 1.0);
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
			this.player.crashTimer = 0.32;
			this.player.invulnerability = Math.max(this.player.invulnerability, 0.16);
			this.setStatus('Crash window open. Punch through a patrol and relocate.', 0.75);
		}

		if (this.input.consumePulse()) {
			this.triggerPulse();
		}

		const desiredVelocity = move.multiplyScalar(this.config.player.speed);
		this.player.velocity.lerp(desiredVelocity, dampFactor(delta, 12));
		this.player.mesh.position.addScaledVector(this.player.velocity, delta);
		this.player.velocity.multiplyScalar(0.9);
		this.player.crashTimer = Math.max(0, this.player.crashTimer - delta);

		const halfWidth = this.config.arena.width * 0.5 - 1.8;
		const halfDepth = this.config.arena.depth * 0.5 - 1.8;
		this.player.mesh.position.x = clamp(this.player.mesh.position.x, -halfWidth, halfWidth);
		this.player.mesh.position.z = clamp(this.player.mesh.position.z, -halfDepth, halfDepth);
		const facing = this.player.velocity.lengthSq() > 0.02 ? this.player.velocity : move;
		if (facing.lengthSq() > 0) {
			this.player.mesh.rotation.y = Math.atan2(facing.x, facing.z);
		}
	}

	updateEnemyPatrol(enemy, delta) {
		const target = enemy.route[enemy.routeIndex];
		const toTarget = target.clone().sub(enemy.mesh.position);
		toTarget.y = 0;
		if (toTarget.length() < 1.1) {
			enemy.routeIndex = (enemy.routeIndex + 1) % enemy.route.length;
		}
		const desiredVelocity = toTarget.normalize().multiplyScalar(enemy.speed * 1.8);
		enemy.velocity.lerp(desiredVelocity, dampFactor(delta, 3.8));
	}

	crashEnemy(enemy) {
		enemy.disableTimer = Math.max(enemy.disableTimer, enemy.disableSeconds);
		enemy.hitCooldown = 0.8;
		enemy.alertedTimer = 0;
		enemy.velocity.set(0, 0, 0);
		enemy.sightedTimer = 0;
		this.player.crashTimer = 0;
		this.alertLevel = Math.max(0, this.alertLevel - 20);
		this.score += 90;
		this.setStatus(`Crash route opened through ${enemy.name}.`, 0.85);
	}

	updateEnemyVision(enemy, delta) {
		enemy.sightedTimer = Math.max(0, enemy.sightedTimer - delta);
		enemy.visionMesh.visible = enemy.disableTimer <= 0;
		enemy.routeLine.material.opacity = enemy.alertedTimer > 0 ? 0.28 : 0.18;
		enemy.visionMesh.material.opacity = enemy.alertedTimer > 0 || enemy.sightedTimer > 0 ? 0.22 : 0.12;
		if (enemy.disableTimer > 0) {
			enemy.visionMesh.material.opacity = 0.05;
			return;
		}

		const forward = new THREE.Vector3(0, 0, 1).applyQuaternion(enemy.mesh.quaternion).setY(0).normalize();
		const toPlayer = this.player.mesh.position.clone().sub(enemy.mesh.position);
		toPlayer.y = 0;
		const distance = toPlayer.length();
		if (distance <= 0.001 || distance > enemy.visionRange) return;
		const angle = Math.acos(clamp(forward.dot(toPlayer.normalize()), -1, 1));
		if (angle <= enemy.visionAngle * 0.5) {
			this.playerSpottedThisFrame = true;
			enemy.alertedTimer = Math.max(enemy.alertedTimer, 1.2);
			enemy.sightedTimer = 0.35;
			this.alertLevel = clamp(this.alertLevel + enemy.alertGain * delta, 0, 100);
			if (this.eventTimer <= 0.05) {
				this.setStatus(`${enemy.name} has movement in the patrol cone. Break sight.`, 0.2);
			}
		}
	}

	updateEnemies(delta) {
		this.enemies.forEach((enemy) => {
			enemy.hitCooldown = Math.max(0, enemy.hitCooldown - delta);
			enemy.disableTimer = Math.max(0, enemy.disableTimer - delta);
			enemy.alertedTimer = Math.max(0, enemy.alertedTimer - delta);

			if (enemy.disableTimer > 0) {
				enemy.mesh.rotation.y += delta * 5.5;
				enemy.velocity.multiplyScalar(0.88);
			} else {
				const chase = this.player.mesh.position.clone().sub(enemy.mesh.position);
				chase.y = 0;
				const distance = chase.length();
				if (enemy.alertedTimer > 0 && distance < enemy.pursuitRange * 1.6) {
					const desiredVelocity = chase.normalize().multiplyScalar(enemy.speed * 2.9);
					enemy.velocity.lerp(desiredVelocity, dampFactor(delta, 4.8));
				} else {
					this.updateEnemyPatrol(enemy, delta);
				}
			}

			enemy.mesh.position.addScaledVector(enemy.velocity, delta);
			enemy.mesh.position.x = clamp(enemy.mesh.position.x, -24, 24);
			enemy.mesh.position.z = clamp(enemy.mesh.position.z, -24, 24);
			if (enemy.velocity.lengthSq() > 0.05) {
				const targetLook = enemy.mesh.position.clone().add(enemy.velocity);
				enemy.mesh.lookAt(targetLook.x, enemy.mesh.position.y, targetLook.z);
			}

			this.updateEnemyVision(enemy, delta);

			const distanceToPlayer = enemy.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
			if (distanceToPlayer < enemy.radius + this.player.radius) {
				if (this.player.crashTimer > 0 && enemy.disableTimer <= 0) {
					this.crashEnemy(enemy);
					return;
				}
				if (enemy.hitCooldown <= 0) {
					enemy.hitCooldown = 1.1;
					this.applyDamage(14, `${enemy.name} closed the patrol gap.`);
					this.alertLevel = clamp(this.alertLevel + 10, 0, 100);
				}
			}
		});
	}

	updateRelics(delta) {
		const decayRate = this.config.rules.uplinkDecayPerSecond || 0.45;
		this.relics.forEach((relic, index) => {
			relic.core.rotation.y += delta * (1.6 + index * 0.12);
			relic.core.position.y = relic.baseY + Math.sin(this.elapsed * 2 + index) * 0.14;
			if (relic.collected) {
				relic.ring.material.opacity = 0.75;
				relic.core.material.emissiveIntensity = 1.1;
				return;
			}

			const distance = relic.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
			if (distance < relic.radius) {
				const captureRate = 1 / relic.holdSeconds;
				const spottedPenalty = this.playerSpottedThisFrame ? 0.45 : 1;
				relic.captureProgress = clamp(relic.captureProgress + delta * captureRate * spottedPenalty, 0, 1);
				relic.ring.material.opacity = 0.36 + relic.captureProgress * 0.42;
				relic.core.material.emissiveIntensity = 0.82 + relic.captureProgress * 0.55;
				this.setStatus(`Holding ${relic.label} uplink ${Math.round(relic.captureProgress * 100)}%.`, 0.15);
				if (relic.captureProgress >= 1) {
					relic.collected = true;
					this.relicCount += 1;
					this.score += 140;
					this.alertLevel = Math.max(0, this.alertLevel - 12);
					this.setStatus(`${relic.label} secured. Route data recovered.`, 1.0);
				}
			} else {
				relic.captureProgress = Math.max(0, relic.captureProgress - delta * decayRate);
				relic.ring.material.opacity = 0.36 + relic.captureProgress * 0.18;
			}
		});
	}

	updateHazards(delta) {
		this.hazards.forEach((hazard, index) => {
			const pulse = 1 + Math.sin(this.elapsed * 2.2 + hazard.phase + index) * 0.08;
			hazard.outline.scale.setScalar(pulse);
			hazard.beacon.material.emissiveIntensity = 0.62 + Math.sin(this.elapsed * 3 + index) * 0.2;
			const distance = hazard.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
			if (distance < hazard.radius) {
				this.applyDamage(hazard.damagePerSecond * delta, `${hazard.name} lit up the route.`);
				this.alertLevel = clamp(this.alertLevel + (hazard.alertPerSecond || 20) * delta, 0, 100);
			}
		});
	}

	updateGoal(delta) {
		const bob = Math.sin(this.elapsed * 2.8) * 0.16;
		this.goal.beacon.position.y = 2.4 + bob;
		this.goal.ring.rotation.z += 0.01;
		if (!this.goalUnlocked && this.relicCount >= this.goal.unlockRelics) {
			this.goalUnlocked = true;
			this.goal.ring.material.color.set(0x7df9ff);
			this.goal.ring.material.emissive.set(0x0f3340);
			this.goal.beacon.material.emissiveIntensity = 1.32;
			this.setStatus('Extraction live. Hold inside the beacon to disappear.', 1.4);
		}
		if (!this.goalUnlocked) return;

		const distance = this.goal.mesh.position.clone().sub(this.player.mesh.position).setY(0).length();
		if (distance < this.goal.radius) {
			const holdSeconds = this.config.rules.extractionHoldSeconds || 1.5;
			this.extractionProgress = clamp(this.extractionProgress + delta / holdSeconds, 0, 1);
			this.setStatus(`Holding extraction ${Math.round(this.extractionProgress * 100)}%.`, 0.2);
			if (this.extractionProgress >= 1) {
				this.finishRun('Extraction Quiet', 'The patrol grid never fully locked on and the intel is secure. Press R to run it again.');
			}
		} else {
			this.extractionProgress = Math.max(0, this.extractionProgress - delta * 0.7);
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
		this.alertOverloadCooldown = Math.max(0, this.alertOverloadCooldown - delta);

		if (!this.playerSpottedThisFrame) {
			this.alertLevel = Math.max(0, this.alertLevel - (this.config.rules.alertDecayPerSecond || 12) * delta);
		}

		if (this.alertLevel >= (this.config.rules.alertDamageThreshold || 100) && this.alertOverloadCooldown <= 0) {
			this.alertLevel = 62;
			this.alertOverloadCooldown = 2.8;
			this.applyDamage(this.config.rules.alertDamage || 18, 'The patrol grid locked on. Break sight and relocate.');
		}

		if (this.timeRemaining <= 0 && this.state === 'running') {
			this.finishRun('Window Closed', 'The storm sealed the route before extraction. Press R to try again.');
		}

		if (this.eventTimer > 0) {
			this.eventTimer = Math.max(0, this.eventTimer - delta);
		}
		const defaultStatus = this.goalUnlocked ? 'Extraction beacon is live. Hold the circle and stay unseen.' : this.config.rules.statusMessage;
		this.status.textContent = this.eventTimer > 0 ? this.eventMessage : defaultStatus;

		const templateLabel = (this.config.rules.mechanicFamily || this.template).replace(/_/g, ' ');
		const scoreLabel = this.config.rules.scoreLabel || 'Intel';
		const extractionText = this.goalUnlocked ? ` | Extract ${Math.round(this.extractionProgress * 100)}%` : '';
		const crashText = this.player.crashTimer > 0 ? 'live' : this.player.dashCooldown > 0 ? `${this.player.dashCooldown.toFixed(1)}s` : 'ready';
		this.metrics.textContent = `${templateLabel} | Health ${Math.ceil(this.player.health)} | ${scoreLabel} ${this.relicCount}/${this.goal.unlockRelics} | Alert ${Math.round(this.alertLevel)}% | Score ${this.score}${extractionText} | Time ${Math.ceil(this.timeRemaining)}s | Crash ${crashText} | Pulse ${this.player.pulseCooldown > 0 ? this.player.pulseCooldown.toFixed(1) + 's' : 'ready'}`;
	}

	update(delta) {
		if (this.state !== 'running') {
			this.updateRain(delta);
			this.updateCamera(delta);
			return;
		}
		this.elapsed += delta;
		this.playerSpottedThisFrame = false;
		this.updatePlayer(delta);
		this.updateEnemies(delta);
		this.updateRelics(delta);
		this.updateHazards(delta);
		this.updateGoal(delta);
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
