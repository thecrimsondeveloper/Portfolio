function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function pick(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function resolveAssetPath(basePath, relativePath) {
  const absoluteBase = new URL(basePath, window.location.href);
  return new URL(relativePath, absoluteBase).toString();
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = reject;
    image.src = src;
  });
}

async function loadImageMap(basePath, entries = {}) {
  const pairs = await Promise.all(
    Object.entries(entries).map(async ([key, relativePath]) => [key, await loadImage(resolveAssetPath(basePath, relativePath))])
  );
  return Object.fromEntries(pairs);
}

function createBaseState(config, assets, dom) {
  const palette = assets.palettes[config.palette] || assets.palettes.signal;
  document.body.style.background = `radial-gradient(circle at top, ${palette.accent}22, transparent 28%), linear-gradient(180deg, ${palette.bgTop} 0%, ${palette.bgBottom} 72%)`;
  document.documentElement.style.setProperty("--hud-surface", palette.surface);
  document.documentElement.style.setProperty("--hud-line", palette.line);
  document.documentElement.style.setProperty("--hud-muted", palette.muted);
  document.documentElement.style.setProperty("--button-start", palette.accent);
  document.documentElement.style.setProperty("--button-end", palette.accentStrong);

  return {
    config,
    assets,
    dom,
    palette,
    width: dom.canvas.width,
    height: dom.canvas.height,
    running: false,
    time: 0,
    score: 0,
    speed: 1,
    bestScore: 0,
    particles: [],
    metrics: {},
    modeState: {},
    ui: {
      settingsOpen: false,
      helpOpen: false,
      menuOpen: false,
      paused: false,
      settingsState: {},
    },
    images: {
      sprites: assets.spriteImages || {},
      effects: assets.effectImages || {}
    }
  };
}

function resizeCanvas(state) {
  state.dom.canvas.width = window.innerWidth;
  state.dom.canvas.height = window.innerHeight;
  state.width = state.dom.canvas.width;
  state.height = state.dom.canvas.height;
  if (typeof state.onResize === "function") {
    state.onResize();
  }
}

function updateHud(state, extra = []) {
  const rows = [
    ["Score", String(state.score)],
    ["Mode", extra[0] || state.config.hud.modeLabel || "Arcade"],
    ["Pace", extra[1] || `${state.speed.toFixed(1)}x`]
  ];
  if (extra[2]) {
    rows.push(["Stage", extra[2]]);
  }
  state.dom.hud.innerHTML = `
    <div class="arcade-hud-head">
      <h1>${state.config.title}</h1>
      <div class="arcade-hud-actions">
        <button class="arcade-hud-button" type="button" data-arcade-toggle="help">Help</button>
        <button class="arcade-hud-button" type="button" data-arcade-toggle="settings">Settings</button>
        <button class="arcade-hud-button" type="button" data-arcade-toggle="menu">Menu</button>
      </div>
    </div>
    ${rows.map(([label, value]) => `<div class="arcade-hud-row"><span class="arcade-hud-label">${label}</span><span class="arcade-hud-value">${value}</span></div>`).join("")}
    <p class="arcade-hint">${state.config.instructions}</p>
  `;
}

function showOverlay(state, title, copy, actionLabel) {
  state.dom.panelTitle.textContent = title;
  state.dom.panelCopy.textContent = copy;
  state.dom.action.textContent = actionLabel;
  state.dom.overlay.classList.remove("hidden");
}

function hideOverlay(state) {
  state.dom.overlay.classList.add("hidden");
}

function ensureSharedPanels(state) {
  if (!state.dom.utilityRoot) {
    const utilityRoot = document.createElement("div");
    utilityRoot.className = "arcade-utility-root";
    utilityRoot.innerHTML = `
      <section class="arcade-drawer hidden" data-arcade-panel="settings" aria-label="Settings panel"></section>
      <section class="arcade-drawer hidden" data-arcade-panel="help" aria-label="Help overlay"></section>
      <section class="arcade-drawer hidden" data-arcade-panel="menu" aria-label="Game menu"></section>
    `;
    document.body.appendChild(utilityRoot);
    state.dom.utilityRoot = utilityRoot;
    state.dom.settingsPanel = utilityRoot.querySelector('[data-arcade-panel="settings"]');
    state.dom.helpPanel = utilityRoot.querySelector('[data-arcade-panel="help"]');
    state.dom.menuPanel = utilityRoot.querySelector('[data-arcade-panel="menu"]');
  }
}

function getConfigDefaults(config) {
  const defaults = {
    settings: {
      title: "Settings",
      sections: [
        {
          title: "Gameplay",
          controls: [
            { key: "difficulty", label: "Difficulty", type: "select", value: "normal", options: ["easy", "normal", "hard"] },
            { key: "effectIntensity", label: "Effect Intensity", type: "range", value: 0.75, min: 0, max: 1, step: 0.05 },
          ],
        },
      ],
    },
    help: {
      title: "How To Start",
      steps: [
        "Press Start to enter the run.",
        `Use the listed controls: ${config.instructions}`,
        "Follow the HUD goal and react to the playfield.",
        "Restart from the menu if the run ends.",
      ],
      tips: ["Open Settings to tune feel before the run.", "Open Menu to restart or resume."],
    },
    menu: {
      title: "Pause Menu",
      actions: [
        { label: "Resume", action: "resume" },
        { label: "Restart", action: "restart" },
        { label: "Help", action: "open_help" },
        { label: "Settings", action: "open_settings" },
      ],
    },
    onboarding: {
      title: "Get Started",
      startSteps: [
        "Open the help panel if you need the controls.",
        "Press the start button on the center overlay.",
        "Watch the first few beats or hazards before chasing score.",
      ],
      firstGoal: "Survive the opening loop and learn the pattern.",
    },
  };
  return {
    settings: config.settings || defaults.settings,
    help: config.help || defaults.help,
    menu: config.menu || defaults.menu,
    onboarding: config.onboarding || defaults.onboarding,
  };
}

function initializeSettingsState(state) {
  const sections = state.shared.settings.sections || [];
  for (const section of sections) {
    for (const control of section.controls || []) {
      state.ui.settingsState[control.key] = control.value;
    }
  }
}

function renderSettingsPanel(state) {
  const sections = state.shared.settings.sections || [];
  state.dom.settingsPanel.innerHTML = `
    <div class="arcade-drawer-panel">
      <div class="arcade-drawer-head">
        <h3>${state.shared.settings.title}</h3>
        <button type="button" class="arcade-drawer-close" data-arcade-close="settings">Close</button>
      </div>
      ${sections.map((section) => `
        <div class="arcade-settings-section">
          <h4>${section.title}</h4>
          ${(section.controls || []).map((control) => renderSettingControl(state, control)).join("")}
        </div>
      `).join("")}
    </div>
  `;
}

