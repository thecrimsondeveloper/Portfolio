import { buildProjectHref } from "../app/router.js";
import { renderProjectMedia } from "./project-media.js";

export function renderProjectCard(project, linkLabel = "View Details") {
  const cardClass = project.media ? "project-card project-card--video" : "project-card";
  const linkButtons = [
    `<a class="button-link primary" href="${buildProjectHref(project.slug)}" data-route-link data-wobble>${linkLabel}</a>`,
    ...project.links.map((link) => renderActionLink(link)),
  ].join("");

  const media = renderProjectMedia(project, "project-card-media") || (project.image
    ? `<div class="project-card-media"><img src="${project.image}" alt="${project.title}" loading="lazy" /></div>`
    : `
      <div class="project-card-accent">
        <span class="project-card-kind">${project.kind}</span>
      </div>
    `);

  return `
    <article class="${cardClass}">
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
