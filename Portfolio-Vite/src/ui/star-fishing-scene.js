import * as THREE from "three";

const WATER_Y = -0.7;
const TOP_DOWN_VIEW_HEIGHT = 10.4;
const ORB_UNIFORM_COUNT = 8;
const CLICK_RIPPLE_COUNT = 8;

function createStarShape(size) {
  const shape = new THREE.Shape();
  const points = 10;
  for (let index = 0; index <= points; index += 1) {
    const angle = (index / points) * Math.PI * 2 - Math.PI / 2;
    const radius = index % 2 === 0 ? size : size * 0.42;
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius;
    if (index === 0) shape.moveTo(x, y);
    else shape.lineTo(x, y);
  }
  return shape;
}

function createStarMesh(size = 0.22, opacity = 0.92, color = 0xffd66b, flat = false) {
  const geometry = flat
    ? new THREE.ShapeGeometry(createStarShape(size))
    : new THREE.ExtrudeGeometry(createStarShape(size), {
        depth: size * 0.18,
        bevelEnabled: true,
        bevelSize: size * 0.035,
        bevelThickness: size * 0.025,
        bevelSegments: 1,
      });
  if (!flat) {
    geometry.translate(0, 0, -size * 0.09);
  }
  const material = new THREE.MeshStandardMaterial({
    color: 0x000000,
    emissive: color,
    emissiveIntensity: flat ? 0.12 : 0.045,
    metalness: 0.6,
    roughness: 0.18,
    transparent: true,
    opacity,
    depthWrite: false,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.rotation.x = -Math.PI / 2;
  return mesh;
}

function createShootingStar(size = 0.22) {
  const group = new THREE.Group();
  const core = createStarMesh(size, 0.9, 0xffd66b);
  const trail = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]),
    new THREE.LineBasicMaterial({
      color: 0xffd66b,
      transparent: true,
      opacity: 0.35,
      depthWrite: false,
      depthTest: false,
    })
  );
  trail.renderOrder = 3;
  core.renderOrder = 4;
  group.add(trail, core);
  group.userData.core = core;
  group.userData.trail = trail;
  group.userData.size = size;
  group.renderOrder = 4;
  return group;
}

function disposeObject(object) {
  object.traverse((node) => {
    if (node.geometry) node.geometry.dispose();
    if (node.material) {
      if (Array.isArray(node.material)) {
        node.material.forEach((material) => material.dispose());
      } else {
        node.material.dispose();
      }
    }
  });
}