function renderSettingControl(state, control) {
  const value = state.ui.settingsState[control.key];
  if (control.type === "select") {
    return `
      <label class="arcade-setting-row">
        <span>${control.label}</span>
        <select data-arcade-setting="${control.key}">
          ${(control.options || []).map((option) => `<option value="${option}"${option === value ? " selected" : ""}>${option}</option>`).join("")}
        </select>
      </label>
    `;
  }
  return `
    <label class="arcade-setting-row">
      <span>${control.label}</span>
      <input
        data-arcade-setting="${control.key}"
        type="range"
        min="${control.min ?? 0}"
        max="${control.max ?? 1}"
        step="${control.step ?? 0.1}"
        value="${value}"
      />
    </label>
  `;
}

function renderHelpPanel(state) {
  state.dom.helpPanel.innerHTML = `
    <div class="arcade-drawer-panel">
      <div class="arcade-drawer-head">
        <h3>${state.shared.help.title}</h3>
        <button type="button" class="arcade-drawer-close" data-arcade-close="help">Close</button>
      </div>
      <ol class="arcade-step-list">
        ${(state.shared.help.steps || []).map((step) => `<li>${step}</li>`).join("")}
      </ol>
      <div class="arcade-tip-list">
        ${(state.shared.help.tips || []).map((tip) => `<p>${tip}</p>`).join("")}
      </div>
    </div>
  `;
}

function renderMenuPanel(state) {
  state.dom.menuPanel.innerHTML = `
    <div class="arcade-drawer-panel">
      <div class="arcade-drawer-head">
        <h3>${state.shared.menu.title}</h3>
        <button type="button" class="arcade-drawer-close" data-arcade-close="menu">Close</button>
      </div>
      <div class="arcade-menu-actions">
        ${(state.shared.menu.actions || []).map((item) => `
          <button type="button" class="arcade-menu-button" data-arcade-action="${item.action}">
            ${item.label}
          </button>
        `).join("")}
      </div>
      <div class="arcade-onboarding-block">
        <h4>${state.shared.onboarding.title}</h4>
        <ol class="arcade-step-list">
          ${(state.shared.onboarding.startSteps || []).map((step) => `<li>${step}</li>`).join("")}
        </ol>
        <p class="arcade-first-goal"><strong>First goal:</strong> ${state.shared.onboarding.firstGoal}</p>
      </div>
    </div>
  `;
}

function renderSharedPanels(state) {
  renderSettingsPanel(state);
  renderHelpPanel(state);
  renderMenuPanel(state);
}

function syncSharedPanels(state) {
  togglePanel(state.dom.settingsPanel, state.ui.settingsOpen);
  togglePanel(state.dom.helpPanel, state.ui.helpOpen);
  togglePanel(state.dom.menuPanel, state.ui.menuOpen);
}

function togglePanel(panel, isOpen) {
  panel.classList.toggle("hidden", !isOpen);
}

function closeAllPanels(state) {
  state.ui.settingsOpen = false;
  state.ui.helpOpen = false;
  state.ui.menuOpen = false;
  state.ui.paused = false;
  syncSharedPanels(state);
}

function openPanel(state, panelName) {
  closeAllPanels(state);
  if (panelName === "settings") state.ui.settingsOpen = true;
  if (panelName === "help") state.ui.helpOpen = true;
  if (panelName === "menu") {
    state.ui.menuOpen = true;
    state.ui.paused = true;
  }
  syncSharedPanels(state);
}

function performMenuAction(state, action) {
  if (action === "resume") {
    closeAllPanels(state);
    return;
  }
  if (action === "restart") {
    state.running = true;
    state.time = 0;
    closeAllPanels(state);
    state.mode.start(state);
    hideOverlay(state);
    return;
  }
  if (action === "open_help") {
    openPanel(state, "help");
    return;
  }
  if (action === "open_settings") {
    openPanel(state, "settings");
  }
}

function bindSharedUi(state) {
  document.addEventListener("click", (event) => {
    const target = event.target instanceof HTMLElement ? event.target : null;
    if (!target) return;
    const toggle = target.closest("[data-arcade-toggle]");
    if (toggle instanceof HTMLElement) {
      openPanel(state, toggle.dataset.arcadeToggle || "");
      return;
    }
    const close = target.closest("[data-arcade-close]");
    if (close instanceof HTMLElement) {
      closeAllPanels(state);
      return;
    }
    const action = target.closest("[data-arcade-action]");
    if (action instanceof HTMLElement) {
      performMenuAction(state, action.dataset.arcadeAction || "");
      return;
    }
  });

  document.addEventListener("input", (event) => {
    const target = event.target instanceof HTMLInputElement || event.target instanceof HTMLSelectElement ? event.target : null;
    if (!target) return;
    const key = target.dataset.arcadeSetting;
    if (!key) return;
    state.ui.settingsState[key] = target.type === "range" ? Number(target.value) : target.value;
  });
}

function emitParticles(state, x, y, color, count = 8, effectKey = "spark") {
  for (let i = 0; i < count; i += 1) {
    state.particles.push({
      x,
      y,
      vx: (Math.random() - 0.5) * 3,
      vy: (Math.random() - 0.5) * 3,
      radius: 4 + Math.random() * 5,
      alpha: 0.6,
      color,
      effectKey,
      rotation: Math.random() * Math.PI * 2
    });
  }
}

function updateParticles(state, dt) {
  for (const particle of state.particles) {
    particle.x += particle.vx * 60 * dt;
    particle.y += particle.vy * 60 * dt;
    particle.alpha *= 0.96;
    particle.radius *= 0.985;
  }
  state.particles = state.particles.filter((particle) => particle.alpha > 0.04);
}

