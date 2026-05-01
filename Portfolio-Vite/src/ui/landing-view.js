import { addStars } from "../data/star-store.js";
import { buildPageHref } from "../app/router.js";

let activeLandingScene = null;
let activeLandingToken = 0;

export function cleanupLandingView() {
  activeLandingToken += 1;
  if (!activeLandingScene) return;
  activeLandingScene.destroy();
  activeLandingScene = null;
}

export async function renderLandingView(host, page, profile) {
  cleanupLandingView();
  const landingToken = ++activeLandingToken;
  host.innerHTML = `
    <section class="landing-page" aria-labelledby="landing-heading">
      <div class="landing-scene-host" data-star-fishing-scene aria-hidden="true"></div>
      <div class="landing-hero">
        <div class="landing-copy-shell">
          <p class="landing-kicker">${profile.eyebrow}</p>
          <h1 class="landing-title" id="landing-heading">${profile.name}</h1>
          <p class="landing-copy">${page.subtitle}</p>
        </div>
      </div>
      <div class="landing-actions">
        <a class="landing-button" href="${buildPageHref("full-stack")}" data-route-link>Work</a>
        <a class="landing-button" href="${buildPageHref("projects")}" data-route-link>Projects</a>
        <a class="landing-button" href="${buildPageHref("prototypes")}" data-route-link>Arcade</a>
      </div>
    </section>
  `;

  const sceneHost = host.querySelector("[data-star-fishing-scene]");
  if (sceneHost) {
    scheduleLandingScene(sceneHost, landingToken);
  }
}

function scheduleLandingScene(sceneHost, landingToken) {
  const loadScene = async () => {
    if (landingToken !== activeLandingToken || !sceneHost.isConnected) return;
    const { createStarFishingScene } = await import("./star-fishing-scene.js");
    if (landingToken !== activeLandingToken || !sceneHost.isConnected) return;
    activeLandingScene = createStarFishingScene(sceneHost, { addStars });
  };

  const startLoad = () => {
    if (window.requestIdleCallback) {
      window.requestIdleCallback(loadScene, { timeout: 1500 });
    } else {
      window.setTimeout(loadScene, 150);
    }
  };

  if (window.requestAnimationFrame) {
    window.requestAnimationFrame(startLoad);
  } else {
    startLoad();
  }
}
