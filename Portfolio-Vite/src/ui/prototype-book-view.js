import { renderIntroList } from "./intro-list.js";
import { renderProjectCard } from "./project-card.js";
import { hydrateProjectVideos } from "./project-media.js";

export function renderPrototypeBookView(host, page, schema) {
  const projects = Object.values(schema.projects)
    .filter((project) => project.media)
    .map((project) => renderProjectCard(project, "View Capture Details"))
    .join("");

  host.innerHTML = `
    <div class="page-frame">
      <section class="section-header">
        <h1 class="section-heading">Gameplay Captures</h1>
        <p class="section-subtitle">Short, verified gameplay clips replace fragile embedded builds. Each card documents the prototype without making the portfolio host its software.</p>
      </section>

      ${renderIntroList(page)}

      <section class="content-section" aria-labelledby="gameplay-capture-heading">
        <div class="content-section-header">
          <h2 class="content-section-title" id="gameplay-capture-heading">Browser game prototypes</h2>
          <p class="content-section-copy">Videos are muted, limited to two simultaneous players, and replaced by still images when reduced motion is enabled or media is unavailable.</p>
        </div>
        <div class="project-grid project-grid--stacked">${projects}</div>
      </section>
    </div>
  `;

  hydrateProjectVideos(host);
}
