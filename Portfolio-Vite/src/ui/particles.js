const DESKTOP_PARTICLES = 22;
const TABLET_PARTICLES = 12;
const SPEED_RANGE = 0.18;

export function initParticles(canvas) {
  if (!(canvas instanceof HTMLCanvasElement)) {
    return () => {};
  }

  const context = canvas.getContext("2d");
  if (!context) {
    return () => {};
  }

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const coarsePointer = window.matchMedia("(pointer: coarse)");
  const host = canvas.closest(".app-main");

  let frameId = 0;
  let width = 0;
  let height = 0;
  let particles = [];
  let particleColor = "rgba(255, 245, 241, 0.22)";
  const pointer = {
    active: false,
    x: 0,
    y: 0,
  };

  const isEnabled = () =>
    !document.hidden &&
    !document.body.classList.contains("arcade-player-mode") &&
    !reducedMotion.matches &&
    !coarsePointer.matches;

  const resize = () => {
    const rect = canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;

    width = Math.max(1, rect.width);
    height = Math.max(1, rect.height);
    canvas.width = Math.floor(width * ratio);
    canvas.height = Math.floor(height * ratio);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    particleColor =
      getComputedStyle(document.body).getPropertyValue("--particle-color").trim() ||
      "rgba(255, 245, 241, 0.22)";
  };

  const createParticle = () => ({
    alpha: Math.random() * 0.4 + 0.08,
    radius: Math.random() * 1.6 + 0.8,
    vx: (Math.random() - 0.5) * SPEED_RANGE,
    vy: (Math.random() - 0.5) * SPEED_RANGE,
    x: Math.random() * width,
    y: Math.random() * height,
  });

  const seedParticles = () => {
    const targetCount = window.innerWidth >= 1024 ? DESKTOP_PARTICLES : TABLET_PARTICLES;
    particles = Array.from({ length: targetCount }, createParticle);
  };

  const clearCanvas = () => {
    context.clearRect(0, 0, width, height);
  };

  const updateParticles = () => {
    particleColor =
      getComputedStyle(document.body).getPropertyValue("--particle-color").trim() || particleColor;
    clearCanvas();

    particles.forEach((particle) => {
      if (pointer.active) {
        const dx = pointer.x - particle.x;
        const dy = pointer.y - particle.y;
        const distanceSquared = dx * dx + dy * dy;

        if (distanceSquared > 1 && distanceSquared < 42000) {
          const force = Math.min(0.035, 48 / distanceSquared);
          particle.vx += dx * force;
          particle.vy += dy * force;
        }
      }

      particle.vx *= 0.985;
      particle.vy *= 0.985;
      particle.x += particle.vx;
      particle.y += particle.vy;

      if (particle.x < -8) particle.x = width + 8;
      if (particle.x > width + 8) particle.x = -8;
      if (particle.y < -8) particle.y = height + 8;
      if (particle.y > height + 8) particle.y = -8;

      context.beginPath();
      context.fillStyle = particleColor.replace(/[\d.]+\)\s*$/, `${particle.alpha})`);
      context.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      context.fill();
    });
  };

  const frame = () => {
    if (!isEnabled()) {
      clearCanvas();
      return;
    }

    updateParticles();
    frameId = window.requestAnimationFrame(frame);
  };

  const restart = () => {
    window.cancelAnimationFrame(frameId);
    resize();

    if (!isEnabled()) {
      clearCanvas();
      return;
    }

    seedParticles();
    frameId = window.requestAnimationFrame(frame);
  };

  const handlePointerMove = (event) => {
    if (!(host instanceof HTMLElement) || !isEnabled()) return;
    const rect = canvas.getBoundingClientRect();
    pointer.active = true;
    pointer.x = event.clientX - rect.left;
    pointer.y = event.clientY - rect.top;
  };

  const handlePointerLeave = () => {
    pointer.active = false;
  };

  const handleCapabilityChange = () => {
    restart();
  };

  const bodyObserver = new MutationObserver(restart);

  if (host instanceof HTMLElement) {
    host.addEventListener("pointermove", handlePointerMove);
    host.addEventListener("pointerleave", handlePointerLeave);
  }

  window.addEventListener("resize", restart);
  reducedMotion.addEventListener("change", handleCapabilityChange);
  coarsePointer.addEventListener("change", handleCapabilityChange);
  document.addEventListener("visibilitychange", restart);
  bodyObserver.observe(document.body, { attributes: true, attributeFilter: ["class"] });

  restart();

  return () => {
    window.cancelAnimationFrame(frameId);
    window.removeEventListener("resize", restart);
    reducedMotion.removeEventListener("change", handleCapabilityChange);
    coarsePointer.removeEventListener("change", handleCapabilityChange);
    document.removeEventListener("visibilitychange", restart);
    bodyObserver.disconnect();

    if (host instanceof HTMLElement) {
      host.removeEventListener("pointermove", handlePointerMove);
      host.removeEventListener("pointerleave", handlePointerLeave);
    }

    clearCanvas();
  };
}
