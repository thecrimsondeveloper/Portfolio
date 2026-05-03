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

function createStarMesh(size = 0.22, opacity = 0.95, color = 0xffd66b, flat = false) {
  const geometry = flat
    ? new THREE.ShapeGeometry(createStarShape(size))
    : new THREE.ExtrudeGeometry(createStarShape(size), {
        depth: size * 0.45,
        bevelEnabled: true,
        bevelSize: size * 0.08,
        bevelThickness: size * 0.08,
        bevelSegments: 3,
      });
  
  if (!flat) {
    geometry.translate(0, 0, -size * 0.12);
  }

  const material = new THREE.MeshStandardMaterial({
    color: 0x111111,
    emissive: color,
    emissiveIntensity: flat ? 0.25 : 0.8,
    metalness: 0.9,
    roughness: 0.1,
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
  const core = createStarMesh(size, 0.95, 0xffd66b);
  
  const glow = new THREE.PointLight(0xffd66b, 0.8, 2.5);
  glow.position.set(0, 0, 0.1);
  
  const trail = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]),
    new THREE.LineBasicMaterial({
      color: 0xffd66b,
      transparent: true,
      opacity: 0.45,
      depthWrite: false,
      depthTest: false,
    })
  );
  
  trail.renderOrder = 3;
  core.renderOrder = 4;
  group.add(trail, core, glow);
  group.userData.core = core;
  group.userData.trail = trail;
  group.userData.glow = glow;
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
  
  // Get theme colors from CSS variables
  const style = getComputedStyle(document.body);
  const accentColor = new THREE.Color(style.getPropertyValue("--accent").trim() || "#ff7a59");
  const pageBgTop = new THREE.Color(style.getPropertyValue("--page-bg-top").trim() || "#10161c");
  const pageBgBottom = new THREE.Color(style.getPropertyValue("--page-bg-bottom").trim() || "#070b0f");
  const secondaryColor = new THREE.Color(style.getPropertyValue("--secondary").trim() || "#1d6f72");

  scene.fog = new THREE.Fog(pageBgTop, 6, 20);

  const camera = new THREE.OrthographicCamera(-5, 5, 5, -5, 0.1, 50);
  camera.position.set(0, 10, 0.05);
  camera.lookAt(0, WATER_Y, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: !coarsePointer, alpha: true });
  const pixelRatio = Math.min(window.devicePixelRatio || 1, coarsePointer ? 1.5 : 2);
  renderer.setPixelRatio(pixelRatio);
  renderer.setClearColor(0x000000, 0);
  host.appendChild(renderer.domElement);

  const interactionTarget = host.closest(".landing-page") || renderer.domElement;
  const renderTarget = new THREE.WebGLRenderTarget(1, 1, {
    format: THREE.RGBAFormat,
    type: THREE.UnsignedByteType,
  });

  const starSpinAxis = new THREE.Vector3(0, 1, 0);

  const ambient = new THREE.AmbientLight(secondaryColor, 0.25);
  const moon = new THREE.DirectionalLight(accentColor, 1.5);
  moon.position.set(-5, 12, 5);
  scene.add(ambient, moon);

  const waterUniforms = {
    uTime: { value: 0 },
    uOrbPositions: { value: Array.from({ length: ORB_UNIFORM_COUNT }, () => new THREE.Vector3(0, -1000, 0)) },
    uOrbColors: { value: Array.from({ length: ORB_UNIFORM_COUNT }, () => new THREE.Vector3(1, 0.88, 0.25)) },
    uClickData: { value: Array.from({ length: CLICK_RIPPLE_COUNT }, () => new THREE.Vector4(0, 0, 0, -100)) },
    uCameraPosition: { value: new THREE.Vector3() },
    uMainLightPos: { value: new THREE.Vector3(-4.5, 8.5, -3.5) },
    uMainLightColor: { value: accentColor },
    uSceneTexture: { value: renderTarget.texture },
    uResolution: { value: new THREE.Vector2(1, 1) },
    uDeepColor: { value: pageBgBottom },
    uSurfaceColor: { value: secondaryColor },
  };

  const water = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 20, coarsePointer ? 100 : 180, coarsePointer ? 100 : 180),
    new THREE.ShaderMaterial({
      uniforms: waterUniforms,
      depthWrite: false,
      transparent: true,
      vertexShader: `
        varying vec3 vWorldPosition;
        varying vec3 vNormal;
        varying vec2 vUv;
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
          float speed = 2.8;
          float d = distance(pos, center);
          float xWave = d - t * speed;
          float wave = -xWave * exp(-xWave * xWave * 0.85);
          float amplitude = 0.15 * exp(-t * 0.8);
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
          vUv = uv;
          vec3 pos = position;
          float h = getElevation(pos.xy);
          pos.z += h;

          float offset = 0.05;
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
        uniform vec3 uDeepColor;
        uniform vec3 uSurfaceColor;
        varying vec3 vWorldPosition;
        varying vec3 vNormal;
        varying vec2 vUv;

        void main() {
          vec3 viewDir = normalize(uCameraPosition - vWorldPosition);
          vec3 normal = normalize(vNormal);
          vec3 lightDir = normalize(uMainLightPos - vWorldPosition);

          vec2 uv = gl_FragCoord.xy / uResolution;
          vec2 refractDir = normal.xz;
          
          vec2 causticDrift = vec2(sin(vWorldPosition.x * 0.8 + uTime * 0.5), cos(vWorldPosition.z * 0.7 - uTime * 0.4)) * 0.003;
          vec2 distR = refractDir * 0.022 + causticDrift;
          vec2 distG = refractDir * 0.015;
          vec2 distB = refractDir * 0.008 - causticDrift * 0.5;
          
          float refR = texture2D(uSceneTexture, uv + distR).r;
          float refG = texture2D(uSceneTexture, uv + distG).g;
          float refB = texture2D(uSceneTexture, uv + distB).b;
          vec3 refractedScene = vec3(refR, refG, refB);

          float lum = dot(refractedScene, vec3(0.299, 0.587, 0.114));
          
          vec3 waterBase = mix(uDeepColor, uSurfaceColor, smoothstep(-1.5, 0.5, vWorldPosition.y));
          vec3 finalColor = mix(waterBase * 1.5, refractedScene, smoothstep(0.02, 0.4, lum));
          
          finalColor = mix(finalColor, uDeepColor, 0.15);

          vec3 reflected = reflect(-viewDir, normal);
          float envFresnel = pow(1.0 - max(dot(viewDir, normal), 0.0), 3.0);
          vec3 envColor = mix(uDeepColor * 0.5, uSurfaceColor * 1.2, smoothstep(-0.3, 1.2, reflected.y));
          finalColor = mix(finalColor, envColor, envFresnel * 0.75);

          vec3 halfVector = normalize(lightDir + viewDir);
          float nDotH = max(dot(normal, halfVector), 0.0);
          float spec = pow(nDotH, 256.0);
          float softSpec = pow(nDotH, 48.0);
          finalColor += uMainLightColor * (spec * 0.5 + softSpec * 0.06);

          for (int i = 0; i < ${ORB_UNIFORM_COUNT}; i++) {
            vec3 orbPos = uOrbPositions[i];
            vec3 orbColor = uOrbColors[i];
            float dist = distance(vWorldPosition, orbPos);
            
            float under = smoothstep(0.3, -1.0, orbPos.y);
            float surface = smoothstep(-0.8, 0.3, orbPos.y) * (1.0 - smoothstep(0.7, 1.8, orbPos.y));
            
            float sss = 0.12 / (1.0 + pow(dist, 2.5) * 8.0);
            float lightPool = 0.08 / (1.0 + dist * dist * 3.0);
            
            vec3 dirToOrb = normalize(orbPos - vWorldPosition);
            vec3 orbHalf = normalize(dirToOrb + viewDir);
            float orbSpec = pow(max(dot(normal, orbHalf), 0.0), 160.0);
            
            finalColor += orbColor * (sss * under + lightPool * surface * 0.25 + orbSpec * surface * 0.35);
          }

          finalColor *= 1.15;
          finalColor = (finalColor * (2.51 * finalColor + 0.03)) / (finalColor * (2.43 * finalColor + 0.59) + 0.14);
          finalColor = pow(finalColor, vec3(1.0 / 2.2));
          
          gl_FragColor = vec4(finalColor, 0.98);
        }
      `,
    })
  );
  water.rotation.x = -Math.PI / 2;
  water.position.y = WATER_Y;
  water.renderOrder = 2;
  scene.add(water);

  const bottom = new THREE.Mesh(
    new THREE.PlaneGeometry(25, 25),
    new THREE.MeshBasicMaterial({ color: 0x010308 })
  );
  bottom.rotation.x = -Math.PI / 2;
  bottom.position.y = WATER_Y - 1.5;
  bottom.renderOrder = -2;
  scene.add(bottom);

  const stars = [];
  const effects = [];
  const maxStars = coarsePointer ? 3 : 4;
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
    const star = createShootingStar(THREE.MathUtils.randFloat(0.12, 0.19));
    const fromLeft = Math.random() > 0.5;
    const startX = fromLeft ? camera.left - 1.2 : camera.right + 1.2;
    const startZ = THREE.MathUtils.randFloat(camera.bottom + 1.2, camera.top - 1.2);
    const endX = fromLeft ? camera.right + 1.5 : camera.left - 1.5;
    const endZ = startZ + THREE.MathUtils.randFloat(-3, 3);
    const dx = endX - startX;
    const dz = endZ - startZ;
    const distance = Math.max(1, Math.hypot(dx, dz));
    const speed = THREE.MathUtils.randFloat(coarsePointer ? 0.6 : 0.75, coarsePointer ? 0.9 : 1.1);
    const vx = (dx / distance) * speed;
    const vz = (dz / distance) * speed;
    const tailLength = THREE.MathUtils.randFloat(0.8, 1.4);
    const surfaceAt = THREE.MathUtils.randFloat(2.0, 4.0);
    const pauseDuration = THREE.MathUtils.randFloat(1.5, 2.5);
    
    star.position.set(startX, WATER_Y - 0.4, startZ);
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
        // Tightened radius for "actually require a click"
        const radius = star.userData.phase === "underwater" ? 1.25 : 1.5;
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
      catchTarget.userData.surfaceAt = Math.max(0, catchTarget.userData.life - 0.05);
      catchTarget.userData.aboveAt = catchTarget.userData.life + 1.2;
      catchTarget.userData.collectable = true;
      catchTarget.userData.captureQueued = true;
      catchTarget.userData.captureClientX = clientX;
      catchTarget.userData.captureClientY = clientY;
      
      catchTarget.userData.core.material.emissiveIntensity = 2.5;
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
    
    const caught = createStarMesh(0.24, 1.0, 0xffe58a);
    caught.position.set(catchTarget.position.x, WATER_Y + 0.2, catchTarget.position.z);
    caught.userData.life = 0;
    caught.userData.caught = true;
    caught.renderOrder = 5;
    
    effects.push(caught);
    scene.add(caught);
    scene.remove(catchTarget);
    disposeObject(catchTarget);
    stars.splice(stars.indexOf(catchTarget), 1);
  }

  function getCollectionPoint() {
    const x = THREE.MathUtils.lerp(camera.left, camera.right, 0.1);
    const z = THREE.MathUtils.lerp(camera.top, camera.bottom, 0.1);
    return new THREE.Vector3(x, WATER_Y + 2.0, z);
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
      nextSpawnAt = time + 1.0;
    }
    if (time >= nextSpawnAt) {
      spawnShootingStar(time);
      nextSpawnAt = time + THREE.MathUtils.randFloat(coarsePointer ? 2.5 : 1.8, coarsePointer ? 4.5 : 3.5);
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
        star.position.lerp(target, Math.min(1, delta * 3.2));
        star.position.y = THREE.MathUtils.lerp(star.position.y, target.y, Math.min(1, delta * 3.5));
        star.userData.core.rotateOnWorldAxis(starSpinAxis, delta * 6.5);
        star.userData.core.material.opacity = Math.min(1, star.userData.core.material.opacity + delta * 0.5);
        star.userData.core.scale.setScalar(Math.max(0.4, star.userData.core.scale.x * 0.92));
        star.userData.glow.intensity = Math.max(0, star.userData.glow.intensity - delta * 0.5);
        
        if (star.position.distanceTo(target) < 0.25) {
          collectStar(star, star.userData.captureClientX, star.userData.captureClientY);
          continue;
        }
        continue;
      } else {
        star.position.x += star.userData.vx * delta;
        star.position.z += star.userData.vz * delta;
      }

      const surfaceProgress = THREE.MathUtils.smoothstep(star.userData.life, star.userData.surfaceAt - 0.5, star.userData.surfaceAt + 0.4);
      const aboveProgress = THREE.MathUtils.smoothstep(star.userData.life, star.userData.aboveAt, star.userData.aboveAt + 0.6);
      
      star.position.y = THREE.MathUtils.lerp(WATER_Y - 0.4, WATER_Y + 0.35, surfaceProgress);
      star.position.y = THREE.MathUtils.lerp(star.position.y, WATER_Y + 0.8, aboveProgress);

      const fadeIn = THREE.MathUtils.clamp(star.userData.life * 1.5, 0, 1);
      const pulse = Math.sin(time * 4.0 + index) * 0.5 + 0.5;
      
      star.userData.core.material.opacity = Math.min(0.98, fadeIn * (phase === "underwater" ? 0.3 + pulse * 0.15 : 0.85 + pulse * 0.1));
      star.userData.trail.material.opacity = fadeIn * (phase === "underwater" ? 0.05 : 0.15 + pulse * 0.1);
      
      star.userData.core.material.emissiveIntensity = phase === "surface" ? 1.2 + pulse * 0.3 : phase === "above" ? 0.8 : 0.15 + pulse * 0.1;
      star.userData.glow.intensity = (phase === "underwater" ? 0.2 : 0.8) * fadeIn;
      
      if (!star.userData.flying) {
        star.userData.core.rotateOnWorldAxis(starSpinAxis, delta * (phase === "underwater" ? 3.2 : 1.5));
      }
      
      const scaleBase = phase === "surface" ? 1.3 : phase === "above" ? 1.1 : 0.85;
      star.userData.core.scale.setScalar(scaleBase + pulse * 0.08);

      const renderOrder = phase === "underwater" ? 1 : 5;
      star.renderOrder = renderOrder;
      star.userData.core.renderOrder = renderOrder + 1;
      star.userData.trail.renderOrder = renderOrder - 1;

      const outOfBounds =
        star.position.x < camera.left - 2.0 ||
        star.position.x > camera.right + 2.0 ||
        star.position.z < camera.bottom - 2.0 ||
        star.position.z > camera.top + 2.0;
        
      if (outOfBounds || star.userData.life > 15) {
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

    water.position.y = WATER_Y + Math.sin(time * 0.6) * 0.03;

    for (let index = effects.length - 1; index >= 0; index -= 1) {
      const item = effects[index];
      item.userData.life += delta * 2.0;
      item.position.y += delta * 1.5;
      item.material.opacity = Math.max(0, 1.0 - item.userData.life);
      item.scale.setScalar(1.2 + item.userData.life * 1.2);
      if (item.userData.life >= 1) {
        scene.remove(item);
        disposeObject(item);
        effects.splice(index, 1);
      }
    }

    water.visible = false;
    stars.forEach((star) => { star.visible = star.userData.phase === "underwater"; });
    effects.forEach((effect) => { effect.visible = false; });
    
    renderer.setRenderTarget(renderTarget);
    renderer.render(scene, camera);

    water.visible = true;
    stars.forEach((star) => { star.visible = true; });
    effects.forEach((effect) => { effect.visible = true; });
    
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