function drawParticles(state) {
  const { ctx } = state.dom;
  for (const particle of state.particles) {
    const effectImage = state.images.effects[particle.effectKey];
    if (effectImage) {
      ctx.save();
      ctx.globalAlpha = clamp(particle.alpha, 0, 1);
      ctx.translate(particle.x, particle.y);
      ctx.rotate(particle.rotation);
      const size = particle.radius * 3.2;
      ctx.drawImage(effectImage, -size / 2, -size / 2, size, size);
      ctx.restore();
      continue;
    }
    ctx.fillStyle = `${particle.color}${Math.floor(clamp(particle.alpha, 0, 1) * 255).toString(16).padStart(2, "0")}`;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawSprite(ctx, image, x, y, width, height, options = {}) {
  if (!image) return;
  const {
    alpha = 1,
    rotation = 0,
    glow = null
  } = options;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.translate(x + width / 2, y + height / 2);
  ctx.rotate(rotation);
  if (glow) {
    ctx.shadowColor = glow.color;
    ctx.shadowBlur = glow.blur;
  }
  ctx.drawImage(image, -width / 2, -height / 2, width, height);
  ctx.restore();
}

function createRunnerObstacle(state, lane, options = {}) {
  const content = state.config.content;
  return {
    lane,
    y: -80,
    width: state.width * (options.widthFactor ?? content.obstacleWidthFactor ?? 0.085),
    height: state.height * (options.heightFactor ?? content.obstacleHeightFactor ?? 0.08),
    hidden: options.hidden ?? false,
    revealAt: options.revealAt ?? state.height * (content.hiddenRevealAt ?? 0.25)
  };
}

const modes = {
  runner: {
    setup(state) {
      const lanes = state.config.content.lanes;
      const content = state.config.content;
      state.modeState = {
        lanes,
        lane: 1,
        targetLane: 1,
        playerX: 0,
        spawnTimer: content.spawnInterval ?? 0.5,
        obstacles: [],
        distance: 0,
        scoreBonus: 0,
        steadyTime: 0,
        comboTime: 0,
        burstTimer: content.burstInterval ?? Infinity,
        checkpointLane: 1,
        nextCheckpoint: content.checkpointInterval ?? null,
        checkpointFlash: 0,
        stageIndex: 0,
        stageTimer: 0,
        stageName: content.stageSequence ? content.stageSequence[0]?.name : null,
        lastLane: 1
      };
      state.onResize = () => {
        state.modeState.playerX = laneX(state, state.modeState.lane);
      };
      state.onResize();
      state.handleKeyDown = (event) => {
        if (event.key === "ArrowLeft" || event.key.toLowerCase() === "a") {
          state.modeState.targetLane = clamp(state.modeState.targetLane - 1, 0, lanes.length - 1);
          state.modeState.lane = state.modeState.targetLane;
        }
        if (event.key === "ArrowRight" || event.key.toLowerCase() === "d") {
          state.modeState.targetLane = clamp(state.modeState.targetLane + 1, 0, lanes.length - 1);
          state.modeState.lane = state.modeState.targetLane;
        }
      };
    },
    start(state) {
      const content = state.config.content;
      state.score = 0;
      state.speed = 1;
      state.time = 0;
      state.modeState.spawnTimer = content.spawnInterval ?? 0.5;
      state.modeState.obstacles = [];
      state.modeState.distance = 0;
      state.modeState.lane = 1;
      state.modeState.targetLane = 1;
      state.modeState.scoreBonus = 0;
      state.modeState.steadyTime = 0;
      state.modeState.comboTime = 0;
      state.modeState.burstTimer = content.burstInterval ?? Infinity;
      state.modeState.checkpointLane = 1;
      state.modeState.nextCheckpoint = content.checkpointInterval ?? null;
      state.modeState.checkpointFlash = 0;
      state.modeState.stageIndex = 0;
      state.modeState.stageTimer = 0;
      state.modeState.stageSequence = content.stageSequence ? [...content.stageSequence] : [];
      const expertThreshold = content.expertRecoveryUnlockScore;
      if (!expertThreshold || state.bestScore < expertThreshold) {
        state.modeState.stageSequence = state.modeState.stageSequence.filter((stage) => stage.name !== "recovery");
      }
      state.modeState.stageName = state.modeState.stageSequence[0]?.name || null;
      state.modeState.skinKey = content.visuals?.spriteKey || "runnerShip";
      if (content.skinUnlockScore && state.bestScore >= content.skinUnlockScore && content.visuals?.unlockedSpriteKey) {
        state.modeState.skinKey = content.visuals.unlockedSpriteKey;
      }
      state.modeState.dispatchLog = content.dispatchLog || [];
      state.modeState.lastLane = 1;
      state.onResize();
    },
    update(state, dt) {
      const content = state.config.content;
      const speedGrowth = content.speedGrowth ?? 0.08;
      const speedCap = content.speedCap ?? 4.2;
      const spawnFactor = content.spawnFactor ?? 0.09;
      const spawnMin = content.spawnMin ?? 0.26;

      state.speed = 1 + Math.min(speedCap, state.time * speedGrowth);
      state.modeState.distance += dt * state.speed * 140;
      state.modeState.playerX += (laneX(state, state.modeState.targetLane) - state.modeState.playerX) * Math.min(1, dt * 12);
      const stageSequence = state.modeState.stageSequence || [];
      let allowHandoff = true;
      let allowBurst = true;
      let allowCombo = true;
      if (stageSequence.length) {
        state.modeState.stageTimer += dt;
        const stage = stageSequence[state.modeState.stageIndex];
        state.modeState.stageName = stage?.name || null;
        while (stage && state.modeState.stageTimer >= stage.duration) {
          state.modeState.stageTimer -= stage.duration;
          state.modeState.stageIndex = (state.modeState.stageIndex + 1) % stageSequence.length;
        }
        const currentStage = stageSequence[state.modeState.stageIndex];
        state.modeState.stageName = currentStage?.name || null;
        allowHandoff = currentStage?.name === "handoff";
        allowBurst = currentStage?.name === "rush";
        allowCombo = currentStage?.name === "sprint";
      }
      if (content.checkpointInterval && allowHandoff) {
        state.modeState.checkpointFlash = Math.max(0, state.modeState.checkpointFlash - dt * 1.8);
        while (state.modeState.nextCheckpoint !== null && state.modeState.distance >= state.modeState.nextCheckpoint) {
          if (state.modeState.lane === state.modeState.checkpointLane) {
            state.modeState.scoreBonus += content.checkpointReward ?? 18;
            state.modeState.checkpointFlash = 1;
          }
          state.modeState.nextCheckpoint += content.checkpointInterval;
          state.modeState.checkpointLane = pick(content.checkpointLanes || [1]);
        }
      }
      state.modeState.spawnTimer -= dt;
      if (state.modeState.spawnTimer <= 0) {
        const pattern = pick(content.patterns);
        for (const laneIndex of pattern.lanes) {
          state.modeState.obstacles.push(createRunnerObstacle(state, laneIndex, {
            hidden: Math.random() < (content.hiddenObstacleRate ?? 0)
          }));
        }
        state.modeState.spawnTimer = Math.max(spawnMin, (content.spawnInterval ?? 0.95) - state.speed * spawnFactor);
      }

      if (content.burstInterval && allowBurst) {
        state.modeState.burstTimer -= dt;
        if (state.modeState.burstTimer <= 0) {
          const burstPatterns = content.burstPatterns || [
            { lanes: [0, 1] },
            { lanes: [1, 2] },
            { lanes: [0, 1, 2] }
          ];
          const burst = pick(burstPatterns);
          for (const laneIndex of burst.lanes) {
            state.modeState.obstacles.push(createRunnerObstacle(state, laneIndex));
          }
          state.modeState.burstTimer += content.burstInterval;
        }
      }

      for (const obstacle of state.modeState.obstacles) {
        obstacle.y += (320 + state.speed * 135) * dt;
      }

      if (content.bonusLane !== undefined && allowHandoff) {
        if (state.modeState.lane === content.bonusLane) {
          state.modeState.steadyTime += dt;
          if (state.modeState.steadyTime >= (content.bonusHoldTime ?? 1.2)) {
            state.modeState.scoreBonus += content.bonusPoints ?? 10;
            state.modeState.steadyTime -= (content.bonusHoldTime ?? 1.2);
          }
        } else {
          state.modeState.steadyTime = 0;
        }
      }

      if (content.comboThreshold && content.comboReward && allowCombo) {
        if (state.modeState.lane === state.modeState.lastLane) {
          state.modeState.comboTime += dt;
          if (state.modeState.comboTime >= content.comboThreshold) {
            state.modeState.scoreBonus += content.comboReward;
            state.modeState.comboTime -= content.comboThreshold;
          }
        } else {
          state.modeState.comboTime = 0;
        }
      }
      state.modeState.lastLane = state.modeState.lane;

      emitParticles(state, state.modeState.playerX, state.height - 82, state.palette.accent, 1, "smoke");
      state.modeState.obstacles = state.modeState.obstacles.filter((obstacle) => obstacle.y < state.height + 120);
      const playerY = state.height - 110;
      const hit = state.modeState.obstacles.some((obstacle) => {
        const x = laneX(state, obstacle.lane) - obstacle.width / 2;
        return Math.abs(state.modeState.playerX - (x + obstacle.width / 2)) < 28 &&
          obstacle.y + obstacle.height > playerY - 18 &&
          obstacle.y < playerY + 22;
      });
      if (hit) {
        state.running = false;
        state.bestScore = Math.max(state.bestScore, state.score);
        showOverlay(state, "Run Crashed", `Score ${state.score}. Best ${state.bestScore}.`, "Restart Run");
      }
      state.score = Math.floor(state.modeState.distance / 14) + state.modeState.scoreBonus;
      updateHud(state, [state.config.hud.modeLabel, `${state.speed.toFixed(1)}x`, state.modeState.stageName ? state.modeState.stageName.replace(/(^|\s)\S/g, (t) => t.toUpperCase()) : null]);
    },
    draw(state) {
      const { ctx } = state.dom;
      const content = state.config.content;
      ctx.clearRect(0, 0, state.width, state.height);
      drawVerticalGradient(state);
      drawRunnerTrack(state);
      if (content.checkpointInterval) {
        const x = laneX(state, state.modeState.checkpointLane) - state.width * 0.065;
        const zoneWidth = state.width * 0.13;
        const zoneHeight = state.height * 0.12;
        ctx.fillStyle = `${state.palette.accent}33`;
        ctx.fillRect(x, 40, zoneWidth, zoneHeight);
        ctx.strokeStyle = state.palette.accentStrong;
        ctx.lineWidth = 2;
        ctx.strokeRect(x, 40, zoneWidth, zoneHeight);
        ctx.fillStyle = state.palette.accentStrong;
        ctx.font = "bold 14px system-ui, sans-serif";
        ctx.fillText("HANDOFF", x + 8, 60);
        if (state.modeState.checkpointFlash > 0) {
          ctx.fillStyle = `rgba(255,255,255,${state.modeState.checkpointFlash})`;
          ctx.font = "bold 24px system-ui, sans-serif";
          ctx.fillText("RELAY BONUS!", state.width * 0.5 - 78, state.height * 0.18);
        }
      }
      for (const obstacle of state.modeState.obstacles) {
        const x = laneX(state, obstacle.lane) - obstacle.width / 2;
        const alpha = obstacle.hidden && obstacle.y < obstacle.revealAt ? 0.14 : 1;
        drawSprite(ctx, state.images.sprites.hazardBlock, x, obstacle.y, obstacle.width, obstacle.height, {
          alpha,
          glow: { color: state.palette.danger, blur: obstacle.hidden ? 0 : 12 }
        });
      }
      const playerY = state.height - 110;
      const shipKey = state.modeState.skinKey || state.config.visuals?.spriteKey || "runnerShip";
      const shipImage = state.images.sprites[shipKey] || state.images.sprites.runnerShip;
      drawSprite(ctx, shipImage, state.modeState.playerX - 28, playerY - 34, 56, 56, {
        glow: { color: state.palette.accent, blur: 16 }
      });
      const dispatchText = state.modeState.dispatchLog?.[state.modeState.stageIndex] || "";
      if (dispatchText) {
        ctx.fillStyle = state.palette.ink;
        ctx.font = "bold 12px system-ui, sans-serif";
        ctx.fillText(dispatchText, 24, state.height - 24);
      }
      drawParticles(state);
    }
  },
  orbit: {
    setup(state) {
      state.modeState = {
        pointer: { x: state.width / 2, y: state.height / 2 },
        score: 0,
        combo: 1,
        angle: 0,
        targets: []
      };
      state.handlePointerMove = (event) => {
        state.modeState.pointer.x = event.clientX;
        state.modeState.pointer.y = event.clientY;
      };
      state.handleClick = () => {
        const target = state.modeState.targets.find((item) => !item.hit && Math.hypot(item.x - state.modeState.pointer.x, item.y - state.modeState.pointer.y) < item.radius + 12);
        if (target) {
          target.hit = true;
          state.score += 10 * state.modeState.combo;
          state.modeState.combo += 1;
          emitParticles(state, target.x, target.y, state.palette.warning, 10);
        } else {
          state.modeState.combo = 1;
        }
      };
      refillOrbitTargets(state);
    },
    start(state) {
      state.score = 0;
      state.modeState.combo = 1;
      refillOrbitTargets(state);
    },
    update(state, dt) {
      state.modeState.angle += dt * state.config.content.orbitSpeed;
      for (const target of state.modeState.targets) {
        target.theta += dt * target.velocity;
        target.x = state.width / 2 + Math.cos(target.theta) * target.radiusBand;
        target.y = state.height / 2 + Math.sin(target.theta * 1.2) * (target.radiusBand * 0.65);
      }
      if (state.modeState.targets.every((target) => target.hit)) {
        refillOrbitTargets(state);
      }
      updateHud(state, [`Combo ${state.modeState.combo}`, `${state.score}`]);
      updateParticles(state, dt);
    },
    draw(state) {
      const { ctx } = state.dom;
      ctx.clearRect(0, 0, state.width, state.height);
      drawVerticalGradient(state);
      const cx = state.width / 2;
      const cy = state.height / 2;
      ctx.strokeStyle = "rgba(255,255,255,0.09)";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(cx, cy, state.config.content.coreRadius, 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = state.palette.accentStrong;
      drawSprite(ctx, state.images.sprites.orbNode, cx + Math.cos(state.modeState.angle) * 90 - 18, cy + Math.sin(state.modeState.angle * 1.35) * 62 - 18, 36, 36, {
        glow: { color: state.palette.accentStrong, blur: 18 }
      });
      for (const target of state.modeState.targets) {
        if (target.hit) continue;
        drawSprite(ctx, state.images.sprites.orbNode, target.x - target.radius, target.y - target.radius, target.radius * 2, target.radius * 2, {
          alpha: 0.92,
          glow: { color: target.color, blur: 12 }
        });
      }
      ctx.strokeStyle = "rgba(255,255,255,0.18)";
      ctx.beginPath();
      ctx.moveTo(state.modeState.pointer.x - 10, state.modeState.pointer.y);
      ctx.lineTo(state.modeState.pointer.x + 10, state.modeState.pointer.y);
      ctx.moveTo(state.modeState.pointer.x, state.modeState.pointer.y - 10);
      ctx.lineTo(state.modeState.pointer.x, state.modeState.pointer.y + 10);
      ctx.stroke();
      drawParticles(state);
    }
  },
  pulseGrid: {
    setup(state) {
      state.modeState = {
        active: false,
        pulse: 0,
        step: 0,
        sequence: [...state.config.content.sequence],
        deadline: 1.4,
        timer: 0
      };
      state.handleKeyDown = (event) => {
        if (event.code !== "Space") return;
        if (!state.running) return;
        const correctStep = state.modeState.sequence[state.modeState.step];
        const onBeat = Math.abs(state.modeState.timer - correctStep.time) < 0.22;
        state.modeState.pulse = 1;
        if (onBeat) {
          state.score += 15;
          state.modeState.step = (state.modeState.step + 1) % state.modeState.sequence.length;
          emitParticles(state, state.width / 2, state.height / 2, state.palette.accent, 12);
        } else {
          state.score = Math.max(0, state.score - 8);
        }
      };
    },
    start(state) {
      state.score = 0;
      state.modeState.timer = 0;
      state.modeState.step = 0;
      state.modeState.pulse = 0;
    },
    update(state, dt) {
      state.modeState.timer += dt;
      if (state.modeState.timer > state.modeState.deadline) {
        state.modeState.timer = 0;
      }
      state.modeState.pulse *= 0.92;
      updateHud(state, [`Beat ${state.modeState.step + 1}`, `${state.score}`]);
      updateParticles(state, dt);
    },
    draw(state) {
      const { ctx } = state.dom;
      ctx.clearRect(0, 0, state.width, state.height);
      drawVerticalGradient(state);
      const cell = Math.min(78, state.width / 8);
      for (let y = 0; y < 5; y += 1) {
        for (let x = 0; x < 5; x += 1) {
          const index = y * 5 + x;
          const seq = state.config.content.sequence.find((item) => item.cell === index);
          const cx = state.width / 2 - cell * 2.5 + x * cell;
          const cy = state.height / 2 - cell * 2.5 + y * cell;
          const active = seq && Math.abs(state.modeState.timer - seq.time) < 0.16;
          const light = active ? 0.9 : 0.28 + state.modeState.pulse * 0.35;
          ctx.fillStyle = `hsla(${250 + x * 8 + y * 6}, 84%, ${20 + light * 30}%, ${0.18 + light * 0.32})`;
          ctx.fillRect(cx + 5, cy + 5, cell - 10, cell - 10);
          if (active) {
            drawSprite(ctx, state.images.sprites.padTile, cx + 12, cy + 12, cell - 24, cell - 24, {
              alpha: 0.88,
              glow: { color: state.palette.accent, blur: 18 }
            });
          }
        }
      }
      drawParticles(state);
    }
  },
  labRift: {
    setup(state) {
      state.modeState = {
        player: { x: state.width * 0.18, y: state.height * 0.5 },
        velocity: { x: 0, y: 0 },
        shards: state.config.content.shards.map((shard) => ({ ...shard, taken: false })),
        sentries: state.config.content.sentries.map((sentry) => ({ ...sentry })),
        goalOpen: false
      };
      state.handleKeyDown = (event) => { setMoveIntent(state, event, true); };
      state.handleKeyUp = (event) => { setMoveIntent(state, event, false); };
    },
    start(state) {
      state.score = 0;
      for (const shard of state.modeState.shards) shard.taken = false;
      state.modeState.goalOpen = false;
      state.modeState.player.x = state.width * 0.18;
      state.modeState.player.y = state.height * 0.5;
      state.modeState.velocity.x = 0;
      state.modeState.velocity.y = 0;
    },
    update(state, dt) {
      const speed = state.config.content.playerSpeed;
      state.modeState.player.x = clamp(state.modeState.player.x + state.modeState.velocity.x * speed * dt, 42, state.width - 42);
      state.modeState.player.y = clamp(state.modeState.player.y + state.modeState.velocity.y * speed * dt, 42, state.height - 42);
      for (const sentry of state.modeState.sentries) {
        sentry.phase += dt * sentry.rate;
      }
      for (const shard of state.modeState.shards) {
        if (!shard.taken && Math.hypot(shard.x * state.width - state.modeState.player.x, shard.y * state.height - state.modeState.player.y) < 24) {
          shard.taken = true;
          state.score += 20;
          emitParticles(state, shard.x * state.width, shard.y * state.height, state.palette.warning, 8);
        }
      }
      state.modeState.goalOpen = state.modeState.shards.every((shard) => shard.taken);
      if (state.modeState.goalOpen && state.modeState.player.x > state.width * 0.84) {
        state.running = false;
        state.bestScore = Math.max(state.bestScore, state.score);
        showOverlay(state, "Rift Cleared", `You sealed the room with ${state.score} points.`, "Run Again");
      }
      updateHud(state, [state.modeState.goalOpen ? "Exit Open" : "Collect Shards", `${state.score}`]);
      updateParticles(state, dt);
    },
    draw(state) {
      const { ctx } = state.dom;
      ctx.clearRect(0, 0, state.width, state.height);
      drawVerticalGradient(state);
      ctx.strokeStyle = "rgba(255,255,255,0.06)";
      for (let i = 0; i < state.width; i += 100) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, state.height);
        ctx.stroke();
      }
      ctx.fillStyle = state.modeState.goalOpen ? state.palette.accent : "rgba(255,255,255,0.08)";
      ctx.fillRect(state.width * 0.87, state.height * 0.28, 24, state.height * 0.44);
      for (const shard of state.modeState.shards) {
        if (shard.taken) continue;
        const x = shard.x * state.width;
        const y = shard.y * state.height;
        drawSprite(ctx, state.images.sprites.shardCrystal, x - 15, y - 15, 30, 30, {
          glow: { color: state.palette.warning, blur: 14 }
        });
      }
      for (const sentry of state.modeState.sentries) {
        const x = sentry.x * state.width + Math.sin(sentry.phase) * 28;
        const y = sentry.y * state.height + Math.cos(sentry.phase * 1.2) * 22;
        drawSprite(ctx, state.images.sprites.sentryDrone, x - 16, y - 16, 32, 32, {
          glow: { color: state.palette.danger, blur: 12 }
        });
      }
      drawSprite(ctx, state.images.sprites.runnerShip, state.modeState.player.x - 18, state.modeState.player.y - 18, 36, 36, {
        glow: { color: state.palette.accentStrong, blur: 12 }
      });
      drawParticles(state);
    }
  },
  phaseDrop: {
    setup(state) {
      state.modeState = {
        lane: 1,
        phases: state.config.content.phases,
        timer: 0,
        blocks: []
      };
      state.handleKeyDown = (event) => {
        if (event.key === "ArrowLeft") state.modeState.lane = Math.max(0, state.modeState.lane - 1);
        if (event.key === "ArrowRight") state.modeState.lane = Math.min(2, state.modeState.lane + 1);
        if (event.code === "Space") state.modeState.timer = 0;
      };
    },
    start(state) {
      state.score = 0;
      state.modeState.lane = 1;
      state.modeState.timer = 0;
      state.modeState.blocks = [];
    },
    update(state, dt) {
      state.modeState.timer += dt;
      state.speed = 1 + Math.min(2.8, state.time * 0.1);
      if (state.modeState.blocks.length < 9) {
        state.modeState.blocks.push({
          lane: Math.floor(Math.random() * 3),
          phase: Math.floor(Math.random() * state.modeState.phases.length),
          y: -70 - Math.random() * 120
        });
      }
      for (const block of state.modeState.blocks) {
        block.y += (260 + state.speed * 110) * dt;
      }
      state.modeState.blocks = state.modeState.blocks.filter((block) => block.y < state.height + 100);
      const activePhase = Math.floor(state.modeState.timer / 1.4) % state.modeState.phases.length;
      const playerY = state.height - 96;
      const hit = state.modeState.blocks.some((block) => block.lane === state.modeState.lane && Math.abs(block.y - playerY) < 28 && block.phase !== activePhase);
      if (hit) {
        state.running = false;
        showOverlay(state, "Phase Collapse", `You reached ${state.score} points before the wrong phase hit.`, "Retry Drop");
      }
      state.score += Math.floor(dt * 28);
      updateHud(state, [`Phase ${activePhase + 1}`, `${state.score}`]);
    },
    draw(state) {
      const { ctx } = state.dom;
      ctx.clearRect(0, 0, state.width, state.height);
      drawVerticalGradient(state);
      const lanes = [0.28, 0.5, 0.72];
      const activePhase = Math.floor(state.modeState.timer / 1.4) % state.modeState.phases.length;
      lanes.forEach((fraction, index) => {
        ctx.fillStyle = index === state.modeState.lane ? "rgba(143, 221, 255, 0.12)" : "rgba(255,255,255,0.04)";
        ctx.fillRect(state.width * fraction - 36, 0, 72, state.height);
      });
      for (const block of state.modeState.blocks) {
        const phaseColor = state.modeState.phases[block.phase];
        drawSprite(ctx, state.images.sprites.hazardBlock, state.width * lanes[block.lane] - 22, block.y, 44, 44, {
          alpha: block.phase === activePhase ? 1 : 0.5,
          glow: { color: phaseColor, blur: block.phase === activePhase ? 18 : 8 }
        });
      }
      drawSprite(ctx, state.images.sprites.padTile, state.width * lanes[state.modeState.lane] - 24, state.height - 114, 48, 48, {
        glow: { color: state.palette.accentStrong, blur: 14 }
      });
    }
  },
  harbor: {
    setup(state) {
      state.modeState = {
        pointer: { x: state.width / 2, y: state.height * 0.72 },
        boat: { x: state.width / 2, y: state.height * 0.72, vx: 0, vy: 0 },
        buoys: state.config.content.buoys.map((buoy) => ({ ...buoy, taken: false })),
        currents: state.config.content.currents
      };
      state.handlePointerMove = (event) => {
        state.modeState.pointer.x = event.clientX;
        state.modeState.pointer.y = event.clientY;
      };
    },
    start(state) {
      state.score = 0;
      state.modeState.boat.x = state.width / 2;
      state.modeState.boat.y = state.height * 0.72;
      for (const buoy of state.modeState.buoys) buoy.taken = false;
    },
    update(state, dt) {
      const boat = state.modeState.boat;
      boat.vx += (state.modeState.pointer.x - boat.x) * dt * 0.7;
      boat.vy += (state.modeState.pointer.y - boat.y) * dt * 0.45;
      const current = state.modeState.currents[Math.floor((boat.x / state.width) * state.modeState.currents.length)] || { x: 0, y: 0 };
      boat.x = clamp(boat.x + boat.vx * dt + current.x * 60 * dt, 32, state.width - 32);
      boat.y = clamp(boat.y + boat.vy * dt + current.y * 60 * dt, 32, state.height - 32);
      boat.vx *= 0.9;
      boat.vy *= 0.9;
      emitParticles(state, boat.x, boat.y + 18, state.palette.accentStrong, 1, "smoke");
      for (const buoy of state.modeState.buoys) {
        if (!buoy.taken && Math.hypot(buoy.x * state.width - boat.x, buoy.y * state.height - boat.y) < 26) {
          buoy.taken = true;
          state.score += 25;
          emitParticles(state, buoy.x * state.width, buoy.y * state.height, state.palette.accentStrong, 10);
        }
      }
      if (state.modeState.buoys.every((buoy) => buoy.taken)) {
        state.running = false;
        showOverlay(state, "Harbor Cleared", `All buoys collected. Score ${state.score}.`, "Sail Again");
      }
      updateHud(state, ["Collect Buoys", `${state.score}`]);
      updateParticles(state, dt);
    },
    draw(state) {
      const { ctx } = state.dom;
      ctx.clearRect(0, 0, state.width, state.height);
      drawVerticalGradient(state);
      for (let i = 0; i < state.modeState.currents.length; i += 1) {
        const bandWidth = state.width / state.modeState.currents.length;
        const current = state.modeState.currents[i];
        ctx.fillStyle = `rgba(111, 216, 255, ${0.05 + Math.abs(current.x) * 0.08})`;
        ctx.fillRect(i * bandWidth, 0, bandWidth, state.height);
      }
      for (const buoy of state.modeState.buoys) {
        if (buoy.taken) continue;
        drawSprite(ctx, state.images.sprites.buoyMarker, buoy.x * state.width - 16, buoy.y * state.height - 16, 32, 32, {
          glow: { color: state.palette.warning, blur: 12 }
        });
      }
      const boat = state.modeState.boat;
      drawSprite(ctx, state.images.sprites.boatSkiff, boat.x - 22, boat.y - 26, 44, 44, {
        glow: { color: state.palette.accentStrong, blur: 16 }
      });
      drawParticles(state);
    }
  },
  rhythm: {
    setup(state) {
      state.modeState = {
        timer: 0,
        beats: [...state.config.content.beats],
        lane: 1,
        pulses: []
      };
      state.handleKeyDown = (event) => {
        if (event.code !== "Space") return;
        const hitBeat = state.modeState.beats.find((beat) => !beat.hit && Math.abs(beat.time - state.modeState.timer) < 0.18);
        if (hitBeat) {
          hitBeat.hit = true;
          state.score += 18;
          emitParticles(state, state.width / 2, state.height * 0.45, state.palette.accent, 8);
        } else {
          state.score = Math.max(0, state.score - 6);
        }
      };
    },
    start(state) {
      state.score = 0;
      state.modeState.timer = 0;
      state.modeState.beats = state.config.content.beats.map((beat) => ({ ...beat, hit: false }));
    },
    update(state, dt) {
      state.modeState.timer += dt;
      const duration = state.config.content.loopDuration;
      if (state.modeState.timer > duration) {
        state.modeState.timer = 0;
        state.modeState.beats = state.config.content.beats.map((beat) => ({ ...beat, hit: false }));
      }
      updateHud(state, ["Hit Beats", `${state.score}`]);
      updateParticles(state, dt);
    },
    draw(state) {
      const { ctx } = state.dom;
      ctx.clearRect(0, 0, state.width, state.height);
      drawVerticalGradient(state);
      const baseY = state.height * 0.78;
      ctx.strokeStyle = "rgba(255,255,255,0.12)";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(state.width * 0.12, baseY);
      ctx.lineTo(state.width * 0.88, baseY);
      ctx.stroke();
      for (const beat of state.modeState.beats) {
        const progress = 1 - ((beat.time - state.modeState.timer + state.config.content.loopDuration) % state.config.content.loopDuration) / state.config.content.loopDuration;
        const x = state.width * 0.14 + progress * state.width * 0.72;
        const size = beat.hit ? 24 : 30;
        drawSprite(ctx, state.images.sprites.orbNode, x - size / 2, baseY - 40 - size / 2, size, size, {
          alpha: beat.hit ? 0.92 : 0.84,
          glow: { color: beat.hit ? state.palette.accentStrong : state.palette.accent, blur: 14 }
        });
      }
      drawSprite(ctx, state.images.sprites.padTile, state.width * 0.48 - 18, baseY - 68, 36, 36, {
        glow: { color: state.palette.warning, blur: 14 }
      });
      drawParticles(state);
    }
  },
  echo: {
    setup(state) {
      state.modeState = {
        pattern: [...state.config.content.pattern],
        step: 0,
        revealTimer: 0,
        showing: true,
        flashIndex: -1
      };
      state.handleKeyDown = (event) => {
        const mapping = state.config.content.inputMap[event.key.toLowerCase()];
        if (mapping == null || state.modeState.showing) return;
        if (mapping === state.modeState.pattern[state.modeState.step]) {
          state.score += 12;
          state.modeState.step += 1;
          state.modeState.flashIndex = mapping;
          if (state.modeState.step >= state.modeState.pattern.length) {
            state.running = false;
            showOverlay(state, "Loop Solved", `Pattern cleared with ${state.score} points.`, "Play Again");
          }
        } else {
          state.score = Math.max(0, state.score - 10);
          state.modeState.step = 0;
        }
      };
    },
    start(state) {
      state.score = 0;
      state.modeState.step = 0;
      state.modeState.revealTimer = 0;
      state.modeState.showing = true;
      state.modeState.flashIndex = -1;
    },
    update(state, dt) {
      if (state.modeState.showing) {
        state.modeState.revealTimer += dt;
        if (state.modeState.revealTimer > state.config.content.revealEvery * state.modeState.pattern.length) {
          state.modeState.showing = false;
        }
      }
      updateHud(state, [state.modeState.showing ? "Watch Pattern" : "Repeat Pattern", `${state.score}`]);
    },
    draw(state) {
      const { ctx } = state.dom;
      ctx.clearRect(0, 0, state.width, state.height);
      drawVerticalGradient(state);
      const colors = state.config.content.padColors;
      for (let i = 0; i < 4; i += 1) {
        const x = state.width / 2 + (i % 2 === 0 ? -1 : 1) * 90 - 70;
        const y = state.height / 2 + (i < 2 ? -1 : 1) * 90 - 70;
        const revealIndex = state.modeState.showing ? Math.floor(state.modeState.revealTimer / state.config.content.revealEvery) : -1;
        const active = state.modeState.pattern[revealIndex] === i || state.modeState.flashIndex === i;
        ctx.fillStyle = active ? colors[i] : `${colors[i]}55`;
        ctx.fillRect(x, y, 140, 140);
        drawSprite(ctx, state.images.sprites.padTile, x + 18, y + 18, 104, 104, {
          alpha: active ? 0.96 : 0.52,
          glow: { color: colors[i], blur: active ? 24 : 10 }
        });
      }
    }
  }
};

function laneX(state, index) {
  return state.width * state.config.content.lanes[index];
}

function refillOrbitTargets(state) {
  state.modeState.targets = state.config.content.rings.map((ring, index) => ({
    theta: Math.random() * Math.PI * 2,
    radiusBand: ring.radiusBand * Math.min(state.width, state.height),
    radius: ring.radius,
    velocity: ring.velocity,
    color: [state.palette.warning, state.palette.accent, state.palette.accentStrong][index % 3],
    hit: false,
    x: 0,
    y: 0
  }));
}

function setMoveIntent(state, event, active) {
  const velocity = state.modeState.velocity;
  if (event.key === "ArrowLeft" || event.key.toLowerCase() === "a") velocity.x = active ? -1 : velocity.x === -1 ? 0 : velocity.x;
  if (event.key === "ArrowRight" || event.key.toLowerCase() === "d") velocity.x = active ? 1 : velocity.x === 1 ? 0 : velocity.x;
  if (event.key === "ArrowUp" || event.key.toLowerCase() === "w") velocity.y = active ? -1 : velocity.y === -1 ? 0 : velocity.y;
  if (event.key === "ArrowDown" || event.key.toLowerCase() === "s") velocity.y = active ? 1 : velocity.y === 1 ? 0 : velocity.y;
}

function drawVerticalGradient(state) {
  const { ctx } = state.dom;
  const gradient = ctx.createLinearGradient(0, 0, 0, state.height);
  gradient.addColorStop(0, state.palette.bgTop);
  gradient.addColorStop(1, state.palette.bgBottom);
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, state.width, state.height);
}

