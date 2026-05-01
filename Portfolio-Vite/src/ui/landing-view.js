import { addStars } from "../data/star-store.js";

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
      <div class="landing-scroll">
        <section class="landing-panel landing-panel--hero">
          <p class="landing-kicker">${profile.eyebrow}</p>
          <h1 class="landing-title" id="landing-heading">${profile.name}</h1>
          <p class="landing-copy">${page.subtitle}</p>
        </section>
        <section class="landing-panel">
          <p class="landing-panel-label">Systems</p>
          <h2>Interfaces, automation, games, and agentic tools.</h2>
          <p>Work is organized as quiet surfaces over a living background: readable first, cinematic second, expandable always.</p>
        </section>
        <section class="landing-panel">
          <p class="landing-panel-label">Arcade</p>
          <h2>Stars are persistent across the site.</h2>
          <p>Tap the slow shooting stars as they cross the scene to collect them in the counter.</p>
        </section>
        <section class="landing-panel landing-panel--continue">
          <p class="landing-panel-label">Continue</p>
          <h2>Enter the portfolio.</h2>
          <a class="landing-continue-link" href="/?page=full-stack" data-route-link>
            Continue
          </a>
        </section>
      </div>
    </section>
  `;

  const sceneHost = host.querySelector("[data-star-fishing-scene]");
  if (sceneHost) {
    const { createStarFishingScene } = await import("./star-fishing-scene.js");
    if (landingToken !== activeLandingToken || !sceneHost.isConnected) return;
    activeLandingScene = createStarFishingScene(sceneHost, { addStars });
  }
}
