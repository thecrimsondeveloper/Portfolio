const VIEWPORT_MARGIN = 16;
const PANEL_GAP = 12;

let activeOverlayCleanup = null;

export function clearOverlay(root) {
  if (typeof activeOverlayCleanup === "function") {
    const cleanup = activeOverlayCleanup;
    activeOverlayCleanup = null;
    cleanup();
    return;
  }

  if (root instanceof HTMLElement) {
    root.replaceChildren();
  }
}

export function showAnchoredOverlay(
  root,
  { anchor, markup, panelClassName = "", panelId = "", preferTop = true, width = null }
) {
  if (!(root instanceof HTMLElement) || !(anchor instanceof HTMLElement)) {
    return null;
  }

  clearOverlay(root);

  const panel = document.createElement("div");
  panel.className = ["app-overlay-panel", panelClassName].filter(Boolean).join(" ");
  panel.dataset.overlayPanel = "true";
  panel.style.position = "fixed";
  panel.style.pointerEvents = "auto";

  if (panelId) {
    panel.id = panelId;
  }

  panel.innerHTML = markup;
  root.replaceChildren(panel);

  let frameId = 0;

  const updatePosition = () => {
    cancelAnimationFrame(frameId);
    frameId = window.requestAnimationFrame(() => {
      if (!anchor.isConnected || !panel.isConnected) {
        cleanup();
        return;
      }

      positionPanel(panel, anchor, width, preferTop);
    });
  };

  const cleanup = () => {
    cancelAnimationFrame(frameId);
    window.removeEventListener("resize", updatePosition);
    document.removeEventListener("scroll", updatePosition, true);

    if (panel.isConnected) {
      panel.remove();
    }

    if (root.childElementCount === 0) {
      root.replaceChildren();
    }

    if (activeOverlayCleanup === cleanup) {
      activeOverlayCleanup = null;
    }
  };

  activeOverlayCleanup = cleanup;
  window.addEventListener("resize", updatePosition);
  document.addEventListener("scroll", updatePosition, true);
  updatePosition();

  return {
    cleanup,
    panel,
    updatePosition,
  };
}

function positionPanel(panel, anchor, requestedWidth, preferTop) {
  const anchorRect = anchor.getBoundingClientRect();
  const panelWidth = Math.max(
    280,
    Math.min(requestedWidth || anchorRect.width, window.innerWidth - VIEWPORT_MARGIN * 2)
  );

  panel.style.width = `${panelWidth}px`;
  panel.style.maxWidth = `calc(100vw - ${VIEWPORT_MARGIN * 2}px)`;
  panel.style.visibility = "hidden";
  panel.style.left = "0px";
  panel.style.top = "0px";

  const panelRect = panel.getBoundingClientRect();
  const topSpace = anchorRect.top - VIEWPORT_MARGIN;
  const bottomSpace = window.innerHeight - anchorRect.bottom - VIEWPORT_MARGIN;
  const canPlaceTop = topSpace >= panelRect.height + PANEL_GAP;
  const canPlaceBottom = bottomSpace >= panelRect.height + PANEL_GAP;

  let top = anchorRect.bottom + PANEL_GAP;
  if ((preferTop && canPlaceTop) || (!canPlaceBottom && topSpace > bottomSpace)) {
    top = anchorRect.top - panelRect.height - PANEL_GAP;
  }

  const clampedTop = clamp(top, VIEWPORT_MARGIN, window.innerHeight - panelRect.height - VIEWPORT_MARGIN);
  const clampedLeft = clamp(
    anchorRect.left,
    VIEWPORT_MARGIN,
    window.innerWidth - panelRect.width - VIEWPORT_MARGIN
  );

  panel.style.left = `${clampedLeft}px`;
  panel.style.top = `${clampedTop}px`;
  panel.style.visibility = "visible";
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}
