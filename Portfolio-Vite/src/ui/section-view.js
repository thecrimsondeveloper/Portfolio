import { buildProjectHref } from "../app/router.js";
import { renderIntroList } from "./intro-list.js";

const SECTION_PROJECT_LIMIT = 6;

export function renderSectionView(host, page, schema) {
  const projects = page.featuredProjectSlugs
    .map((slug) => schema.projects[slug])
    .filter(Boolean)
    .slice(0, SECTION_PROJECT_LIMIT)
    .map((project) => renderProjectCard(project))
    .join("");

  const tools = page.tools.map((tool) => `<span class="tag">${tool}</span>`).join("");

  host.innerHTML = `
    <div class="page-frame">
      <section class="section-header">
        <h1 class="section-heading">${page.title}</h1>
        <p class="section-subtitle">${page.subtitle}</p>
      </section>

      ${renderIntroList(page)}

      <section class="content-section content-section--plain" aria-labelledby="featured-work-heading">
        <div class="content-section-header">
          <h2 class="content-section-title" id="featured-work-heading">Featured Work</h2>
          <p class="content-section-copy">Selected projects presented one at a time with image, title, and summary.</p>
        </div>
        <div class="project-grid project-grid--stacked">${projects}</div>
      </section>

      <section class="content-section" aria-labelledby="tools-heading">
        <div class="content-section-header">
          <h2 class="content-section-title" id="tools-heading">Tools / Focus</h2>
        </div>
        <div class="tag-list">${tools}</div>
      </section>
    </div>
  `;
}

export function renderEmptySectionView(host, page) {
  host.innerHTML = `
    <div class="page-frame">
      <section class="section-header">
        <h1 class="section-heading">${page.title}</h1>
        <p class="section-subtitle">${page.subtitle}</p>
      </section>

      ${renderIntroList(page)}

      <section class="content-section" aria-labelledby="prototype-empty-heading">
        <div class="content-section-header">
          <h2 class="content-section-title" id="prototype-empty-heading">Nothing published yet</h2>
        </div>
        <section class="project-empty">
          <h1>Empty for now.</h1>
          <p>This tab is reserved for prototype experiments, rough slices, and early proof-of-concept work.</p>
        </section>
      </section>
    </div>
  `;
}

function renderProjectCard(project) {
  const linkButtons = [
    `<a class="button-link primary" href="${buildProjectHref(project.slug)}" data-route-link data-wobble>Project Details</a>`,
    ...project.links.map((link) => renderActionLink(link)),
  ].join("");

  const media = project.image
    ? `<div class="project-card-media"><img src="${project.image}" alt="${project.title}" loading="lazy" /></div>`
    : `
      <div class="project-card-accent">
        <span class="project-card-kind">${project.kind}</span>
      </div>
    `;

  return `
    <article class="project-card">
      ${media}
      <div class="project-card-body">
        <div>
          <span class="project-card-kind">${project.kind}</span>
          <h3>${project.title}</h3>
        </div>
        <p>${project.shortDescription}</p>
      </div>
      <div class="project-card-footer">
        <div class="project-card-links">${linkButtons}</div>
      </div>
    </article>
  `;
}

function renderActionLink(link) {
  const rel = link.external ? ' target="_blank" rel="noreferrer"' : "";
  return `<a class="button-link ${link.style || "ghost"}" href="${link.href}"${rel} data-wobble>${link.label}</a>`;
}
