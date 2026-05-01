import { renderIntroList } from "./intro-list.js";

export function renderSettingsView(host, page, profile) {
  host.innerHTML = `
    <div class="page-frame">
      <section class="section-header">
        <h1 class="section-heading">${page.title}</h1>
        <p class="section-subtitle">${page.subtitle}</p>
      </section>

      ${renderIntroList(page)}

      <section class="content-section" aria-labelledby="settings-principles-heading">
        <div class="content-section-header">
          <h2 class="content-section-title" id="settings-principles-heading">Interface Principles</h2>
          <p class="content-section-copy">
            This portfolio now runs from one shared visual system so every section keeps the same rhythm,
            density, and presentation language.
          </p>
        </div>
        <div class="connect-grid">
          <article class="connect-card" data-wobble>
            <div class="connect-card-copy">
              <h3>Single Baseline</h3>
              <p>
                Theme, type, spacing, and card geometry stay fixed so the work reads consistently
                from page to page.
              </p>
            </div>
          </article>
          <article class="connect-card" data-wobble>
            <div class="connect-card-copy">
              <h3>Project First</h3>
              <p>
                Visual controls are removed so the settings area supports the portfolio instead of
                competing with it.
              </p>
            </div>
          </article>
          <article class="connect-card" data-wobble>
            <div class="connect-card-copy">
              <h3>Direct Contact</h3>
              <p>
                For collaboration, reach out through the Connect section or email
                <a href="mailto:${profile.email}">${profile.email}</a>.
              </p>
            </div>
          </article>
        </div>
      </section>
    </div>
  `;
}
