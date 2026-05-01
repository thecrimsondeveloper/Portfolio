import { initArcadeGame } from "./arcade-runtime.js";

const bootstrapper = document.querySelector("[data-arcade-config]");

if (!bootstrapper) {
  throw new Error("Arcade bootstrap requires a [data-arcade-config] script.");
}

initArcadeGame({
  configPath: bootstrapper.dataset.arcadeConfig,
  assetsPath: bootstrapper.dataset.arcadeAssets || "./arcade-assets.json",
  canvasSelector: "#game",
  hudSelector: "#hud",
  overlaySelector: "#overlay",
  panelTitleSelector: "#overlay-title",
  panelCopySelector: "#overlay-copy",
  actionSelector: "#action"
});
