import { renderIntroList } from "./intro-list.js";

export function renderConnectView(host, page, profile) {
  host.innerHTML = `
    <div class="page-frame">
      <section class="section-header">
        <h1 class="section-heading">${page.title}</h1>
        <p class="section-subtitle">${page.subtitle}</p>
      </section>

      ${renderIntroList(page)}

      <section class="content-section" aria-labelledby="socials-heading">
        <div class="content-section-header">
          <h2 class="content-section-title" id="socials-heading">Socials</h2>
          <p class="content-section-copy">Reach out through the channels below. Email is best for direct contact.</p>
        </div>
        <div class="connect-grid">
          <a class="connect-card" href="mailto:${profile.email}" data-wobble>
            <span class="connect-card-label">Email</span>
            <span class="connect-card-value">${profile.email}</span>
            <span class="connect-card-note">Best for project inquiries, follow-up questions, and quick coordination.</span>
          </a>
          <a class="connect-card" href="${profile.github}" target="_blank" rel="noreferrer" data-wobble>
            <span class="connect-card-label">GitHub</span>
            <span class="connect-card-value">crimsonwheeler</span>
            <span class="connect-card-note">Source code, experiments, and technical work in progress.</span>
          </a>
          <a class="connect-card" href="${profile.linkedin}" target="_blank" rel="noreferrer" data-wobble>
            <span class="connect-card-label">LinkedIn</span>
            <span class="connect-card-value">Crimson Wheeler</span>
            <span class="connect-card-note">Professional background and network connections.</span>
          </a>
        </div>
      </section>
    </div>
  `;
}
