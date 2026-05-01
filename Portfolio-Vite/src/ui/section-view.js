import { buildPageHref } from "../app/router.js";
import { renderIntroList } from "./intro-list.js";

const SECTION_PROJECT_LIMIT = 6;
const WORK_IDEAS = ["automation", "research", "game-dev", "agentic-engineering"];

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

      ${page.id === "full-stack" ? renderWorkIdeas(page, schema) : ""}
      ${page.id === "full-stack" ? renderWorkChips() : ""}
      ${renderIntroList(page)}

      ${renderCollapsibleSection(
        "featured-work",
        "Featured Work",
        "Selected projects presented one at a time with image, title, and summary.",
        `<div class="project-grid project-grid--stacked">${projects}</div>`,
        true
      )}

      ${renderCollapsibleSection(
        "tools",
        "Tools / Focus",
        "The technologies and capabilities that power each work area.",
        `<div class="tag-list">${tools}</div>`
      )}
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

function renderWorkIdeas(page, schema) {
  const ideaCards = WORK_IDEAS
    .map((ideaId) => schema.pages[ideaId])
    .filter(Boolean)
    .map((idea) => renderWorkIdeaCard(idea))
    .join("");

  return renderCollapsibleSection(
    "work-ideas",
    "Work ideas",
    "Existing idea areas that define the Work tab and its expertise focus.",
    `<div class="idea-grid">${ideaCards}</div>`,
    true
  );
}

function renderCollapsibleSection(id, title, summary, content, open = false) {
  return `
    <details class="section-block" id="${id}"${open ? " open" : ""}>
      <summary class="section-block-summary">
        <div>
          <span class="section-block-title">${title}</span>
          <span class="section-block-note">${summary}</span>
        </div>
        <span class="section-block-icon" aria-hidden="true">▾</span>
      </summary>
      <div class="section-block-content">${content}</div>
    </details>
  `;
}

function renderWorkIdeaCard(idea) {
  const url = buildPageHref(idea.id);
  const projectCount = idea.featuredProjectSlugs?.length || 0;
  return `
    <article class="idea-card">
      <div class="idea-card-body">
        <span class="idea-card-label">${idea.title}</span>
        <h3>${idea.title}</h3>
        <p>${idea.description}</p>
      </div>
      <div class="idea-card-footer">
        <span>${projectCount} project${projectCount === 1 ? "" : "s"}</span>
        <a class="button-link secondary" href="${url}" data-route-link>Explore</a>
      </div>
    </article>
  `;
}

function renderWorkChips() {
  const filters = [
    { id: "full-stack", label: "Full Stack" },
    { id: "automation", label: "Automation" },
    { id: "research", label: "Research" },
    { id: "game-dev", label: "Game Dev / XR" },
    { id: "agentic-engineering", label: "Agentic" },
  ];

  return `
    <div class="work-chips">
      ${filters
        .map(
          (filter) => `
            <a class="button-link secondary" href="/?page=${encodeURIComponent(filter.id)}" data-route-link>
              ${filter.label}
            </a>
          `
        )
        .join("")}
    </div>
  `;
}
