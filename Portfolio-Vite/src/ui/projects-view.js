import { renderProjectCard } from "./project-card.js";
import { hydrateProjectVideos } from "./project-media.js";

const PROJECT_CATEGORIES = [
  {
    id: "agentic-engineering",
    title: "Agentic Engineering / Automation",
    summary: "Agentic systems, local inference tooling, and automation workflows.",
    predicate: (project) => project.section === "agentic-engineering" || project.kind === "Agentic Engineering",
  },
  {
    id: "immersive-technology",
    title: "Immersive Technology",
    summary: "XR and spatial experiences that extend gameplay into immersive spaces.",
    predicate: (project) => project.kind === "XR" || /vr|xr|immersive|spatial|quest/i.test(project.title + project.description),
  },
  {
    id: "game-development",
    title: "Game Development",
    summary: "Playable game work, demos, and browser gameplay experiments.",
    predicate: (project) => project.section === "game-dev" || /game dev|demo game|gameplay/i.test(project.kind.toLowerCase()),
  },
  {
    id: "tooling",
    title: "Tooling",
    summary: "Automation, deployment, and operations tooling for technical teams.",
    predicate: (project) => project.section === "full-stack" && /tool|automation|deployment|workflow|runtime|system/i.test(project.title + project.shortDescription + project.description),
  },
  {
    id: "full-stack",
    title: "Full Stack",
    summary: "End-to-end product, interface, and delivery work across software and systems.",
    predicate: (project) => project.section === "full-stack",
  },
];

export function renderProjectsView(host, page, schema) {
  const allProjects = Object.values(schema.projects);
  const categorized = categorizeProjects(allProjects);
  const categoryBlocks = PROJECT_CATEGORIES.map((category) => {
    const projects = categorized[category.id] || [];
    return renderProjectCategoryBlock(category, projects);
  }).filter(Boolean).join("");

  host.innerHTML = `
    <div class="page-frame">
      <section class="section-header">
        <h1 class="section-heading">${page.title}</h1>
        <p class="section-subtitle">${page.subtitle}</p>
      </section>

      <div class="content-section content-section--plain" aria-labelledby="projects-overview-heading">
        <div class="content-section-header">
          <h2 class="content-section-title" id="projects-overview-heading">Project categories</h2>
          <p class="content-section-copy">Browse the project portfolio by the work streams that best describe each implementation type.</p>
        </div>
      </div>

      ${categoryBlocks}
    </div>
  `;
  hydrateProjectVideos(host);
}

function categorizeProjects(projects) {
  const assigned = new Set();
  return PROJECT_CATEGORIES.reduce((result, category) => {
    const matches = projects.filter((project) => {
      if (assigned.has(project.slug)) return false;
      if (!category.predicate(project)) return false;
      assigned.add(project.slug);
      return true;
    });
    result[category.id] = matches;
    return result;
  }, {});
}

function renderProjectCategoryBlock(category, projects) {
  if (!projects.length) return "";
  const cardMarkup = projects.map((project) => renderProjectCard(project)).join("");
  return renderCollapsibleSection(
    category.id,
    category.title,
    category.summary,
    `<div class="project-grid project-grid--stacked">${cardMarkup}</div>`,
    true
  );
}

function renderProjectSectionBlock(point, open) {
  return renderCollapsibleSection(
    `project-${point.pair.toLowerCase().replace(/[^a-z0-9]+/gi, "-")}`,
    point.pair,
    point.text,
    `<p>${point.text}</p>`,
    open
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