function drawRunnerTrack(state) {
  const { ctx } = state.dom;
  ctx.strokeStyle = state.assets.motifs.runner.laneGlow;
  ctx.lineWidth = 2;
  for (let i = 1; i < state.config.content.lanes.length; i += 1) {
    const x = state.width * (state.config.content.lanes[i] - 0.09);
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, state.height);
    ctx.stroke();
  }
  ctx.strokeStyle = state.assets.motifs.runner.stripe;
  ctx.lineWidth = 6;
  ctx.lineCap = "round";
  const stripeOffset = (state.modeState.distance * 0.8) % 80;
  for (let y = -120 + stripeOffset; y < state.height + 120; y += 80) {
    ctx.beginPath();
    ctx.moveTo(state.width * 0.49, y);
    ctx.lineTo(state.width * 0.49, y + 44);
    ctx.stroke();
  }
}

export async function initArcadeGame({ configPath, assetsPath, canvasSelector, hudSelector, overlaySelector, panelTitleSelector, panelCopySelector, actionSelector }) {
  const [assetsResponse, configResponse] = await Promise.all([fetch(assetsPath), fetch(configPath)]);
  const [assets, config] = await Promise.all([assetsResponse.json(), configResponse.json()]);
  const [spriteImages, effectImages] = await Promise.all([
    loadImageMap(assetsPath, assets.sprites),
    loadImageMap(assetsPath, assets.effects)
  ]);
  const canvas = document.querySelector(canvasSelector);
  const hud = document.querySelector(hudSelector);
  const overlay = document.querySelector(overlaySelector);
  const panelTitle = document.querySelector(panelTitleSelector);
  const panelCopy = document.querySelector(panelCopySelector);
  const action = document.querySelector(actionSelector);
  const ctx = canvas.getContext("2d");

  const state = createBaseState(config, assets, {
    canvas,
    ctx,
    hud,
    overlay,
    panelTitle,
    panelCopy,
    action
  });
  state.images.sprites = spriteImages;
  state.images.effects = effectImages;
  state.shared = getConfigDefaults(config);
  if (config.content?.expertRecoveryUnlockScore && state.bestScore >= config.content.expertRecoveryUnlockScore) {
    config.overlay.startCopy += "\n\nExpert recovery drills are unlocked for the next run.";
  }

  const mode = modes[config.mode];
  if (!mode) {
    throw new Error(`Unknown arcade mode: ${config.mode}`);
  }
  state.mode = mode;

  mode.setup(state);
  ensureSharedPanels(state);
  initializeSettingsState(state);
  renderSharedPanels(state);
  bindSharedUi(state);
  resizeCanvas(state);
  updateHud(state, [config.hud.modeLabel, "Ready"]);
  showOverlay(state, config.overlay.startTitle, config.overlay.startCopy, config.overlay.startAction);

  action.addEventListener("click", () => {
    state.running = true;
    state.time = 0;
    mode.start(state);
    hideOverlay(state);
    scheduleFrame();
  });

  window.addEventListener("resize", () => resizeCanvas(state));
  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      if (state.ui.settingsOpen || state.ui.helpOpen || state.ui.menuOpen) {
        closeAllPanels(state);
      } else {
        openPanel(state, "menu");
      }
      return;
    }
    if (event.key.toLowerCase() === "h") {
      openPanel(state, "help");
      return;
    }
    if (event.key.toLowerCase() === "o") {
      openPanel(state, "settings");
      return;
    }
    if (!state.running && (event.code === "Space" || event.key === "Enter")) {
      state.running = true;
      state.time = 0;
      mode.start(state);
      hideOverlay(state);
      scheduleFrame();
      return;
    }
    if (state.ui.paused || state.ui.settingsOpen || state.ui.helpOpen) return;
    if (typeof state.handleKeyDown === "function") state.handleKeyDown(event);
  });
  window.addEventListener("keyup", (event) => {
    if (typeof state.handleKeyUp === "function") state.handleKeyUp(event);
  });
  window.addEventListener("pointermove", (event) => {
    if (typeof state.handlePointerMove === "function") state.handlePointerMove(event);
  });
  window.addEventListener("click", () => {
    if (typeof state.handleClick === "function") state.handleClick();
  });

  let lastTime = 0;
  let frameId = 0;

  const shouldAnimate = () =>
    !document.hidden &&
    (state.running || state.ui.settingsOpen || state.ui.helpOpen || state.ui.menuOpen);

  const scheduleFrame = () => {
    if (!frameId && shouldAnimate()) {
      frameId = requestAnimationFrame(frame);
    }
  };

  function frame(time) {
    frameId = 0;
    if (!shouldAnimate()) {
      lastTime = time;
      return;
    }

    const dt = Math.min(0.033, (time - lastTime) / 1000 || 0);
    lastTime = time;
    if (state.running && !state.ui.paused && !state.ui.settingsOpen && !state.ui.helpOpen) {
      state.time += dt;
      mode.update(state, dt);
      updateParticles(state, dt);
    }
    mode.draw(state);
    scheduleFrame();
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      cancelAnimationFrame(frameId);
      frameId = 0;
    } else {
      lastTime = performance.now();
      scheduleFrame();
    }
  });

  mode.draw(state);
}
