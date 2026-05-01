import { buildPageHref } from "../app/router.js";

export function renderProjectView(host, project, page, profileName) {
  const actions = [
    `<a class="button-link primary" href="${buildPageHref(page.id)}" data-route-link data-wobble>Back to ${page.title}</a>`,
    ...project.links.map((link) => renderActionLink(link)),
  ].join("");

  const technologies = project.technologies
    .map((item) => `<span class="tag">${item}</span>`)
    .join("");

  const features = project.features.map((feature) => `<li>${feature}</li>`).join("");

  const projectArt = project.image
    ? `<div class="project-art"><img src="${project.image}" alt="${project.title}" /></div>`
    : `
      <div class="project-art no-image">
        <div class="project-art-copy">
          <h2>${project.kind}</h2>
          <p>${project.shortDescription}</p>
        </div>
      </div>
    `;

  document.title = `${project.title} | ${profileName}`;
  host.innerHTML = `
    <article class="project-shell">
      <div class="project-hero">
        <div class="project-copy">
          <div class="project-breadcrumb">${page.title}</div>
          <h1 class="project-title">${project.title}</h1>
          <p class="project-summary">${project.description}</p>
          <div class="project-actions">${actions}</div>
        </div>
        ${projectArt}
      </div>

      <div class="project-content">
        <section class="project-section" aria-labelledby="detail-heading">
          <h2 id="detail-heading">Overview</h2>
          <p>${project.shortDescription}</p>
        </section>

        <section class="project-section" aria-labelledby="feature-heading">
          <h2 id="feature-heading">Key Highlights</h2>
          <ul>${features}</ul>
        </section>

        <section class="project-section" aria-labelledby="tech-heading">
          <h2 id="tech-heading">Technologies</h2>
          <div class="tag-list">${technologies}</div>
        </section>
      </div>
    </article>
  `;
}

export function renderProjectMissing(host, profileName) {
  document.title = `Project Not Found | ${profileName}`;
  host.innerHTML = `
    <section class="project-empty">
      <h1>Project not found.</h1>
      <p>The requested project does not exist. Use the section navigation to return to the portfolio.</p>
      <div class="utility-links">
        <a class="button-link primary" href="${buildPageHref("full-stack")}" data-route-link data-wobble>Go to Full Stack</a>
      </div>
    </section>
  `;
}

function renderActionLink(link) {
  const rel = link.external ? ' target="_blank" rel="noreferrer"' : "";
  return `<a class="button-link ${link.style || "ghost"}" href="${link.href}"${rel} data-wobble>${link.label}</a>`;
}
