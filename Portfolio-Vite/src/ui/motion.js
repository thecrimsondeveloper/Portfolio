const MAX_OFFSET = 3;
const MAX_ROTATION = 0.6;
const HOVER_SCALE = 1.01;
const PRESS_SCALE = 0.985;

export function initInteractiveMotion(root = document) {
  if (!(root instanceof Document || root instanceof HTMLElement)) {
    return () => {};
  }

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const finePointer = window.matchMedia("(pointer: fine)");

  const isEnabled = () => finePointer.matches && !reducedMotion.matches;
  let pendingMove = null;
  let moveFrame = 0;

  const findTarget = (event) =>
    event.target instanceof HTMLElement ? event.target.closest("[data-wobble]") : null;

  const isDenseMotionTarget = (element) =>
    Boolean(element.closest(".project-grid, .prototype-book-grid, .arcade-rail"));

  const applyMotion = (element, event) => {
    const rect = element.getBoundingClientRect();
    const xRatio = (event.clientX - rect.left) / rect.width - 0.5;
    const yRatio = (event.clientY - rect.top) / rect.height - 0.5;
    const lift = -2;
    const scale = element.dataset.wobblePressed === "true" ? PRESS_SCALE : HOVER_SCALE;

    element.style.setProperty("--wobble-x", `${(xRatio * MAX_OFFSET * 2).toFixed(2)}px`);
    element.style.setProperty(
      "--wobble-y",
      `${(lift + yRatio * MAX_OFFSET * 2).toFixed(2)}px`
    );
    element.style.setProperty("--wobble-rotate", `${(xRatio * MAX_ROTATION * 2).toFixed(2)}deg`);
    element.style.setProperty("--wobble-scale", String(scale));
  };

  const resetMotion = (element) => {
    element.style.removeProperty("--wobble-x");
    element.style.removeProperty("--wobble-y");
    element.style.removeProperty("--wobble-rotate");
    element.style.removeProperty("--wobble-scale");
    element.dataset.wobblePressed = "false";
  };

  const handlePointerMove = (event) => {
    if (!isEnabled()) return;
    const target = findTarget(event);
    if (!(target instanceof HTMLElement)) return;
    if (isDenseMotionTarget(target)) return;

    pendingMove = { target, clientX: event.clientX, clientY: event.clientY };
    if (moveFrame) return;

    moveFrame = window.requestAnimationFrame(() => {
      moveFrame = 0;
      if (!pendingMove || !pendingMove.target.isConnected) return;
      applyMotion(pendingMove.target, pendingMove);
      pendingMove = null;
    });
  };

  const handlePointerOver = (event) => {
    if (!isEnabled()) return;
    const target = findTarget(event);
    if (!(target instanceof HTMLElement)) return;
    target.dataset.wobblePressed = "false";
    applyMotion(target, event);
  };

  const handlePointerOut = (event) => {
    const target = findTarget(event);
    if (!(target instanceof HTMLElement)) return;

    const nextTarget =
      event.relatedTarget instanceof HTMLElement ? event.relatedTarget.closest("[data-wobble]") : null;
    if (nextTarget === target) return;

    resetMotion(target);
  };

  const handlePointerDown = (event) => {
    if (!isEnabled()) return;
    const target = findTarget(event);
    if (!(target instanceof HTMLElement)) return;
    target.dataset.wobblePressed = "true";
    applyMotion(target, event);
  };

  const handlePointerUp = (event) => {
    const target = findTarget(event);
    if (!(target instanceof HTMLElement)) return;
    target.dataset.wobblePressed = "false";
    if (isEnabled()) {
      applyMotion(target, event);
    } else {
      resetMotion(target);
    }
  };

  const clearAllMotion = () => {
    document.querySelectorAll("[data-wobble]").forEach((element) => {
      if (element instanceof HTMLElement) {
        resetMotion(element);
      }
    });
  };

  root.addEventListener("pointermove", handlePointerMove, true);
  root.addEventListener("pointerover", handlePointerOver, true);
  root.addEventListener("pointerout", handlePointerOut, true);
  root.addEventListener("pointerdown", handlePointerDown, true);
  root.addEventListener("pointerup", handlePointerUp, true);
  root.addEventListener("pointercancel", handlePointerUp, true);
  reducedMotion.addEventListener("change", clearAllMotion);
  finePointer.addEventListener("change", clearAllMotion);

  return () => {
    root.removeEventListener("pointermove", handlePointerMove, true);
    root.removeEventListener("pointerover", handlePointerOver, true);
    root.removeEventListener("pointerout", handlePointerOut, true);
    root.removeEventListener("pointerdown", handlePointerDown, true);
    root.removeEventListener("pointerup", handlePointerUp, true);
    root.removeEventListener("pointercancel", handlePointerUp, true);
    reducedMotion.removeEventListener("change", clearAllMotion);
    finePointer.removeEventListener("change", clearAllMotion);
    window.cancelAnimationFrame(moveFrame);
    clearAllMotion();
  };
}