export function createStarFishingScene(host, starStore) {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const coarsePointer = window.matchMedia("(pointer: coarse)").matches;
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(0x07141d, 8, 16);

  const camera = new THREE.OrthographicCamera(-5, 5, 5, -5, 0.1, 30);
  camera.position.set(0, 9.4, 0.05);
  camera.lookAt(0, WATER_Y, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: !coarsePointer, alpha: true });
  const pixelRatio = Math.min(window.devicePixelRatio || 1, coarsePointer ? 1.25 : 1.75);
  renderer.setPixelRatio(pixelRatio);
  renderer.setClearColor(0x02060b, 0);
  host.appendChild(renderer.domElement);
  const interactionTarget = host.closest(".landing-page") || renderer.domElement;
  const renderTarget = new THREE.WebGLRenderTarget(1, 1);
  const starSpinAxis = new THREE.Vector3(0, 1, 0);

  const ambient = new THREE.AmbientLight(0x9bcce5, 0.18);
  const moon = new THREE.DirectionalLight(0x88b7ff, 2.8);
  moon.position.set(-3, 8, 4);
  scene.add(ambient, moon);

  const waterUniforms = {
    uTime: { value: 0 },
    uOrbPositions: { value: Array.from({ length: ORB_UNIFORM_COUNT }, () => new THREE.Vector3(0, -1000, 0)) },
    uOrbColors: { value: Array.from({ length: ORB_UNIFORM_COUNT }, () => new THREE.Vector3(1, 0.84, 0.18)) },
    uClickData: { value: Array.from({ length: CLICK_RIPPLE_COUNT }, () => new THREE.Vector4(0, 0, 0, -100)) },
    uCameraPosition: { value: new THREE.Vector3() },
    uMainLightPos: { value: new THREE.Vector3(-4.5, 8.5, -3.5) },
    uMainLightColor: { value: new THREE.Color(0x1b3f76) },
    uSceneTexture: { value: renderTarget.texture },
    uResolution: { value: new THREE.Vector2(1, 1) },
  };
  const water = new THREE.Mesh(
    new THREE.PlaneGeometry(18, 18, coarsePointer ? 96 : 160, coarsePointer ? 96 : 160),
    new THREE.ShaderMaterial({
      uniforms: waterUniforms,
      depthWrite: false,
      vertexShader: `
        varying vec3 vWorldPosition;
        varying vec3 vNormal;
        uniform float uTime;
        uniform vec3 uOrbPositions[${ORB_UNIFORM_COUNT}];
        uniform vec4 uClickData[${CLICK_RIPPLE_COUNT}];

        vec2 hash(vec2 p) {
          p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
          return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
        }

        float noise(vec2 p) {
          const float K1 = 0.366025404;
          const float K2 = 0.211324865;
          vec2 i = floor(p + (p.x + p.y) * K1);
          vec2 a = p - i + (i.x + i.y) * K2;
          vec2 o = (a.x > a.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
          vec2 b = a - o + K2;
          vec2 c = a - 1.0 + 2.0 * K2;
          vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
          vec3 n = h * h * h * h * vec3(dot(a, hash(i)), dot(b, hash(i + o)), dot(c, hash(i + 1.0)));
          return dot(n, vec3(70.0));
        }

        float fbm(vec2 p) {
          float f = 0.0;
          float amp = 0.5;
          for (int i = 0; i < 3; i++) {
            f += amp * noise(p);
            p *= 2.0;
            amp *= 0.5;
          }
          return f;
        }

        float singleRipple(vec2 pos, vec2 center, float t) {
          float speed = 2.55;
          float d = distance(pos, center);
          float xWave = d - t * speed;
          float wave = -xWave * exp(-xWave * xWave * 0.72);
          float amplitude = 0.1 * exp(-t * 0.92);
          return wave * amplitude;
        }

        float getElevation(vec2 pos) {
          float h = 0.0;
          h += noise(pos * 0.16 + uTime * 0.055) * 0.105;
          h += fbm(pos * 0.34 - uTime * 0.07) * 0.036;
          h += noise(pos * 0.82 + uTime * 0.14) * 0.012;

          for (int i = 0; i < ${ORB_UNIFORM_COUNT}; i++) {
            vec3 orb = uOrbPositions[i];
            float d = distance(pos, orb.xz);
            float rippleStrength = smoothstep(-1.1, 0.1, orb.y) * (1.0 - smoothstep(0.7, 2.0, orb.y));
            h += sin(d * 3.15 - uTime * 3.0) * exp(-d * 0.82) * 0.034 * rippleStrength;
          }

          for (int i = 0; i < ${CLICK_RIPPLE_COUNT}; i++) {
            vec4 click = uClickData[i];
            float t = uTime - click.w;
            if (t > 0.0 && t < 4.0) {
              h += singleRipple(pos, click.xz, t);
            }
          }
          return h;
        }

        void main() {
          vec3 pos = position;
          float h = getElevation(pos.xy);
          pos.z += h;

          float offset = 0.06;
          float hRight = getElevation(pos.xy + vec2(offset, 0.0));
          float hForward = getElevation(pos.xy + vec2(0.0, offset));
          float dx = hRight - h;
          float dy = hForward - h;
          vec3 computedNormal = normalize(vec3(-dx / offset, -dy / offset, 1.0));

          vec4 worldPos = modelMatrix * vec4(pos, 1.0);
          vWorldPosition = worldPos.xyz;
          vNormal = normalize(mat3(modelMatrix) * computedNormal);
          gl_Position = projectionMatrix * viewMatrix * worldPos;
        }
      `,
      fragmentShader: `
        uniform float uTime;
        uniform vec3 uOrbPositions[${ORB_UNIFORM_COUNT}];
        uniform vec3 uOrbColors[${ORB_UNIFORM_COUNT}];
        uniform vec3 uCameraPosition;
        uniform vec3 uMainLightPos;
        uniform vec3 uMainLightColor;
        uniform sampler2D uSceneTexture;
        uniform vec2 uResolution;
        varying vec3 vWorldPosition;
        varying vec3 vNormal;

        void main() {
          vec3 viewDir = normalize(uCameraPosition - vWorldPosition);
          vec3 normal = normalize(vNormal);
          vec3 lightDir = normalize(uMainLightPos - vWorldPosition);

          vec2 uv = gl_FragCoord.xy / uResolution;
          vec2 refractDir = normal.xz;
          vec2 causticDrift = vec2(sin(vWorldPosition.x * 0.95 + uTime * 0.42), cos(vWorldPosition.z * 0.78 - uTime * 0.36)) * 0.0025;
          vec2 distR = refractDir * 0.019 + causticDrift;
          vec2 distG = refractDir * 0.012;
          vec2 distB = refractDir * 0.006 - causticDrift * 0.45;
          float refR = texture2D(uSceneTexture, uv + distR).r;
          float refG = texture2D(uSceneTexture, uv + distG).g;
          float refB = texture2D(uSceneTexture, uv + distB).b;
          vec3 refractedScene = vec3(refR, refG, refB);

          float lum = dot(refractedScene, vec3(0.299, 0.587, 0.114));
          vec3 waterTint = vec3(0.025, 0.036, 0.068);
          vec3 finalColor = mix(refractedScene * waterTint * 2.1, refractedScene * 0.86, smoothstep(0.07, 0.55, lum));

          vec3 reflected = reflect(-viewDir, normal);
          float envFresnel = pow(1.0 - max(dot(viewDir, normal), 0.0), 2.6);
          vec3 envColor = mix(vec3(0.004, 0.004, 0.011), vec3(0.024, 0.038, 0.07), smoothstep(-0.2, 1.0, reflected.y));
          finalColor = mix(finalColor, envColor, envFresnel * 0.82);

          vec3 halfVector = normalize(lightDir + viewDir);
          float nDotH = max(dot(normal, halfVector), 0.0);
          float spec = pow(nDotH, 220.0);
          float softSpec = pow(nDotH, 36.0);
          finalColor += uMainLightColor * (spec * 0.34 + softSpec * 0.035);

          for (int i = 0; i < ${ORB_UNIFORM_COUNT}; i++) {
            vec3 orbPos = uOrbPositions[i];
            vec3 orbColor = uOrbColors[i];
            float dist = distance(vWorldPosition, orbPos);
            float under = smoothstep(0.25, -0.8, orbPos.y);
            float surface = smoothstep(-0.7, 0.25, orbPos.y) * (1.0 - smoothstep(0.65, 1.4, orbPos.y));
            float sss = 0.085 / (1.0 + pow(dist, 2.35) * 6.0);
            float lightPool = 0.055 / (1.0 + dist * dist * 2.2);
            vec3 dirToOrb = normalize(orbPos - vWorldPosition);
            vec3 orbHalf = normalize(dirToOrb + viewDir);
            float orbSpec = pow(max(dot(normal, orbHalf), 0.0), 130.0);
            finalColor += orbColor * (sss * under + lightPool * surface * 0.18 + orbSpec * surface * 0.24);
          }

          finalColor *= 1.08;
          finalColor = (finalColor * (2.51 * finalColor + 0.03)) / (finalColor * (2.43 * finalColor + 0.59) + 0.14);
          finalColor = pow(finalColor, vec3(1.0 / 2.2));
          gl_FragColor = vec4(finalColor, 1.0);
        }
      `,
    })
  );
  water.rotation.x = -Math.PI / 2;
  water.position.y = WATER_Y;
  water.renderOrder = 2;
  scene.add(water);

  const bottom = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 20),
    new THREE.MeshBasicMaterial({ color: 0x000108 })
  );
  bottom.rotation.x = -Math.PI / 2;
  bottom.position.y = WATER_Y - 1.15;
  bottom.renderOrder = -2;
  scene.add(bottom);

  const stars = [];
  const effects = [];
  const maxStars = coarsePointer ? 2 : 3;
  let rippleIndex = 0;
  let nextSpawnAt = null;
  let lastRenderTime = 0;
  let running = false;
  let destroyed = false;
  let frameId = 0;

  function resize() {
    const width = Math.max(1, host.clientWidth);
    const height = Math.max(1, host.clientHeight);
    const aspect = width / height;
    const viewWidth = TOP_DOWN_VIEW_HEIGHT * aspect;
    camera.left = -viewWidth / 2;
    camera.right = viewWidth / 2;
    camera.top = TOP_DOWN_VIEW_HEIGHT / 2;
    camera.bottom = -TOP_DOWN_VIEW_HEIGHT / 2;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height, false);
    renderTarget.setSize(Math.ceil(width * pixelRatio), Math.ceil(height * pixelRatio));
    waterUniforms.uResolution.value.set(Math.ceil(width * pixelRatio), Math.ceil(height * pixelRatio));
    render(performance.now() * 0.001);
  }

  function spawnShootingStar(time) {
    if (stars.length >= maxStars) return;
    const star = createShootingStar(THREE.MathUtils.randFloat(0.1, 0.17));
    const fromLeft = Math.random() > 0.5;
    const startX = fromLeft ? camera.left - 0.8 : camera.right + 0.8;
    const startZ = THREE.MathUtils.randFloat(camera.bottom + 0.8, camera.top - 0.6);
    const endX = fromLeft ? camera.right + 1 : camera.left - 1;
    const endZ = startZ + THREE.MathUtils.randFloat(-2.2, 2.2);
    const dx = endX - startX;
    const dz = endZ - startZ;
    const distance = Math.max(1, Math.hypot(dx, dz));
    const speed = THREE.MathUtils.randFloat(coarsePointer ? 0.7 : 0.85, coarsePointer ? 1.0 : 1.25);
    const vx = (dx / distance) * speed;
    const vz = (dz / distance) * speed;
    const tailLength = THREE.MathUtils.randFloat(0.7, 1.25);
    const surfaceAt = THREE.MathUtils.randFloat(1.8, 3.4);
    const pauseDuration = THREE.MathUtils.randFloat(1.35, 2.05);
    star.position.set(startX, WATER_Y - 0.26, startZ);
    star.userData.vx = vx;
    star.userData.vz = vz;
    star.userData.spawnedAt = time;
    star.userData.life = 0;
    star.userData.tailLength = tailLength;
    star.userData.collectable = false;
    star.userData.captureQueued = false;
    star.userData.flying = false;
    star.userData.flyTarget = new THREE.Vector3();
    star.userData.captureClientX = 0;
    star.userData.captureClientY = 0;
    star.userData.surfaceAt = surfaceAt;
    star.userData.pauseDuration = pauseDuration;
    star.userData.aboveAt = surfaceAt + pauseDuration;
    star.userData.phase = "underwater";
    star.userData.trail.geometry.dispose();
    star.userData.trail.geometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3((-vx / speed) * tailLength, 0, (-vz / speed) * tailLength),
    ]);
    stars.push(star);
    scene.add(star);
  }

  function findCatchableStar(x, z) {
    return stars.reduce(
      (best, star) => {
        const distance = Math.hypot(x - star.position.x, z - star.position.z);
        const radius = star.userData.phase === "underwater" ? 1.45 : 1.8;
        if ((!star.userData.collectable && star.userData.phase !== "underwater") || distance > radius || distance >= best.distance) {
          return best;
        }
        return { star, distance };
      },
      { star: null, distance: Infinity }
    ).star;
  }

  function getStarPhase(star) {
    const life = star.userData.life;
    if (life < star.userData.surfaceAt) return "underwater";
    if (life < star.userData.aboveAt) return "surface";
    return "above";
  }

  function tryCatchStar(clientX, clientY, x, z) {
    const catchTarget = findCatchableStar(x, z);
    if (!catchTarget) return;
    if (catchTarget.userData.phase === "underwater") {
      catchTarget.userData.surfaceAt = Math.max(0, catchTarget.userData.life - 0.02);
      catchTarget.userData.aboveAt = catchTarget.userData.life + 1.05;
      catchTarget.userData.collectable = true;
      catchTarget.userData.captureQueued = true;
      catchTarget.userData.flying = false;
      catchTarget.userData.flyTarget.set(0, 0, 0);
      catchTarget.userData.captureClientX = clientX;
      catchTarget.userData.captureClientY = clientY;
      return;
    }
    collectStar(catchTarget, clientX, clientY);
  }

  function collectStar(catchTarget, clientX, clientY) {
    starStore.addStars(1);
    document.dispatchEvent(
      new CustomEvent("portfolio-star-caught", {
        detail: { clientX, clientY },
      })
    );
    const caught = createStarMesh(0.22);
    caught.position.set(catchTarget.position.x, WATER_Y + 0.1, catchTarget.position.z);
    caught.userData.life = 0;
    caught.userData.caught = true;
    caught.renderOrder = 5;
    effects.push(caught);
    scene.add(caught);
    scene.remove(catchTarget);
    disposeObject(catchTarget);
    stars.splice(stars.indexOf(catchTarget), 1);
  }

  function handlePointer(event) {
    const target = event.target instanceof HTMLElement ? event.target : null;
    if (target?.closest("a, button")) return;
    const bounds = renderer.domElement.getBoundingClientRect();
    const normalX = (event.clientX - bounds.left) / bounds.width;
    const normalY = (event.clientY - bounds.top) / bounds.height;
    const x = THREE.MathUtils.lerp(camera.left, camera.right, normalX);
    const z = THREE.MathUtils.lerp(camera.top, camera.bottom, normalY);
    waterUniforms.uClickData.value[rippleIndex].set(x, WATER_Y, z, lastRenderTime || performance.now() * 0.001);
    rippleIndex = (rippleIndex + 1) % CLICK_RIPPLE_COUNT;
    tryCatchStar(event.clientX, event.clientY, x, z);
    if (!running) start();
  }

  function render(time) {
    const delta = lastRenderTime ? Math.min(0.05, time - lastRenderTime) : 0.016;
    lastRenderTime = time;
    waterUniforms.uTime.value = time;
    waterUniforms.uCameraPosition.value.copy(camera.position);
    if (nextSpawnAt === null) {
      nextSpawnAt = time + 0.75;
    }
    if (time >= nextSpawnAt) {
      spawnShootingStar(time);
      nextSpawnAt = time + THREE.MathUtils.randFloat(coarsePointer ? 2.4 : 1.7, coarsePointer ? 3.8 : 3.0);
    }

    for (let index = stars.length - 1; index >= 0; index -= 1) {
      const star = stars[index];
      star.userData.life += delta;
      const phase = getStarPhase(star);
      star.userData.phase = phase;
      star.userData.collectable = !star.userData.flying && phase === "surface";
      if (star.userData.captureQueued && !star.userData.flying && phase === "above") {
        star.userData.flying = true;
        star.userData.flyTarget.copy(getCollectionPoint());
      }

      if (star.userData.flying) {
        const target = star.userData.flyTarget;
        star.position.lerp(target, Math.min(1, delta * 2.5));
        star.position.y = THREE.MathUtils.lerp(star.position.y, target.y, Math.min(1, delta * 3.0));
        star.userData.core.rotateOnWorldAxis(starSpinAxis, delta * 4.5);
        star.userData.core.material.opacity = Math.min(1, star.userData.core.material.opacity + delta * 0.35);
        star.userData.core.scale.setScalar(Math.max(0.38, star.userData.core.scale.x * 0.94));
        if (star.position.distanceTo(target) < 0.18) {
          collectStar(star, star.userData.captureClientX, star.userData.captureClientY);
          continue;
        }
        continue;
      } else {
        if (phase === "underwater") {
          star.position.x += star.userData.vx * delta;
          star.position.z += star.userData.vz * delta;
        } else if (phase !== "surface") {
          star.position.x += star.userData.vx * delta;
          star.position.z += star.userData.vz * delta;
        }
      }
      const surfaceProgress = THREE.MathUtils.smoothstep(
        star.userData.life,
        star.userData.surfaceAt - 0.45,
        star.userData.surfaceAt + 0.35
      );
      const aboveProgress = THREE.MathUtils.smoothstep(
        star.userData.life,
        star.userData.aboveAt,
        star.userData.aboveAt + 0.55
      );
      star.position.y = THREE.MathUtils.lerp(WATER_Y - 0.28, WATER_Y + 0.32, surfaceProgress);
      star.position.y = THREE.MathUtils.lerp(star.position.y, WATER_Y + 0.6, aboveProgress);
      const fadeIn = THREE.MathUtils.clamp(star.userData.life * 1.2, 0, 1);
      const wave = Math.sin(time * 3.4 + index) * 0.5 + 0.5;
      const underDistortion = phase === "underwater" ? 0.2 + wave * 0.18 : 0;
      const surfaceGlow = phase === "surface" ? 1 : 0;
      const clearAbove = phase === "above" ? 1 : 0;
      const coreOpacity = phase === "underwater" ? fadeIn * (0.2 + wave * 0.1) : fadeIn * (0.82 + surfaceGlow * 0.12);
      star.userData.core.material.opacity = Math.min(0.94, coreOpacity);
      star.userData.trail.material.opacity =
        phase === "underwater" ? fadeIn * 0.04 : phase === "surface" ? fadeIn * 0.02 : fadeIn * (0.12 + clearAbove * 0.08);
      star.userData.core.material.color.setHex(0x000000);
      star.userData.core.material.emissive.setHex(phase === "underwater" ? 0xd2a839 : 0xffe56a);
      star.userData.core.material.emissiveIntensity = phase === "surface" ? 0.18 : phase === "above" ? 0.1 : 0.035;
      star.userData.core.material.metalness = phase === "underwater" ? 0.3 : 0.72;
      star.userData.core.material.roughness = phase === "underwater" ? 0.42 : 0.16;
      if (!star.userData.flying) {
        star.userData.core.rotateOnWorldAxis(starSpinAxis, delta * (phase === "underwater" ? 2.8 : 1.2));
      }
      const scale = phase === "surface" ? 1.2 + wave * 0.04 : phase === "above" ? 0.98 : 0.74 + underDistortion * 0.6;
      star.userData.core.scale.setScalar(scale);
      star.scale.set(1 + underDistortion * 0.5, phase === "underwater" ? 0.8 + wave * 0.05 : 1, 1);
      const renderOrder = phase === "underwater" ? 1 : 5;
      star.renderOrder = renderOrder;
      star.userData.core.renderOrder = renderOrder + 1;
      star.userData.trail.renderOrder = renderOrder - 1;
      const outOfBounds =
        star.position.x < camera.left - 1.4 ||
        star.position.x > camera.right + 1.4 ||
        star.position.z < camera.bottom - 1.4 ||
        star.position.z > camera.top + 1.4;
      if (outOfBounds || star.userData.life > 13) {
        scene.remove(star);
        disposeObject(star);
        stars.splice(index, 1);
      }
    }

    for (let index = 0; index < ORB_UNIFORM_COUNT; index += 1) {
      const star = stars[index];
      if (star) {
        waterUniforms.uOrbPositions.value[index].copy(star.position);
      } else {
        waterUniforms.uOrbPositions.value[index].set(0, -1000, 0);
      }
    }

    water.position.y = WATER_Y + Math.sin(time * 0.55) * 0.025;

    for (let index = effects.length - 1; index >= 0; index -= 1) {
      const item = effects[index];
      item.userData.life += delta * 1.8;
      item.position.y += delta * 1.2;
      item.material.opacity = Math.max(0, 0.9 - item.userData.life);
      item.scale.setScalar(1 + item.userData.life * 0.8);
      if (item.userData.life >= 1) {
        scene.remove(item);
        disposeObject(item);
        effects.splice(index, 1);
      }
    }

    water.visible = false;
    stars.forEach((star) => {
      star.visible = star.userData.phase === "underwater";
    });
    effects.forEach((effect) => {
      effect.visible = false;
    });
    renderer.setRenderTarget(renderTarget);
    renderer.render(scene, camera);

    water.visible = true;
    stars.forEach((star) => {
      star.visible = true;
    });
    effects.forEach((effect) => {
      effect.visible = true;
    });
    renderer.setRenderTarget(null);
    renderer.render(scene, camera);
  }

  function loop(time) {
    if (!running || destroyed) return;
    render(time * 0.001);
    frameId = window.requestAnimationFrame(loop);
  }

  function start() {
    if (running || destroyed || document.hidden || reducedMotion) return;
    running = true;
    frameId = window.requestAnimationFrame(loop);
  }

  function stop() {
    running = false;
    if (frameId) {
      window.cancelAnimationFrame(frameId);
      frameId = 0;
    }
  }

  function handleVisibility() {
    if (document.hidden) {
      stop();
      return;
    }
    start();
    render(performance.now() * 0.001);
  }

  window.addEventListener("resize", resize);
  document.addEventListener("visibilitychange", handleVisibility);
  interactionTarget.addEventListener("pointerdown", handlePointer);
  resize();
  if (reducedMotion) {
    render(performance.now() * 0.001);
  } else {
    start();
  }

  return {
    destroy() {
      destroyed = true;
      stop();
      window.removeEventListener("resize", resize);
      document.removeEventListener("visibilitychange", handleVisibility);
      interactionTarget.removeEventListener("pointerdown", handlePointer);
      scene.traverse((node) => {
        if (node !== scene) disposeObject(node);
      });
      renderTarget.dispose();
      renderer.dispose();
      renderer.domElement.remove();
    },
  };
}
